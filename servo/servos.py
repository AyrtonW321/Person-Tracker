'''
sets up the pwm output to both servos
angle limits
'''
import config

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


def clamp(v, vmin, vmax):
    return max(vmin, min(vmax, v))


_GPIO_MODE_SET = False


class Servo:
    def __init__(self, pin, min_dc, max_dc, center_dc, freq=None):
        if GPIO is None:
            raise RuntimeError("RPi.GPIO not available (run on Raspberry Pi).")

        global _GPIO_MODE_SET
        if not _GPIO_MODE_SET:
            GPIO.setmode(GPIO.BCM)
            _GPIO_MODE_SET = True

        self.pin = pin
        self.freq = config.SERVO_FREQ if freq is None else freq

        self.min_dc = min_dc
        self.max_dc = max_dc
        self.dc = center_dc

        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(0)

        self.set_duty(center_dc)

    def set_duty(self, duty):
        self.dc = clamp(duty, self.min_dc, self.max_dc)
        self.pwm.ChangeDutyCycle(self.dc)

    def stop(self):
        self.pwm.stop()
