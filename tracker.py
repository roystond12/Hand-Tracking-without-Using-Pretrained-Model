import cv2
import collections
import numpy

x1, y1, x2, y2 = 200, 100, 440, 380

class LineDetector:
    def __init__(self, k=5):
        self.last_k_cx = collections.deque(maxlen=k)

    def get_smoothed_center(self, cx, cy):
        self.last_k_cx.append(cx)
        cx_smooth = int(numpy.mean(self.last_k_cx)) 
        return cx_smooth, cy 

def area(cnt):
    return cv2.contourArea(cnt)

line_detector = LineDetector(k=5)

def tracker(img, ctime, p_time):
    threshold = 1000
    
    h, w = img.shape[:2]
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    len(contours)
    
    large_contours = [cnt for cnt in contours if area(cnt) >= threshold]
    print(large_contours)
    if large_contours:

        cnt = max(large_contours, key=lambda x: cv2.contourArea(x))
        temp = cv2.drawContours(img, cnt, -1, (255,0,0), 3)
        convhull = cv2.convexHull(cnt, returnPoints = True)
        img = cv2.drawContours(img, [convhull], -1, (0,0,255), 3, 2)
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"]) if M["m00"] != 0 else w // 2
        cY = int(M["m01"] / M["m00"]) if M["m00"] != 0 else h // 2
        cX, cY = line_detector.get_smoothed_center(cX, cY)
        
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x1,y1),(x2,y2),(225,225,225),5)
        cv2.circle(img, (x+w//2, y+h//2), 100, (0, 255, 0), -1)
        
        if p_time != 0:
            cv2.putText(img, f"FPS {1 / (ctime - p_time):.2f}", (450, 30), cv2.FONT_HERSHEY_PLAIN, 2, (225, 0, 0))
        
        p_time = ctime
    else:
        p_time = 0
    cv2.imshow("Image", img)
    return p_time

