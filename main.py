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

    modes = ["colour", "person", "face"]
    mode_index = modes.index(config.TRACK_MODE) if config.TRACK_MODE in modes else 0
    tracker = make_tracker(modes[mode_index])

    try:
        while True:
            frame = camera.read()
            result = tracker.process(frame)

            # Distance from bbox width (requires calibration)
            distance_cm = None
            if result.get("found") and result.get("bbox") is not None:
                _, _, w, _ = result["bbox"]
                distance_cm = dist_est.estimate_cm(w)
            result["distance_cm"] = distance_cm

            # Draw overlays
            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            # Servo control
            if controller is not None and result.get("found") and result.get("error") is not None:
                error_x, error_y = result["error"]
                controller.update(error_x, error_y)

            # Display
            cv.imshow("Video", frame)
            mask = result.get("mask")
            if mask is not None:
                cv.imshow("Mask", mask)

            # Keyboard input (handle AFTER showing frames so UI stays responsive)
            key = cv.waitKey(1) & 0xFF

            # Mode switching
            if key == ord("1"):
                mode_index = 0
                tracker = make_tracker(modes[mode_index])
            elif key == ord("2"):
                mode_index = 1
                tracker = make_tracker(modes[mode_index])
            elif key == ord("3"):
                mode_index = 2
                tracker = make_tracker(modes[mode_index])

            # Calibration (press 'c')
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
