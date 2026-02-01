import cv2 as cv
import numpy as np
import config


class ColorTracker:
    def __init__(self, active_colors=None):
        """
        active_colors: list of color keys from config.COLOR_RANGES
                       Example: ["cb132b_red"] or ["cb132b_red", "blue"]
                       If None, uses config.ACTIVE_COLORS
        """
        self.active_colors = active_colors or config.ACTIVE_COLORS

        self.color_ranges = config.COLOR_RANGES  # dict: color_name -> list[(lower, upper)]

        self.min_area = config.MIN_AREA
        self.deadband_px = config.DEADBAND_PX

    def _build_mask(self, hsv):
        """
        Builds a combined mask for all active colors.
        Each color may contain multiple HSV ranges.
        """
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        for color_name in self.active_colors:
            ranges = self.color_ranges.get(color_name, [])
            for lower, upper in ranges:
                mask = cv.bitwise_or(mask, cv.inRange(hsv, lower, upper))

        return mask

    def process(self, frame_bgr):
        H, W = frame_bgr.shape[:2]

        # Optional: blur to reduce speckle noise (helps twitching)
        frame_bgr = cv.GaussianBlur(frame_bgr, (5, 5), 0)

        hsv = cv.cvtColor(frame_bgr, cv.COLOR_BGR2HSV)

        # Build mask from config-selected color(s)
        mask = self._build_mask(hsv)

        # Clean noise (same as your old code)
        mask = cv.erode(mask, None, iterations=1)
        mask = cv.dilate(mask, None, iterations=2)

        # Find contours
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Default result if nothing found
        result = {
            "found": False,
            "bbox": None,        # (x, y, w, h)
            "center": None,      # (cx, cy)
            "error": None,       # (error_x, error_y)
            "area": 0,
            "mask": mask,
        }

        if not contours:
            return result

        c = max(contours, key=cv.contourArea)
        area = cv.contourArea(c)
        result["area"] = int(area)

        if area < self.min_area:
            return result

        x, y, w, h = cv.boundingRect(c)
        cx = x + w // 2
        cy = y + h // 2

        error_x = cx - (W // 2)
        error_y = cy - (H // 2)

        # Deadband to reduce servo jitter later
        if abs(error_x) < self.deadband_px:
            error_x = 0
        if abs(error_y) < self.deadband_px:
            error_y = 0

        result.update({
            "found": True,
            "bbox": (x, y, w, h),
            "center": (cx, cy),
            "error": (error_x, error_y),
        })

        return result