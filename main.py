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
    except Exception as e:
        print("[WARN] Servo controller failed to import:", e)
        PanTiltController = None


def main():
    camera = Camera()
    dist_est = DistanceEstimator()

    controller = None
    if config.USE_SERVO and PanTiltController is not None:
        try:
            controller = PanTiltController()
        except Exception as e:
            print("[WARN] Servo controller failed to start:", e)
            controller = None

    tracker = None

    try:
        while True:
            frame = camera.read()

            result = {
                "found": False,
                "bbox": None,
                "center": None,
                "raw_center": None,
                "error": None,
                "area": 0,
                "mask": None,
                "distance_cm": None,
                "label": "idle",
                "weight": 0.0,
            }

            # Only process tracking if a tracker is active
            if tracker is not None:
                result = tracker.process(frame)

                # Distance from bbox width
                if result.get("found") and result.get("bbox") is not None:
                    _, _, w, _ = result["bbox"]
                    result["distance_cm"] = dist_est.estimate_cm(w)

                # Servo control
                if controller is not None and result.get("found") and result.get("error"):
                    error_x, error_y = result["error"]
                    controller.update(error_x, error_y)

            # Draw overlays
            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            # Display
            cv.imshow("Video", frame)
            if result.get("mask") is not None:
                cv.imshow("Mask", result["mask"])

            # Keyboard input
            key = cv.waitKey(1) & 0xFF

            # ----- MODE CONTROL -----
            if key == ord("0"):
                tracker = None
                print("[MODE] Idle (no tracking)")

            elif key == ord("1"):
                tracker = make_tracker("colour")
                print("[MODE] Colour tracking")

            elif key == ord("2"):
                tracker = make_tracker("person")
                print("[MODE] Person tracking")

            elif key == ord("3"):
                tracker = make_tracker("face")
                print("[MODE] Face tracking")

            # Calibration
            elif key == ord("c"):
                if result.get("found") and result.get("bbox") is not None:
                    _, _, w, _ = result["bbox"]
                    focal = dist_est.calibrate(w)
                    if focal is not None:
                        print(f"[CALIB] FOCAL_LENGTH_PX = {focal:.2f}")
                        print("[CALIB] Put that value into config.py to persist it.")
                    else:
                        print("[CALIB] Invalid bbox width.")
                else:
                    print("[CALIB] No target detected; can't calibrate.")

            # Quit
            elif key == ord("q"):
                break

    finally:
        camera.close()
        if controller is not None:
            controller.close()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
