import cv2
import numpy as np

cap1 = cv2.VideoCapture(3)  # First webcam
cap2 = cv2.VideoCapture(1)  # Second webcam

# Define lower and upper bounds for red in HSV
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("Failed to grab frame from one of the cameras.")
        break

    for idx, frame in enumerate([frame1, frame2], start=1):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 | mask2

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 500:
                (x, y), radius = cv2.minEnclosingCircle(largest)
                center = (int(x), int(y))
                cv2.circle(frame, center, int(radius), (0, 255, 0), 2)
                print(f"Camera {idx} - Ball center at: {center}")

        cv2.imshow(f'Red Ball Tracker - Camera {idx}', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release both cameras
cap1.release()
cap2.release()
cv2.destroyAllWindows()

