import cv2 as cv
import config


class PersonTracker:
    """
    HOG-based person detector.
    Returns: (result_dict, debug_frame)
    """

    def __init__(self):
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

        # Person-specific knobs
        self.min_area = getattr(config, "PERSON_MIN_AREA", 2500)
        self.deadband_px = getattr(config, "PERSON_DEADBAND_PX", 10)

        self.win_stride = getattr(config, "PERSON_WIN_STRIDE", (8, 8))
        self.padding = getattr(config, "PERSON_PADDING", (8, 8))
        self.scale = getattr(config, "PERSON_SCALE", 1.05)

        self.min_weight = getattr(config, "PERSON_MIN_WEIGHT", 0.6)

        # Speed boost
        self.detect_width = getattr(config, "PERSON_DETECT_WIDTH", 640)

    def process(self, frame_bgr):
        H0, W0 = frame_bgr.shape[:2]
        debug = frame_bgr.copy()

        # Standardized result schema (matches ColourTracker-style expectations)
        result = {
            "found": False,
            "bbox": None,
            "center": None,
            "raw_center": None,
            "error": None,
            "area": 0,
            "mask": None,          # usually no mask for person
            "distance_cm": None,
            "label": "person",
            "weight": 0.0,
        }

        # Optional resize for faster detection
        scale_factor = 1.0
        det_frame = frame_bgr

        if self.detect_width is not None and W0 > self.detect_width:
            scale_factor = self.detect_width / float(W0)
            new_h = int(H0 * scale_factor)
            det_frame = cv.resize(frame_bgr, (self.detect_width, new_h), interpolation=cv.INTER_LINEAR)

        rects, weights = self.hog.detectMultiScale(
            det_frame,
            winStride=self.win_stride,
            padding=self.padding,
            scale=self.scale
        )

        if rects is None or len(rects) == 0:
            return result, debug

        # Scale rects back up to original frame size
        if scale_factor != 1.0:
            rects = [
                (int(x / scale_factor), int(y / scale_factor), int(w / scale_factor), int(h / scale_factor))
                for (x, y, w, h) in rects
            ]

        # Filter candidates
        candidates = []
        for (x, y, w, h), weight in zip(rects, weights):
            weight = float(weight)
            if weight < self.min_weight:
                continue

            area = int(w * h)
            if area < self.min_area:
                continue

            candidates.append((x, y, w, h, weight, area))

        if not candidates:
            return result, debug

        # Pick biggest area
        x, y, w, h, weight, area = max(candidates, key=lambda it: it[5])

        # Center and error
        cx = x + (w // 2)
        cy = y + (h // 2)

        frame_cx = W0 // 2
        frame_cy = H0 // 2

        error_x = cx - frame_cx
        error_y = cy - frame_cy

        # Deadband
        if abs(error_x) < self.deadband_px:
            error_x = 0
        if abs(error_y) < self.deadband_px:
            error_y = 0

        result.update({
            "found": True,
            "bbox": (int(x), int(y), int(w), int(h)),
            "center": (int(cx), int(cy)),
            "raw_center": (int(cx), int(cy)),      # person tracker typically has no separate raw
            "error": (int(error_x), int(error_y)),
            "area": int(area),
            "label": "person",
            "weight": float(weight),               # confidence if you have it
        })


        # Draw debug overlay
        cv.rectangle(debug, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.circle(debug, (cx, cy), 6, (255, 0, 0), -1)

        cv.putText(
            debug,
            f"person w={weight:.2f} area={area}",
            (x, max(0, y - 10)),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        return result, debug
