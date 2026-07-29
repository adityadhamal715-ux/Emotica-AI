"""
camera.py
=========
A background-threaded webcam reader plus a MediaPipe-based face
detector. Running capture on its own thread decouples grabbing frames
from the (slower) Streamlit render / inference loop, which is what
keeps the feed smooth instead of freezing on every `cap.read()` call.
"""

from __future__ import annotations

import logging
import platform
import threading
import time
from dataclasses import dataclass

import cv2
import numpy as np

import config

logger = logging.getLogger(__name__)

# On Windows, cv2.CAP_ANY frequently hangs or silently fails to open the
# webcam. cv2.CAP_DSHOW (DirectShow) is far more reliable there. On other
# platforms we stick with CAP_ANY (DSHOW doesn't exist on Linux/Mac).
_PREFERRED_BACKEND = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY

_FALLBACK_BACKENDS: list[tuple[int, str]] = (
    [(cv2.CAP_MSMF, "MSMF"), (cv2.CAP_ANY, "ANY (auto)")]
    if platform.system() == "Windows"
    else [(cv2.CAP_ANY, "ANY (auto)")]
)


def _backend_name(backend: int) -> str:
    return {cv2.CAP_DSHOW: "DSHOW", cv2.CAP_MSMF: "MSMF", cv2.CAP_ANY: "ANY (auto)"}.get(
        backend, str(backend)
    )


def _fallback_indices(preferred: int) -> list[int]:
    # Try the requested index first, then a couple of common alternates
    # (some laptops enumerate the built-in webcam at 1 instead of 0).
    candidates = [preferred, 0, 1, 2]
    seen: set[int] = set()
    ordered: list[int] = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


@dataclass
class FaceBox:
    x: int
    y: int
    w: int
    h: int
    confidence: float


class CameraStream:
    """
    Continuously reads frames from a webcam on a background thread and
    exposes only the *latest* frame, so consumers never block on I/O
    and never fall behind (old frames are simply dropped).
    """

    def __init__(
        self,
        camera_index: int = config.DEFAULT_CAMERA_INDEX,
        width: int = config.DEFAULT_CAMERA_WIDTH,
        height: int = config.DEFAULT_CAMERA_HEIGHT,
        target_fps: int = config.DEFAULT_TARGET_FPS,
    ) -> None:
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.target_fps = target_fps

        self._cap: cv2.VideoCapture | None = None
        self._frame: np.ndarray | None = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._opened = False
        self.last_error: str | None = None
        self.opened_index: int | None = None
        self.opened_backend: str | None = None

    # ------------------------------------------------------------------ #
    def _try_open(self, index: int, backend: int, backend_name: str) -> bool:
        cap = cv2.VideoCapture(index, backend)
        if not cap.isOpened():
            cap.release()
            return False

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.target_fps)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # isOpened() can lie (esp. DSHOW) — only trust a real frame read.
        ok, frame = cap.read()
        if not ok or frame is None:
            cap.release()
            return False

        self._cap = cap
        self.opened_index = index
        self.opened_backend = backend_name
        return True

    def start(self) -> bool:
        """
        Tries the preferred backend at the requested index first, then
        falls back across a small matrix of (backend, index) combos —
        this covers the most common Windows/Linux/Mac quirks (wrong
        backend, wrong index, camera claimed by another app, etc).
        """
        attempts = [(_PREFERRED_BACKEND, self.camera_index, _backend_name(_PREFERRED_BACKEND))]
        for backend, name in _FALLBACK_BACKENDS:
            for idx in _fallback_indices(self.camera_index):
                attempts.append((backend, idx, name))

        for backend, idx, name in attempts:
            try:
                if self._try_open(idx, backend, name):
                    self._opened = True
                    self.last_error = None
                    self._stop_event.clear()
                    self._thread = threading.Thread(target=self._update_loop, daemon=True)
                    self._thread.start()
                    logger.info("Camera opened: index=%s backend=%s", idx, name)
                    return True
            except Exception as exc:  # noqa: BLE001
                logger.warning("Camera open attempt failed (index=%s, backend=%s): %s", idx, name, exc)

        self._opened = False
        self.last_error = (
            "No working webcam found after trying multiple backends/indices. "
            "The camera may be in use by another app (Zoom/Teams/Camera app), "
            "disabled in Windows privacy settings, or not connected."
        )
        logger.error(self.last_error)
        return False

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=1.0)
        if self._cap is not None:
            self._cap.release()
        self._opened = False

    @property
    def is_running(self) -> bool:
        return self._opened and not self._stop_event.is_set()

    # ------------------------------------------------------------------ #
    def _update_loop(self) -> None:
        min_frame_time = 1.0 / max(self.target_fps, 1)
        while not self._stop_event.is_set():
            t0 = time.perf_counter()
            ok, frame = self._cap.read()
            if ok:
                frame = cv2.flip(frame, 1)  # mirror, feels natural on webcam
                with self._lock:
                    self._frame = frame
            else:
                time.sleep(0.01)
                continue

            elapsed = time.perf_counter() - t0
            sleep_left = min_frame_time - elapsed
            if sleep_left > 0:
                time.sleep(sleep_left)

    def read(self) -> np.ndarray | None:
        with self._lock:
            return None if self._frame is None else self._frame.copy()


