import cv2 as cv

from vision.camera import Camera
from vision.colour_tracker import ColourTracker
from ui.overlay import draw_crosshair, draw_tracking_overlay


def main():
    camera = Camera()
    tracker = ColourTracker()

    try:
        while True:
            frame = camera.read()  # BGR
            result, mask = tracker.process(frame)

            draw_crosshair(frame)
            draw_tracking_overlay(frame, result)

            cv.imshow("Video", frame)
            cv.imshow("Mask", mask)

            if cv.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.close()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()