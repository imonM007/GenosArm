import cv2
import numpy as np

cap1 = cv2.VideoCapture(2)  # First webcam
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

    center1 = None
    center2 = None

    # Process camera 1
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask1_1 = cv2.inRange(hsv1, lower_red1, upper_red1)
    mask1_2 = cv2.inRange(hsv1, lower_red2, upper_red2)
    mask1 = mask1_1 | mask1_2

    contours1, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours1:
        largest1 = max(contours1, key=cv2.contourArea)
        if cv2.contourArea(largest1) > 500:
            (x1, y1), radius1 = cv2.minEnclosingCircle(largest1)
            center1 = (int(x1), int(y1))
            cv2.circle(frame1, center1, int(radius1), (0, 255, 0), 2)

    # Process camera 2
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask2_1 = cv2.inRange(hsv2, lower_red1, upper_red1)
    mask2_2 = cv2.inRange(hsv2, lower_red2, upper_red2)
    mask2 = mask2_1 | mask2_2

    contours2, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours2:
        largest2 = max(contours2, key=cv2.contourArea)
        if cv2.contourArea(largest2) > 500:
            (x2, y2), radius2 = cv2.minEnclosingCircle(largest2)
            center2 = (int(x2), int(y2))
            cv2.circle(frame2, center2, int(radius2), (0, 255, 0), 2)

    if center1 and center2:
        # Print coordinates in desired format: (x, y, z)
        print(f"(x, y, z) = ({center1[0]}, {center1[1]}, {center2[1]})")

    # Show both frames
    cv2.imshow('Red Ball Tracker - Camera 1', frame1)
    cv2.imshow('Red Ball Tracker - Camera 2', frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release both cameras
cap1.release()
cap2.release()
cv2.destroyAllWindows()
