import cv2
import numpy as np
from tracker import tracker


def segmentation(img, ctime, ptime):
    kernel = np.ones((5,5), np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower = np.array([100, 50, 50])
    upper = np.array([140, 255, 255])

    mask = cv2.inRange(img, lower, upper)
    mask = cv2.dilate(mask, kernel, iterations=4)
    img2 = cv2.GaussianBlur(mask, (5, 5), 0)

    opening = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    #cv2.imshow("img", closing)
    tracker(closing, ctime, ptime)

