import cv2
import numpy as np
from collections import deque

x1, y1, x2, y2 = 200, 100, 440, 380

class CentroidSmoother:
    def __init__(self, k=7):
        self.points = deque(maxlen=k)

    def smooth(self, cx, cy):
        self.points.append((cx, cy))
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return int(np.mean(xs)), int(np.mean(ys))


smoother = CentroidSmoother(k=7)


def tracker(mask, frame, c_time, p_time):

    h, w = mask.shape[:2]
    frame_area = h * w

    # Hand area expected bounds
    min_area = frame_area * 0.015
    max_area = frame_area * 0.35

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        cv2.putText(frame, "NO HAND", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("Output", frame)
        return c_time

    cnt = max(contours, key=cv2.contourArea)
    A = cv2.contourArea(cnt)

    if not (min_area < A < max_area):
        cv2.putText(frame, "INVALID BLOB", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("Output", frame)
        return c_time

    x, y, bw, bh = cv2.boundingRect(cnt)
    ratio = bh / float(bw)
    if not (0.6 < ratio < 2.5):
        cv2.putText(frame, "BAD RATIO", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("Output", frame)
        return c_time

    hull = cv2.convexHull(cnt)
    cv2.drawContours(frame, [hull], -1, (0, 0, 255), 2)

    M = cv2.moments(cnt)
    if M["m00"] == 0:
        cv2.imshow("Output", frame)
        return c_time

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    cx, cy = smoother.smooth(cx, cy)

    # Draw centroid
    cv2.circle(frame, (cx, cy), 6, (0, 255, 0), -1)

    # Draw rectangle boundary
    cv2.rectangle(frame, (x1, y1), (x2, y2),
                  (255, 255, 255), 2)

    # FPS text
    if p_time:
        fps = 1 / (c_time - p_time)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.imshow("Output", frame)
    return c_time
