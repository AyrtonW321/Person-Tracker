import cv2
import numpy as np

picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (1280, 960)}
    )
)
picam2.start()

while True:
    frame = picam2.capture_array()        # RGBA
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Start with RED (easy to see)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Clean noise
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > 800:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(
                frame_bgr,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cx = x + w // 2
            cy = y + h // 2

            cv2.circle(
                frame_bgr,
                (cx, cy),
                5,
                (255, 0, 0),
                -1
            )

            print("cx:", cx)

    cv2.imshow("Video", frame_bgr)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()