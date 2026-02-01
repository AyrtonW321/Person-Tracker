# main.py
import cv2 as cv
import config

from distance.estimator import DistanceEstimator
from vision.camera import Camera
from ui.overlay import draw_crosshair, draw_tracking_overlay
from vision.tracker import make_tracker

# Try to load servo controller only if enabled
PanTiltController = None
if config.USE_SERVO:
    try:
        from servo.controller import PanTiltController
    except Exception:
        PanTiltController = None


def main():
    camera = Camera()
    dist_est = DistanceEstimator()

    # Tracker is selected ONCE from config
    tracker = make_tracker(getattr(config, "TRACK_MODE", "colour"))

    controller = None
    if config.USE_SERVO and PanTiltController is not None:
        try:
            controller = PanTiltController()
        except Exception:
            controller = None

    try:
        while True:
            frame = camera.read()

            # Always get a dict result from the tracker
            result = tracker.process(frame)

            # Distance from bbox width (always, when found)
            result["distance_cm"] = None
            bbox = result.get("bbox")
            if result.get("found") and isinstance(bbox, (tuple, list)) and len(bbox) == 4:
                w = int(bbox[2])
                result["distance_cm"] = dist_est.estimate_cm(w)

            # Servo control
            if controller is not None and result.get("found") and result.get("error"):
                error_x, error_y = result["error"]
                controller.update(error_x, error_y)

            # Draw overlays + display
            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            cv.imshow("Video", frame)
            if result.get("mask") is not None:
                cv.imshow("Mask", result["mask"])

            # Keys: calibrate + quit only
            key = cv.waitKey(1) & 0xFF

            if key == ord("c"):
                if result.get("found") and isinstance(bbox, (tuple, list)) and len(bbox) == 4:
                    w = int(bbox[2])
                    dist_est.calibrate(w)

            elif key == ord("q"):
                break

    finally:
        camera.close()
        if controller is not None:
            controller.close()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
