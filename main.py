import cv2 as cv
import config

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


def main():
    camera = Camera()
    tracker = ColourTracker()

    controller = None
    if config.USE_SERVO and PanTiltController is not None:
        try:
            controller = PanTiltController()
            print("[INFO] Servo controller started")
        except Exception as e:
            print("[WARN] Servo controller failed to start:", e)
            controller = None

    try:
        while True:
            frame = camera.read()

            # ColourTracker returns a dict (includes mask)
            result = tracker.process(frame)
            mask = result["mask"]

            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            # Direct servo control (no lock/hold)
            if controller is not None and result["found"]:
                error_x, error_y = result["error"]
                controller.update(error_x, error_y)

            cv.imshow("Video", frame)
            cv.imshow("Mask", mask)

            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.close()
        if controller is not None:
            controller.close()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
