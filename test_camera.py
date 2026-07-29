"""
test_camera.py
===============
Standalone webcam diagnostic — completely bypasses Streamlit/threading so
you can see exactly what OpenCV sees. Run this directly from the terminal:

    python test_camera.py

It tries every backend/index combo Emotica AI would try, reports which
ones work, and opens a plain OpenCV window showing the live feed for the
first working combo. Press 'q' to close the window.
"""

from __future__ import annotations

import platform

import cv2

BACKENDS = (
    [(cv2.CAP_DSHOW, "DSHOW"), (cv2.CAP_MSMF, "MSMF"), (cv2.CAP_ANY, "ANY")]
    if platform.system() == "Windows"
    else [(cv2.CAP_ANY, "ANY")]
)
INDICES = [0, 1, 2]


def main() -> None:
    print(f"OpenCV version: {cv2.__version__}")
    print(f"Platform: {platform.system()}")
    print("Scanning for a working camera (backend, index) combination...\n")

    working: list[tuple[int, str, int]] = []

    for backend, name in BACKENDS:
        for idx in INDICES:
            cap = cv2.VideoCapture(idx, backend)
            opened = cap.isOpened()
            frame_ok = False
            if opened:
                ok, frame = cap.read()
                frame_ok = ok and frame is not None
            cap.release()

            status = "OK (frame read)" if frame_ok else ("opened but no frame" if opened else "failed")
            print(f"  backend={name:6s} index={idx}  ->  {status}")
            if frame_ok:
                working.append((backend, name, idx))

    if not working:
        print(
            "\nNo backend/index combination could open the camera.\n"
            "Most likely causes:\n"
            "  - Another app (Zoom/Teams/Camera app/browser tab) is using the webcam.\n"
            "  - Windows Settings -> Privacy & security -> Camera -> "
            "'Let desktop apps access your camera' is OFF.\n"
            "  - No physical webcam connected, or a driver issue.\n"
        )
        return

    backend, name, idx = working[0]
    print(f"\nUsing backend={name}, index={idx}. Opening live preview window...")
    print("Press 'q' in the video window to quit.\n")

    cap = cv2.VideoCapture(idx, backend)
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Frame read failed mid-stream.")
            break
        cv2.imshow("Emotica AI - Camera Test (press q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()