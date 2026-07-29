"""
collect_faces.py
=================
Standalone tool to build your own labeled face dataset for the 4
custom emotions (Angry, Happy, Neutral, Sad) using your webcam. Runs
outside Streamlit (plain OpenCV window) — simpler and more responsive
for a capture workflow.

Captures color 96x96 face crops (data/custom/<Emotion>/*.png) for the
MobileNetV2 transfer-learning pipeline (train_transfer_model.py). If
you have older grayscale 48x48 images from before, delete data/custom/
first and recollect — the two formats can't be mixed in one training
run.

Usage
-----
    python collect_faces.py

Controls (shown on-screen too):
    a / h / n / s   -> select current label (Angry / Happy / Neutral / Sad)
    SPACE           -> capture a 3-second burst (~20 images) for the
                       currently selected label
    q               -> quit

Tips for a good dataset
------------------------
- Aim for at least 150-200 images per emotion (more is better), across
  MULTIPLE separate sittings (different times/lighting/rooms) — bursts
  from a single sitting look too similar to each other and the model
  can end up recognizing the room/lighting instead of the expression.
- Make expressions clearly distinct from each other, especially
  Angry vs. Sad (the two most commonly confused pair):
    * Angry: eyebrows pulled DOWN and IN, jaw/lips tense or pressed,
      eyes narrowed/glaring.
    * Sad: eyebrows raised in the middle (inner corners UP), mouth
      corners drooping, eyes downcast — a softer, "drooping" look.
  Exaggerate a bit more than feels natural — subtle expressions are
  genuinely hard for a small model to tell apart.
- If other people are available (family/friends), have them contribute
  bursts too. A dataset built from only one face will recognize that
  face very well but may generalize poorly to anyone else's face.
"""

from __future__ import annotations

import time
from pathlib import Path

import cv2

import config
from camera import CameraStream, FaceDetector, crop_face_color

KEY_TO_LABEL = {
    ord("a"): "Angry",
    ord("h"): "Happy",
    ord("n"): "Neutral",
    ord("s"): "Sad",
}

BURST_DURATION_SECONDS = 3.0
BURST_CAPTURE_INTERVAL = 0.15  # ~20 images per burst


def count_existing(label: str) -> int:
    folder = config.CUSTOM_DATA_DIR / label
    folder.mkdir(parents=True, exist_ok=True)
    return len(list(folder.glob("*.png")))


def draw_overlay(frame, current_label: str, counts: dict[str, int], status: str) -> None:
    h, w = frame.shape[:2]
    overlay_h = 120
    cv2.rectangle(frame, (0, 0), (w, overlay_h), (20, 15, 10), -1)

    cv2.putText(
        frame, f"Label: {current_label}", (12, 28),
        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 229, 255), 2, cv2.LINE_AA,
    )
    cv2.putText(
        frame, status, (12, 55),
        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA,
    )
    counts_text = "  ".join(f"{lbl}:{counts.get(lbl, 0)}" for lbl in config.EMOTION_LABELS)
    cv2.putText(
        frame, counts_text, (12, 80),
        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150, 220, 150), 1, cv2.LINE_AA,
    )
    cv2.putText(
        frame, "[a]ngry [h]appy [n]eutral [s]ad   SPACE=capture burst   q=quit",
        (12, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180, 180, 180), 1, cv2.LINE_AA,
    )


def main() -> None:
    print("Emotica AI — Custom Dataset Collector")
    print(f"Saving to: {config.CUSTOM_DATA_DIR}\n")

    stream = CameraStream()
    if not stream.start():
        print(f"Could not open camera: {stream.last_error}")
        return

    detector = FaceDetector()
    current_label = "Happy"
    counts = {lbl: count_existing(lbl) for lbl in config.EMOTION_LABELS}
    status = "Ready."

    print("Window opened. Press SPACE to capture a burst, 'q' to quit.")

    try:
        while True:
            frame = stream.read()
            if frame is None:
                time.sleep(0.01)
                continue

            faces = detector.detect(frame)
            display = frame.copy()

            if faces:
                box = faces[0]
                cv2.rectangle(
                    display, (box.x, box.y), (box.x + box.w, box.y + box.h),
                    (255, 197, 0), 2, cv2.LINE_AA,
                )

            draw_overlay(display, current_label, counts, status)
            cv2.imshow("Emotica AI - Dataset Collector (press q to quit)", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key in KEY_TO_LABEL:
                current_label = KEY_TO_LABEL[key]
                status = f"Switched to {current_label}."
            elif key == ord(" "):
                if not faces:
                    status = "No face detected — center your face and try again."
                    continue
                status = f"Capturing burst for {current_label}..."
                folder = config.CUSTOM_DATA_DIR / current_label
                folder.mkdir(parents=True, exist_ok=True)

                burst_start = time.time()
                burst_id = int(burst_start * 1000)
                captured = 0
                while time.time() - burst_start < BURST_DURATION_SECONDS:
                    live_frame = stream.read()
                    if live_frame is None:
                        continue
                    live_faces = detector.detect(live_frame)
                    if live_faces:
                        crop_rgb = crop_face_color(live_frame, live_faces[0], size=config.TRANSFER_IMG_SIZE)
                        crop_bgr = cv2.cvtColor(crop_rgb, cv2.COLOR_RGB2BGR)  # cv2.imwrite expects BGR
                        fname = folder / f"{current_label}_burst{burst_id}_{captured:02d}.png"
                        cv2.imwrite(str(fname), crop_bgr)
                        captured += 1
                        counts[current_label] = counts.get(current_label, 0) + 1

                    preview = live_frame.copy()
                    remaining = BURST_DURATION_SECONDS - (time.time() - burst_start)
                    cv2.putText(
                        preview, f"CAPTURING... hold your expression ({remaining:.1f}s)",
                        (12, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA,
                    )
                    draw_overlay(preview, current_label, counts, status)
                    cv2.imshow("Emotica AI - Dataset Collector (press q to quit)", preview)
                    cv2.waitKey(1)
                    time.sleep(BURST_CAPTURE_INTERVAL)

                status = f"Captured {captured} images for {current_label}."
                print(status)

    finally:
        stream.stop()
        detector.close()
        cv2.destroyAllWindows()

    print("\nFinal counts:")
    for lbl in config.EMOTION_LABELS:
        print(f"  {lbl}: {count_existing(lbl)} images")
    print(f"\nSaved under: {config.CUSTOM_DATA_DIR}")
    print("Once you have enough images (150-200+ per emotion recommended), run:")
    print("  python train_transfer_model.py")


if __name__ == "__main__":
    main()