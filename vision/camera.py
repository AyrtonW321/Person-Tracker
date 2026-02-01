'''
stars picamera2
capturs frames
convert to rgb
returns frame format for rest of the project
'''
# vision/camera.py
from picamera2 import Picamera2
import cv2 as cv
import config

# Camera Class
class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(
            self.picam2.create_preview_configuration(
                main={"size": config.PREVIEW_SIZE}
            )
        )
        self.picam2.start()

    def read(self):
        frame = self.picam2.capture_array()

        if frame.ndim == 3 and frame.shape[2] == 4:
            return cv.cvtColor(frame, cv.COLOR_RGBA2BGR)
        return cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    def close(self):
        self.picam2.stop()
