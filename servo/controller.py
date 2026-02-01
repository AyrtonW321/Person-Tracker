import time
import config
from servo.servos import Servo

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

class PanTiltController:
    def __init__(self):
        if GPIO is None:
            raise RuntimeError("RPi.GPIO not available (run on Raspberry Pi).")

        self.pan = Servo(config.PAN_PIN, config.PAN_MIN, config.PAN_MAX, config.PAN_CENTER, config.SERVO_FREQ)
        self.tilt = Servo(config.TILT_PIN, config.TILT_MIN, config.TILT_MAX, config.TILT_CENTER, config.SERVO_FREQ)

        self._last_update = 0.0

    def update(self, error_x, error_y):
        now = time.time()
        if now - self._last_update < config.SERVO_UPDATE_S:
            return
        self._last_update = now

        if error_x > 0:
            self.pan.set_duty(self.pan.dc - config.SERVO_STEP)
        elif error_x < 0:
            self.pan.set_duty(self.pan.dc + config.SERVO_STEP)

        if error_y > 0:
            self.tilt.set_duty(self.tilt.dc - config.SERVO_STEP)
        elif error_y < 0:
            self.tilt.set_duty(self.tilt.dc + config.SERVO_STEP)

    def close(self):
        self.pan.stop()
        self.tilt.stop()
        GPIO.cleanup()