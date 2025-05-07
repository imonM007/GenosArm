import cv2
import numpy as np
import math
import serial
import time

try:
    arduino = serial.Serial('COM3', 9600)  # Update COM port if needed
    time.sleep(2)  # Wait for Arduino to be ready
    print("Arduino connected.")
except Exception as e:
    print("Failed to connect to Arduino:", e)
    arduino = None

# === Arm Constants (adjust as needed) ===
L1 = 1000  # base to joint2
L2 = 2500  # joint2 to joint3
L3 = 2500  # joint2 to joint3
L4 = 1000  # joint3 to joint4
L5 = L2 + L3  # max reach

# === Start Camera Capture ===
cap1 = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(1)

# Red HSV range
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# === Function to compute angles ===
def compute_angles(X, Y, Z):
    try:
        J1 = math.degrees(math.atan2(Y, X))
        D0 = math.sqrt(X ** 2 + Y ** 2)
        D1 = math.sqrt(D0 ** 2 + Z ** 2)
        phi1 = math.degrees(math.atan(Z / D0))
        phi2 = 90 - phi1
        D2 = math.sqrt(L1 ** 2 + D1 ** 2 - 2 * L1 * D1 * math.cos(math.radians(phi2)))
        phi3 = math.degrees(math.acos((L1 ** 2 + D2 ** 2 - D1 ** 2) / (2 * L1 * D2)))
        phi4 = 180 - phi2 - phi3
        D3 = math.sqrt(D2 ** 2 + L4 ** 2 - 2 * L4 * D2 * math.cos(math.radians(phi3)))

        if D3 > L5 or (L2 > D3 + L3) or (L3 > D3 + L2):
            print('Object is out of range.')
        else:
            phi5 = math.degrees(math.acos((D2 ** 2 + D3 ** 2 - L4 ** 2) / (2 * D2 * D3)))
            phi6 = math.degrees(math.acos((D3 ** 2 + L2 ** 2 - L3 ** 2) / (2 * L2 * D3)))
            phi7 = 180 - (2 * phi6)
            J2 = 180 - phi3 - phi5 - phi6  # Revolution of joint 2 from Z-axis on XZ plane

            phi8 = phi7 - J2
            J3 = 180 - phi8  # Revolution of joint 3 from Z-axis on XZ plane

            J4 = 180  # Revolution of joint 4 from Z-axis is always 180 degrees

        return round(J1), round(J2), round(J3), round(J4)
    except Exception as e:
        print("Angle computation error:", e)
        return None

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if not ret1 or not ret2:
        print("Camera error.")
        break

    center1, center2 = None, None

    # Detect red in camera 1
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv1, lower_red1, upper_red1) | cv2.inRange(hsv1, lower_red2, upper_red2)
    contours1, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours1:
        largest = max(contours1, key=cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            (x1, y1), r1 = cv2.minEnclosingCircle(largest)
            center1 = (int(x1), int(y1))
            cv2.circle(frame1, center1, int(r1), (0, 255, 0), 2)

    # Detect red in camera 2
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask2 = cv2.inRange(hsv2, lower_red1, upper_red1) | cv2.inRange(hsv2, lower_red2, upper_red2)
    contours2, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours2:
        largest = max(contours2, key=cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            (x2, y2), r2 = cv2.minEnclosingCircle(largest)
            center2 = (int(x2), int(y2))
            cv2.circle(frame2, center2, int(r2), (0, 255, 0), 2)

    # 3D position and angles
    if center1 and center2:
        X, Y, Z = center1[0], center1[1], center2[1]
        print(f"Ball at: X={X}, Y={Y}, Z={Z}")

        angles = compute_angles(X, Y, Z)
        if angles:
            J1, J2, J3, J4 = angles
            print(f"Sending Angles → J1={J1}, J2={J2}, J3={J3}, J4={J4}")
            if arduino:
                arduino.write(f"{J1},{J2},{J3},{J4}\n".encode())

    # Show both cameras
    cv2.imshow("Camera 1", frame1)
    cv2.imshow("Camera 2", frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap1.release()
cap2.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
