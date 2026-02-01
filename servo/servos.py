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

class Servo:
    def __init__(self, pin, min_dc, max_dc, center_dc, freq=None):
        if GPIO is None:
            raise RuntimeError("RPi.GPIO not available (run on Raspberry Pi).")

        self.pin = pin
        self.freq = config.SERVO_FREQ if freq is None else freq

        self.min_dc = min_dc
        self.max_dc = max_dc
        self.dc = center_dc

        # GPIO mode should be set once; safe to call multiple times
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(0)

        self.set_duty(center_dc)

    def set_duty(self, duty):
        self.dc = clamp(duty, self.min_dc, self.max_dc)
        self.pwm.ChangeDutyCycle(self.dc)

    def stop(self):
        self.pwm.stop()