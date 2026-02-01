import cv2 as cv
import config

from vision.camera import Camera
from vision.colour_tracker import ColourTracker
from ui.overlay import draw_crosshair, draw_tracking_overlay

PanTiltController = None
if config.USE_SERVO:
    try:
        from servo.controller import PanTiltController
    except Exception:
        PanTiltController = None


def main():
    camera = Camera()
    tracker = ColourTracker()

    controller = None
    if config.USE_SERVO and PanTiltController is not None:
        controller = PanTiltController()

    try:
        while True:
            frame = camera.read()          # BGR frame
            result = tracker.process(frame)  # dict result
            mask = result["mask"]

            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

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
