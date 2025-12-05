import cv2
import numpy as np
from tracker import tracker

# Load haar face detector
face_cascade = cv2.CascadeClassifier("haar_face.xml")

def segment_and_track(frame, c_time, p_time):

    h, w = frame.shape[:2]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 30, 60], dtype=np.uint8)
    upper_hsv = np.array([25, 150, 255], dtype=np.uint8)
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    lower_ycrcb = np.array([0, 135, 85], dtype=np.uint8)
    upper_ycrcb = np.array([255, 180, 135], dtype=np.uint8)
    mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

    mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(80, 80))

    for (fx, fy, fw, fh) in faces:
        pad = 20  # expand a bit
        x1 = max(fx - pad, 0)
        y1 = max(fy - pad, 0)
        x2 = min(fx + fw + pad, w)
        y2 = min(fy + fh + pad, h)

        mask[y1:y2, x1:x2] = 0

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    return tracker(mask, frame.copy(), c_time, p_time)

