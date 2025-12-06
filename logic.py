import cv2
import math

SAFE = 0
WARN = 1
DANGER = 2

def point_to_rect_distance(cx, cy, x1, y1, x2, y2):
    if x1 <= cx <= x2 and y1 <= cy <= y2:
        return 0
    
    dx = max(x1 - cx, 0, cx - x2)
    dy = max(y1 - cy, 0, cy - y2)
    return math.sqrt(dx*dx + dy*dy)

def classify_state(d, width, height):
    d_norm = d / min(width, height)

    if d_norm <= 0.03:
        return DANGER
    elif d_norm <= 0.08:
        return WARN
    return SAFE

def render_state(frame, state):
    if state == SAFE:
        cv2.putText(frame, "SAFE", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)
    elif state == WARN:
        cv2.putText(frame, "WARNING!", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3)
    else:
        cv2.putText(frame, "DANGER DANGER!", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)
        cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]),
                      (0,0,255), 5)

def logic(frame, cx, cy, box, c_time, p_time):
    (x1, y1, x2, y2) = box
    h, w = frame.shape[:2]

    d = point_to_rect_distance(cx, cy, x1, y1, x2, y2)
    state = classify_state(d, w, h)

    render_state(frame, state)

    if p_time:
        fps = 1 / (c_time - p_time)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, frame.shape[0]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Output", frame)
    return c_time
