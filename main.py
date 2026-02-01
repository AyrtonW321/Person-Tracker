import cv2 as cv
import time
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


def _point_in_bbox(px, py, bbox):
    x, y, w, h = bbox
    return (x <= px <= x + w) and (y <= py <= y + h)

def main():
    camera = Camera()
    tracker = ColourTracker()

    controller = None
    if config.USE_SERVO and PanTiltController is not None:
        controller = PanTiltController()

    lock_start = None
    hold_until = 0.0

    try:
        while True:
            frame = camera.read()
            result = tracker.process(frame)
            mask = result["mask"]

            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            now = time.time()

            # Decide if we're "locked"
            locked = False
            if result["found"] and result["bbox"] is not None:
                H, W = frame.shape[:2]
                cx_screen, cy_screen = (W // 2, H // 2)

                if _point_in_bbox(cx_screen, cy_screen, result["bbox"]):
                    if lock_start is None:
                        lock_start = now
                    elif (now - lock_start) >= config.LOCK_TIME_S:
                        locked = True
                else:
                    lock_start = None
            else:
                lock_start = None

            # If locked, hold servo updates for HOLD_TIME_S
            if locked and now >= hold_until:
                hold_until = now + config.HOLD_TIME_S

            # Servo updates only when NOT holding
            if controller is not None and result["found"] and now >= hold_until:
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
