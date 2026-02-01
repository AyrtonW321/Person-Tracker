# Import Libraries
import cv2 as cv
import config

from distance.estimator import DistanceEstimator
from vision.camera import Camera
from vision.colour_tracker import ColourTracker
from ui.overlay import draw_crosshair, draw_tracking_overlay

# Try to load servo controller only if enabled
PanTiltController = None
if config.USE_SERVO:
    try:
        from servo.controller import PanTiltController
    except Exception as e:
        print("[WARN] Servo controller failed to import:", e)
        PanTiltController = None

# Loads whichever object you are trying to track
PersonTracker = None
if config.TRACK_MODE == "person":
    from vision.person_tracker import PersonTracker

# Main function
def main():
    # Initialize the camera
    camera = Camera()
    
    # Changing the tracking modes (config.py)
    if config.TRACK_MODE == "person":
        tracker = PersonTracker()
    else:
        tracker = ColourTracker()

    # Initialize the distance estimator
    dist_est = DistanceEstimator()

    # Initilize the servo motors if being used
    controller = None
    if config.USE_SERVO and PanTiltController is not None:
        controller = PanTiltController()

    # The operating loop
    try:
        while True:
            # Initialize the frame for the output
            frame = camera.read()
            # Outputs what the camera is looking at
            result = tracker.process(frame)

            # Distance from bbox width (requires calibration)
            distance_cm = None
            if result["found"] and result["bbox"] is not None:
                x, y, w, h = result["bbox"]
                distance_cm = dist_est.estimate_cm(w)

            result["distance_cm"] = distance_cm

            # Camera mask
            mask = result["mask"]

            # Draw the crosshair and the tracking overlay
            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            # Direct servo control
            if controller is not None and result["found"]:
                error_x, error_y = result["error"]
                controller.update(error_x, error_y)

            # Display the video and the mask
            cv.imshow("Video", frame)
            cv.imshow("Mask", mask)

            # Sees if there are any inputs from the keyboard
            key = cv.waitKey(1) & 0xFF

            # Turns on the distance calculator
            if key == ord("c"):
                # Calibrate focal length using current bbox width
                if result["found"] and result["bbox"] is not None:
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

# import cv2 as cv
# import config
# from vision.camera import Camera
# from vision.person_tracker import PersonTracker
# from ui.overlay import draw_crosshair, draw_tracking_overlay


# def main():
#     camera = Camera()
#     tracker = PersonTracker()

#     try:
#         while True:
#             frame = camera.read()

#             result, debug = tracker.process(frame)

#             # Draw overlays on the debug frame
#             draw_crosshair(debug)
#             draw_tracking_overlay(debug, result)

#             cv.imshow("Video", debug)

#             if cv.waitKey(1) & 0xFF == ord("q"):
#                 break

#     finally:
#         camera.close()
#         cv.destroyAllWindows()


# if __name__ == "__main__":
#     main()

