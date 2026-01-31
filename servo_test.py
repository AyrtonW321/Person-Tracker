import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PAN = 18
TILT = 13

GPIO.setup(PAN, GPIO.OUT)
GPIO.setup(TILT, GPIO.OUT)

pan = GPIO.PWM(PAN, 50)
tilt = GPIO.PWM(TILT, 50)

try:
    pan.start(0)
    tilt.start(0)

    # move a bit
    pan.ChangeDutyCycle(7.2)
    tilt.ChangeDutyCycle(7.2)
    time.sleep(1)

    pan.ChangeDutyCycle(0)
    tilt.ChangeDutyCycle(0)
    time.sleep(1)

finally:
    # IMPORTANT: stop PWM objects first
    try:
        pan.stop()
    except Exception:
        pass
    try:
        tilt.stop()
    except Exception:
        pass

    # THEN cleanup
    GPIO.cleanup()

    # extra: drop references so __del__ won't try to stop again later
    pan = None
    tilt = None
