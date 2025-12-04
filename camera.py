import cv2
import numpy as np
import time

x1, y1, x2, y2 = 200, 100, 440, 380

def camera():

    cap = cv2.VideoCapture(0)
    p_time = 0
    while True:
        sucess,img = cap.read()
        ctime = time.time()
        if not sucess or img is None:
            break
        cv2.putText(img,f"FPS {1 / (ctime - p_time)}",(450,30),cv2.FONT_HERSHEY_SIMPLEX,1,(225,0,0))
        p_time = ctime
        cv2.rectangle(img,(x1,y1),(x2,y2),(225,0,0))
        cv2.putText(img, "SAFE",(20,40),cv2.FONT_HERSHEY_PLAIN,1,(255, 255, 255),1)
        cv2.imshow("img",img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

