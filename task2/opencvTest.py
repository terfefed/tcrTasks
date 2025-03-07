import cv2
import numpy as np
calibration_data = np.load(r'C:\Users\Allen\.vscode\tcr\task2\calibrationData.npz')
mtx = calibration_data['mtx']
dist = calibration_data['dist']
object_radius = 5 
cap = cv2.VideoCapture(0)
lower = np.array([0, 0, 220])
upper = np.array([180, 30, 255])
while True:
    ret, frame = cap.read()
    if not ret:
        break
    undistorted_frame = cv2.undistort(frame, mtx, dist, None, mtx)
    hsv = cv2.cvtColor(undistorted_frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(undistorted_frame, center, radius, (0, 255, 0), 2)
        cv2.circle(undistorted_frame, center, 5, (0, 0, 255), -1)
        depth = (object_radius * mtx[0, 0]) / (2 * radius)
        x_3d, y_3d, z_3d = x, y, depth
        print("Depth (cm):", depth)
        print("3D Coordinates (x, y, z):", (x_3d, y_3d, z_3d))
    cv2.imshow('Ball Detection', undistorted_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()