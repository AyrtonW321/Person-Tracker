# servo/controller.py
import time
import pigpio
import config
from servo.servos import Servo


def clamp(v, vmin, vmax):
    return max(vmin, min(vmax, v))


class PanTiltController:
    """
    Mid-level control: error -> servo pulse width updates (pigpio).
    """

    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpio daemon not running (start with: sudo systemctl start pigpiod)")

        self.pan = Servo(
            pi=self.pi,
            pin=config.PAN_PIN,
            us_min=config.PAN_US_MIN,
            us_max=config.PAN_US_MAX,
            us_center=config.PAN_US_CENTER,
        )

        self.tilt = Servo(
            pi=self.pi,
            pin=config.TILT_PIN,
            us_min=config.TILT_US_MIN,
            us_max=config.TILT_US_MAX,
            us_center=config.TILT_US_CENTER,
        )

        self._last_update = 0.0

    def update(self, error_x: int, error_y: int):
        now = time.time()
        if now - self._last_update < config.SERVO_UPDATE_S:
            return
        self._last_update = now

        if error_x == 0 and error_y == 0:
            return

        # Convert pixel error -> microsecond delta (proportional)
        d_pan = config.SERVO_KP_PAN * error_x
        d_tilt = config.SERVO_KP_TILT * error_y

        # Cap per update
        d_pan = clamp(d_pan, -config.SERVO_MAX_STEP_US, config.SERVO_MAX_STEP_US)
        d_tilt = clamp(d_tilt, -config.SERVO_MAX_STEP_US, config.SERVO_MAX_STEP_US)

        if config.PAN_INVERT:
            d_pan = -d_pan
        if config.TILT_INVERT:
            d_tilt = -d_tilt

        # Apply: subtracting generally moves toward reducing error
        self.pan.set_us(self.pan.us - int(d_pan))
        self.tilt.set_us(self.tilt.us - int(d_tilt))

    def close(self):
        self.pan.stop()
        self.tilt.stop()
        self.pi.stop()
