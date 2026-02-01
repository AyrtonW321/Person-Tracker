# vision/face_tracker.py
import cv2 as cv
import numpy as np
import config


class FaceTracker:
    """
    Face-only detector.
    Returns a result dict compatible with your current pipeline:
      {
        "found": bool,
        "bbox": (x,y,w,h) or None,
        "center": (cx,cy) or None,
        "raw_center": (rcx, rcy) or None,
        "error": (error_x, error_y) or None,
        "area": int,
        "mask": uint8 mask (for display/debug),
      }
    """

    def __init__(self, cascade_path=None):
        # Use OpenCV's default haarcascade path if none is provided
        if cascade_path is None:
            cascade_path = cv.data.haarcascades + "haarcascade_frontalface_default.xml"

        self.face_cascade = cv.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            raise RuntimeError(f"Failed to load Haar cascade at: {cascade_path}")

        # Reuse your config tuning knobs
        self.min_area = getattr(config, "MIN_AREA", 1000)
        self.deadband_px = getattr(config, "DEADBAND_PX", 0)

        self.center_alpha = getattr(config, "CENTER_SMOOTH_ALPHA", 1.0)
        self.error_alpha = getattr(config, "ERROR_SMOOTH_ALPHA", 1.0)

        self._smoothed_center = None  # (sx, sy)
        self._smoothed_error = None   # (ex, ey)

    def _ema2(self, prev_xy, new_xy, alpha):
        """2D exponential moving average."""
        if prev_xy is None:
            return (float(new_xy[0]), float(new_xy[1]))
        px, py = prev_xy
        nx, ny = new_xy
        sx = (1 - alpha) * px + alpha * nx
        sy = (1 - alpha) * py + alpha * ny
        return (sx, sy)

    def process(self, frame_bgr):
        H, W = frame_bgr.shape[:2]

        # Grayscale is standard for Haar cascades
        gray = cv.cvtColor(frame_bgr, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),   # raise if you want fewer tiny false positives
            flags=cv.CASCADE_SCALE_IMAGE
        )

        # Build a "mask" for debugging (like your colour mask window)
        mask = np.zeros((H, W), dtype=np.uint8)

        result = {
            "found": False,
            "bbox": None,
            "center": None,
            "raw_center": None,
            "error": None,
            "area": 0,
            "mask": mask,
        }

        if len(faces) == 0:
            self._smoothed_center = None
            self._smoothed_error = None
            return result

        # Choose the largest detected face
        x, y, w, h = max(faces, key=lambda b: b[2] * b[3])
        area = int(w * h)
        result["area"] = area

        if area < self.min_area:
            self._smoothed_center = None
            self._smoothed_error = None
            return result

        # Fill mask for visualization
        mask[y:y+h, x:x+w] = 255

        # Center of face bbox
        raw_cx = x + w // 2
        raw_cy = y + h // 2

        # Smoothed center (for servo stability)
        sm_cx, sm_cy = self._ema2(self._smoothed_center, (raw_cx, raw_cy), self.center_alpha)
        self._smoothed_center = (sm_cx, sm_cy)

        cx, cy = int(sm_cx), int(sm_cy)

        # Error from frame center
        error_x = cx - (W // 2)
        error_y = cy - (H // 2)

        sm_ex, sm_ey = self._ema2(self._smoothed_error, (error_x, error_y), self.error_alpha)
        self._smoothed_error = (sm_ex, sm_ey)

        error_x, error_y = int(sm_ex), int(sm_ey)

        # Deadband AFTER smoothing
        if abs(error_x) < self.deadband_px:
            error_x = 0
        if abs(error_y) < self.deadband_px:
            error_y = 0

        result.update({
            "found": True,
            "bbox": (int(x), int(y), int(w), int(h)),
            "center": (cx, cy),
            "raw_center": (raw_cx, raw_cy),
            "error": (error_x, error_y),
            "mask": mask,
        })

        return result