class FaceDetector:
    """Thin wrapper around MediaPipe's fast, CPU-friendly face detector."""

    def __init__(self, min_confidence: float = config.MIN_FACE_DETECTION_CONFIDENCE) -> None:
        import mediapipe as mp

        self._mp_face = mp.solutions.face_detection
        self._detector = self._mp_face.FaceDetection(
            model_selection=0, min_detection_confidence=min_confidence
        )

    def detect(self, frame_bgr: np.ndarray) -> list[FaceBox]:
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        result = self._detector.process(rgb)

        boxes: list[FaceBox] = []
        if not result.detections:
            return boxes

        for det in result.detections:
            rel = det.location_data.relative_bounding_box
            x = max(int(rel.xmin * w), 0)
            y = max(int(rel.ymin * h), 0)
            bw = min(int(rel.width * w), w - x)
            bh = min(int(rel.height * h), h - y)
            if bw <= 0 or bh <= 0:
                continue
            conf = det.score[0] if det.score else 0.0
            boxes.append(FaceBox(x, y, bw, bh, conf))

        # Largest face first (most likely the primary subject).
        boxes.sort(key=lambda b: b.w * b.h, reverse=True)
        return boxes

    def close(self) -> None:
        self._detector.close()


def crop_face_for_model(frame_bgr: np.ndarray, box: FaceBox) -> np.ndarray:
    """
    Crops, grayscales, resizes, and lighting-normalizes a face region to
    the CNN's input size. Histogram equalization compensates for webcam
    lighting being very different from FER2013's normalized training
    photos — this must match the same step in train_model.py, so if you
    change this, retrain the model afterwards.
    """
    crop = frame_bgr[box.y : box.y + box.h, box.x : box.x + box.w]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (config.FACE_IMG_SIZE, config.FACE_IMG_SIZE), interpolation=cv2.INTER_AREA)
    equalized = cv2.equalizeHist(resized)
    return equalized


def crop_face_color(frame_bgr: np.ndarray, box: FaceBox, size: int = config.TRANSFER_IMG_SIZE) -> np.ndarray:
    """
    Crops and resizes a face region to a square RGB image, for the
    MobileNetV2 transfer-learning pipeline (collect_faces.py /
    train_transfer_model.py). No grayscale/equalization — the
    pretrained ImageNet backbone expects normal color images; exact
    normalization (MobileNetV2's preprocess_input) happens in
    emotion_model.py at prediction time, matching training.
    """
    crop = frame_bgr[box.y : box.y + box.h, box.x : box.x + box.w]
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (size, size), interpolation=cv2.INTER_AREA)
    return resized


def draw_annotations(
    frame_bgr: np.ndarray,
    box: FaceBox,
    label: str | None,
    confidence: float | None,
) -> np.ndarray:
    """Draws the blue bounding box + emotion/confidence label onto the frame."""
    blue = (255, 197, 0)  # BGR — a bright cyan-blue
    x, y, w, h = box.x, box.y, box.w, box.h
    cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), blue, 2, cv2.LINE_AA)

    if label is not None and confidence is not None:
        text = f"{label} ({confidence * 100:.0f}%)"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame_bgr, (x, y - th - 14), (x + tw + 10, y), blue, -1, cv2.LINE_AA)
        cv2.putText(
            frame_bgr, text, (x + 5, y - 6),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (10, 10, 10), 2, cv2.LINE_AA,
        )
    return frame_bgr