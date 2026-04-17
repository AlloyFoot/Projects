import cv2
import time
import pyautogui
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

CAM_WIDTH, CAM_HEIGHT = 640, 480
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

last_scroll_time = 0
SCROLL_DELAY = 0.5 

def detect_gesture(landmarks, handedness):
    fingers = []
    tips = [8, 12, 16, 20]

    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            fingers.append(1)
    
    thumb_tip = landmarks.landmark[4]
    thumb_ip = landmarks.landmark[3]

    if handedness.classification[0].label == "Right":
        if thumb_tip.x > thumb_ip.x:
            fingers.append(1)
    else:
        if thumb_tip.x < thumb_ip.x:
            fingers.append(1)
    
    if sum(fingers) == 5:
        return "open"
    elif len(fingers) == 0:
        return "closed"
    else:
        return "none"

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    gesture = "none"

    if result.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(
            result.multi_hand_landmarks, 
            result.multi_handedness 
        ):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            gesture = detect_gesture(hand_landmarks.landmark, hand_handedness)
            
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            current_time = time.time()
            if gesture == "open" and current_time - last_scroll_time > SCROLL_DELAY:
                pyautogui.scroll(3)
                last_scroll_time = current_time

    cv2.imshow('Hand Gesture Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
