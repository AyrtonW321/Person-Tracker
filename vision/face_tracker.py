# vision/face_tracker.py
import cv2 as cv
import config

class FaceTracker:
    def __init__(self):
        self.deadband_px = config.DEADBAND_PX

        # Use OpenCV's built-in Haar cascade automatically.
        # This avoids hardcoded /usr/share/... paths that often don't exist.
        cascade_path = getattr(config, "FACE_CASCADE_PATH", None)
        if not cascade_path:
            cascade_path = cv.data.haarcascades + "haarcascade_frontalface_default.xml"

        self.face_cascade = cv.CascadeClassifier(cascade_path)

        # If the cascade fails to load, give a useful message
        if self.face_cascade.empty():
            raise RuntimeError(
                f"Failed to load Haar face cascade.\n"
                f"Tried path: {cascade_path}\n"
                f"Tip: install opencv-data or use cv.data.haarcascades."
            )

    def process(self, frame_bgr):
        H, W = frame_bgr.shape[:2]

        gray = cv.cvtColor(frame_bgr, cv.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        result = {
            "found": False,
            "bbox": None,
            "center": None,
            "raw_center": None,
            "error": None,
            "area": 0,
            "mask": None,
        }

        if len(faces) == 0:
            return result

        # Choose largest detected face
        x, y, w, h = max(faces, key=lambda r: r[2] * r[3])

        cx = x + w // 2
        cy = y + h // 2

        error_x = cx - (W // 2)
        error_y = cy - (H // 2)

        if abs(error_x) < self.deadband_px:
            error_x = 0
        if abs(error_y) < self.deadband_px:
            error_y = 0

        result.update({
            "found": True,
            "bbox": (int(x), int(y), int(w), int(h)),
            "center": (int(cx), int(cy)),
            "raw_center": (int(cx), int(cy)),
            "error": (int(error_x), int(error_y)),
            "area": int(w * h),
        })

        return result
