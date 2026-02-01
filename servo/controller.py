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

        self.tilt = None
        if config.TILT_PIN is not None:
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

        if error_x == 0 and error_y == 0:
            return

        d_pan = clamp(
            config.SERVO_KP_PAN * error_x,
            -config.SERVO_MAX_STEP,
            config.SERVO_MAX_STEP
        )
        d_tilt = clamp(
            config.SERVO_KP_TILT * error_y,
            -config.SERVO_MAX_STEP,
            config.SERVO_MAX_STEP
        )

        # Direction flip toggles
        if config.PAN_INVERT:
            d_pan = -d_pan
        if config.TILT_INVERT:
            d_tilt = -d_tilt

        # Apply (sign here is consistent with “move to reduce error”)
        self.pan.set_duty(self.pan.dc - d_pan)
        if self.tilt is not None:
            self.tilt.set_duty(self.tilt.dc - d_tilt)

    def close(self):
        self.pan.stop()
        if self.tilt is not None:
            self.tilt.stop()
        GPIO.cleanup()
