# Import Libraries
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

# Main function
def main():
    # Initialize the camera
    camera = Camera()

    # Initialize the distance estimator
    dist_est = DistanceEstimator()

    # Initilize the servo motors if being used
    controller = None
    if config.USE_SERVO and PanTiltController is not None:
        controller = PanTiltController()

    modes = ["colour", "person", "face"]
    mode_index = modes.index(config.TRACK_MODE) if config.TRACK_MODE in modes else 0
    tracker = make_tracker(modes[mode_index])

    # The operating loop
    try:
        while True:
            # Initialize the frame for the output
            frame = camera.read()
            # Outputs what the camera is looking at
            result = tracker.process(frame)

            # Sees if there are any inputs from the keyboard
            key = cv.waitKey(1) & 0xFF

            if key == ord("1"):
                mode_index = 0
                tracker = make_tracker(modes[mode_index])
            elif key == ord("2"):
                mode_index = 1
                tracker = make_tracker(modes[mode_index])
            elif key == ord("3"):
                mode_index = 2
                tracker = make_tracker(modes[mode_index])

            # Distance from bbox width (requires calibration)
            distance_cm = None
            if result.get("found") and result.get("bbox") is not None:
                x, y, w, h = result["bbox"]
                distance_cm = dist_est.estimate_cm(w)

            result["distance_cm"] = distance_cm

            # Camera mask
            mask = result.get("mask", None)

            # Draw the crosshair and the tracking overlay
            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            # Direct servo control
            if controller is not None and result.get("found"):
                error_x, error_y = result["error"]
                controller.update(error_x, error_y)

            # Display the video and the mask
            cv.imshow("Video", frame)
            if mask is not None:
                cv.imshow("Mask", mask)


            # Turns on the distance calculator
            if key == ord("c"):
                # Calibrate focal length using current bbox width
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

            # Pressing the q button closes the program
            elif key == ord("q"):
                break

    # Break out of the while loop
    finally:
        # Turn off the camera
        camera.close()
        # Turns off the servos
        if controller is not None:
            controller.close()
        # Closes the application windows
        cv.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    main() 