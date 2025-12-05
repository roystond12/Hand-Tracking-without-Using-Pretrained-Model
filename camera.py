import cv2
import time
from segment import segment_and_track

def camera():
    cap = cv2.VideoCapture(0)

    p_time = None

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  

        c_time = time.time()
        p_time = segment_and_track(frame, c_time, p_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera()
