import cv2
import numpy as np
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((7 * 6, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
objpoints = [] 
imgpoints = []
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        frame_with_corners = cv2.drawChessboardCorners(frame, (7, 6), corners2, ret)
        cv2.imshow('Live Calibration', frame_with_corners)
    else:
        cv2.imshow('Live Calibration', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print("Number of object points:", len(objpoints))
print("Number of image points:", len(imgpoints))
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
np.savez(r'C:\Users\Allen\.vscode\tcr\task2\calibrationData.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
print("Calibration complete. Calibration data saved as 'calibrationData.npz'")