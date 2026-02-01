from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480)}
)
picam2.configure(config)
picam2.start()

printed = False

while True:
    frame = picam2.capture_array()

    if not printed:
        print("frame.shape =", frame.shape)
        print("frame.dtype  =", frame.dtype)
        printed = True

    # Convert depending on channels
    if len(frame.shape) == 3 and frame.shape[2] == 4:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    else:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    cv2.imshow("Camera Preview", frame_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows() 
picam2.stop()