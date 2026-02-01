import time
import config
from servo.servos import Servo

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


def clamp(v, vmin, vmax):
    return max(vmin, min(vmax, v))


class PanTiltController:
    def __init__(self):
        if GPIO is None:
            raise RuntimeError("RPi.GPIO not available (run on Raspberry Pi).")

        self.pan = Servo(
            pin=config.PAN_PIN,
            min_dc=config.PAN_MIN,
            max_dc=config.PAN_MAX,
            center_dc=config.PAN_CENTER,
            freq=config.SERVO_FREQ,
        )

        self.tilt = Servo(
            pin=config.TILT_PIN,
            min_dc=config.TILT_MIN,
            max_dc=config.TILT_MAX,
            center_dc=config.TILT_CENTER,
            freq=config.SERVO_FREQ,
        )

        self._last_update = 0.0

    def update(self, error_x, error_y):
        now = time.time()
        if now - self._last_update < config.SERVO_UPDATE_S:
            return
        self._last_update = now

        # Proportional control: delta duty proportional to pixel error
        d_pan = clamp(config.SERVO_KP_PAN * error_x, -config.SERVO_MAX_STEP, config.SERVO_MAX_STEP)
        d_tilt = clamp(config.SERVO_KP_TILT * error_y, -config.SERVO_MAX_STEP, config.SERVO_MAX_STEP)

        # NOTE: If motion is reversed, flip the sign on that axis here.
        self.pan.set_duty(self.pan.dc - d_pan)
        self.tilt.set_duty(self.tilt.dc - d_tilt)

    def close(self):
        self.pan.stop()
        self.tilt.stop()
        GPIO.cleanup()