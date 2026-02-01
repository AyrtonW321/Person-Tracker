# vision/person_tracker.py
"""
PersonTracker (HOG)

What this file does:
- Uses OpenCV's built-in HOG person detector (pretrained).
- Given a camera frame (BGR), it tries to find people.
- If it finds a person, it returns a result dictionary with:
    - bbox (x, y, w, h)
    - center (cx, cy)
    - error from frame center (error_x, error_y)
    - confidence-ish score (weight)
- If it finds nothing, it returns None.

This is designed to plug into your main loop like your ColourTracker:
    result, debug = tracker.process(frame)
"""

import cv2 as cv
import config


class PersonTracker:
    """
    HOG-based person detector.

    Think of it like:
    - We have a robot "person finder" that looks for human shapes.
    - We run it each frame.
    - We pick the biggest detected person (usually the closest).
    """

    def __init__(self):
        # Create a HOG descriptor object (OpenCV tool for gradient features)
        self.hog = cv.HOGDescriptor()

        # Load OpenCV's built-in pretrained people detector into HOG.
        # This is the "brain" that knows what humans look like (shape patterns).
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

        # Tuning knobs (from config.py)
        self.min_area = getattr(config, "MIN_AREA", 800)
        self.deadband_px = getattr(config, "DEADBAND_PX", 10)

        # HOG detection tuning:
        # - stride: how far the detector moves its window each step (smaller = more accurate, slower)
        # - padding: helps detection at edges
        # - scale: how much the window grows each pass (closer to 1 = more accurate, slower)
        self.win_stride = (8, 8)
        self.padding = (8, 8)
        self.scale = 1.05

        # Optional: If HOG returns many boxes, we can reject weak ones.
        # Higher threshold = fewer false positives, but might miss some people.
        self.min_weight = 0.5

    def process(self, frame_bgr):
        """
        Try to detect a person in the frame.

        Parameters:
            frame_bgr: OpenCV BGR image (numpy array)

        Returns:
            (result, debug_frame)
              - result: dict with bbox/center/errors, or None if no person
              - debug_frame: copy of image with boxes drawn (useful for debugging)
        """

        # Get frame height and width (H, W)
        H, W = frame_bgr.shape[:2]

        # Make a copy for debugging drawings
        debug = frame_bgr.copy()

        # ---- Step 1: Run the HOG detector ----
        # detectMultiScale returns:
        # - rects: list of boxes (x, y, w, h)
        # - weights: list of scores (bigger usually means more confident)
        rects, weights = self.hog.detectMultiScale(
            frame_bgr,
            winStride=self.win_stride,
            padding=self.padding,
            scale=self.scale
        )

        # If nothing was detected, return None
        if rects is None or len(rects) == 0:
            return None, debug

        # ---- Step 2: Filter weak detections (optional but helpful) ----
        # We combine rects + weights into one list, then filter.
        candidates = []
        for (x, y, w, h), weight in zip(rects, weights):
            # Convert weight to a normal Python float (sometimes it's a numpy type)
            weight = float(weight)

            # Reject weak detections
            if weight < self.min_weight:
                continue

            # Compute area (big box means likely closer person)
            area = w * h

            # Reject tiny detections (noise)
            if area < self.min_area:
                continue

            candidates.append((x, y, w, h, weight, area))

        # If after filtering we have nothing, return None
        if not candidates:
            return None, debug

        # ---- Step 3: Pick the best candidate ----
        # Strategy: pick the biggest area detection
        # (closest person usually occupies the most pixels)
        x, y, w, h, weight, area = max(candidates, key=lambda item: item[5])

        # ---- Step 4: Compute center of bounding box ----
        cx = x + (w // 2)
        cy = y + (h // 2)

        # ---- Step 5: Compute error from frame center ----
        # Frame center is (W/2, H/2)
        frame_cx = W // 2
        frame_cy = H // 2

        error_x = cx - frame_cx   # + means target is to the right
        error_y = cy - frame_cy   # + means target is below

        # Deadband: if error is small, treat it as 0 to prevent jitter
        if abs(error_x) < self.deadband_px:
            error_x = 0
        if abs(error_y) < self.deadband_px:
            error_y = 0

        # ---- Step 6: Build result dict (this is what the rest of your app uses) ----
        result = {
            "cx": int(cx),
            "cy": int(cy),
            "error_x": int(error_x),
            "error_y": int(error_y),
            "area": int(area),
            "bbox": (int(x), int(y), int(w), int(h)),
            "frame_center": (int(frame_cx), int(frame_cy)),
            "weight": float(weight),  # confidence-ish score
            "label": "person",
        }

        # ---- Step 7: Draw debug overlay (optional) ----
        # Draw bounding box + center point + weight
        cv.rectangle(debug, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.circle(debug, (cx, cy), 6, (255, 0, 0), -1)

        cv.putText(
            debug,
            f"person w={weight:.2f}",
            (x, max(0, y - 10)),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        return result, debug
