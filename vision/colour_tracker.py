# vision/red_tracker.py
import cv2 as cv
import config


class ColourTracker:
    """
    RED tracker.
    Input: BGR frame
    Output: (result, mask)
      - result: dict or None
      - mask: binary mask (uint8)
    """

    def __init__(self):
        self.lower1 = config.LOWER_RED1
        self.upper1 = config.UPPER_RED1
        self.lower2 = config.LOWER_RED2
        self.upper2 = config.UPPER_RED2

        self.min_area = config.MIN_AREA
        self.deadband_px = config.DEADBAND_PX

    def process(self, frame_bgr):
        H, W = frame_bgr.shape[:2]

        hsv = cv.cvtColor(frame_bgr, cv.COLOR_BGR2HSV)

        mask1 = cv.inRange(hsv, self.lower1, self.upper1)
        mask2 = cv.inRange(hsv, self.lower2, self.upper2)
        mask = cv.bitwise_or(mask1, mask2)

        # Clean noise
        mask = cv.erode(mask, None, iterations=1)
        mask = cv.dilate(mask, None, iterations=2)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None, mask

        c = max(contours, key=cv.contourArea)
        area = cv.contourArea(c)

        if area <= self.min_area:
            return None, mask

        x, y, w, h = cv.boundingRect(c)
        cx = x + w // 2
        cy = y + h // 2

        error_x = cx - (W // 2)
        error_y = cy - (H // 2)

        if abs(error_x) < self.deadband_px:
            error_x = 0
        if abs(error_y) < self.deadband_px:
            error_y = 0

        result = {
            "cx": cx,
            "cy": cy,
            "error_x": error_x,
            "error_y": error_y,
            "area": int(area),
            "bbox": (x, y, w, h),
            "frame_center": (W // 2, H // 2),
        }

        return result, mask