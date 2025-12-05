import cv2
import numpy as np
import time
from segment import segmentation
from collections import deque

def camera():
    frame = deque(maxlen=30)
    median = None
    cap = cv2.VideoCapture(0)
    
    while True:
        sucess,img = cap.read()
        if not sucess or img is None:
            break
        
        frame.append(img)
        if len(frame) == 30:
            median = np.median(frame,axis=0).astype(dtype=np.uint8)
        
        if median is not None:
            img = cv2.absdiff(img, median)
        
        ctime = time.time()
        if img is not None:
            segmentation(img,ctime,ptime=0)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

