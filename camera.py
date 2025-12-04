import cv2
import numpy as np
import time
from segment import segmentation

x1, y1, x2, y2 = 200, 100, 440, 380

def camera():
    frame = []
    median = 0
    cap = cv2.VideoCapture(0)
    p_time = count = 0 
    while True:
        sucess,img = cap.read()
        if count < 30:
            frame.append(img)
            count += 1
        else:
            median = np.median(frame,axis = 0).astype(dtype=np.uint8)
            img = cv2.absdiff(img,median)
        
        ctime = time.time()
        if not sucess or img is None:
            break
        cv2.putText(img,f"FPS {1 / (ctime - p_time)}",(450,30),cv2.FONT_HERSHEY_PLAIN,2,(225,0,0))
        p_time = ctime
        cv2.rectangle(img,(x1,y1),(x2,y2),(225,0,0))
        cv2.putText(img, "SAFE",(20,40),cv2.FONT_HERSHEY_PLAIN,1,(255, 255, 255),1)
        if np.any(median != 0):
            segmentation(img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


