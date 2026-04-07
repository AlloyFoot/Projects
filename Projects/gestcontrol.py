import cv2
import mediapipe as mp
import numpy as np
import time
import os
from datetime import datetime

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

os.makedirs('output', exist_ok=True)

current_filter = 0
filter_names = ['Normal', 'Sepia', 'Negative', 'Blur', 'Glitch', 'Edge', 'Cartoon']

def apply_sepia(image):
    sepia_filter = np.array([[0.393, 0.769, 0.189],
                            [0.349, 0.686, 0.168],
                            [0.272, 0.534, 0.131]])
    sepia_img = cv2.transform(image, sepia_filter)
    sepia_img[np.where(sepia_img > 255)] = 255
    return sepia_img.astype(np.uint8)

def apply_negative(image):
    return 255 - image

def apply_blur(image):
    return cv2.GaussianBlur(image, (15, 15), 0)

def apply_glitch(image):
    h, w = image.shape[:2]
    glitch = image.copy()
    for i in range(0, h, 20):
        shift = np.random.randint(-10, 10)
        glitch[i:i+10, max(0, shift):min(w, w+shift)] = image[i:i+10, max(0, -shift):min(w, w-shift)]
    return glitch

def apply_edge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return edges

def apply_cartoon(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def check_thumb_index_touch(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    dist = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    return dist < 0.04

def check_thumb_middle_touch(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    dist = np.sqrt((thumb_tip.x - middle_tip.x)**2 + (thumb_tip.y - middle_tip.y)**2)
    return dist < 0.04

def check_thumb_ring_touch(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    dist = np.sqrt((thumb_tip.x - ring_tip.x)**2 + (thumb_tip.y - ring_tip.y)**2)
    return dist < 0.04

def check_thumb_pinky_touch(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
    dist = np.sqrt((thumb_tip.x - pinky_tip.x)**2 + (thumb_tip.y - pinky_tip.y)**2)
    return dist < 0.04

cap = cv2.VideoCapture(0)

prev_thumb_index_touch = False
prev_thumb_middle_touch = False
prev_thumb_ring_touch = False
prev_thumb_pinky_touch = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_image)

    filtered_image = image.copy()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(filtered_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            thumb_index_touch = check_thumb_index_touch(landmarks)
            thumb_middle_touch = check_thumb_middle_touch(landmarks)
            thumb_ring_touch = check_thumb_ring_touch(landmarks)
            thumb_pinky_touch = check_thumb_pinky_touch(landmarks)

            if thumb_index_touch and not prev_thumb_index_touch:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"output/picture_{timestamp}.jpg"
                cv2.imwrite(filename, filtered_image)
                print(f"Picture saved: {filename}")
            
            if thumb_middle_touch and not prev_thumb_middle_touch:
                if current_filter in [1, 2]:
                    current_filter = 2 if current_filter == 1 else 1
                else:
                    current_filter = 1
            
            if thumb_ring_touch and not prev_thumb_ring_touch:
                if current_filter in [3, 4]:
                    current_filter = 4 if current_filter == 3 else 3
                else:
                    current_filter = 3 
            
            if thumb_pinky_touch and not prev_thumb_pinky_touch:
                if current_filter in [5, 6]:
                    current_filter = 6 if current_filter == 5 else 5
                else:
                    current_filter = 5 

            prev_thumb_index_touch = thumb_index_touch
            prev_thumb_middle_touch = thumb_middle_touch
            prev_thumb_ring_touch = thumb_ring_touch
            prev_thumb_pinky_touch = thumb_pinky_touch

            if current_filter == 1:
                filtered_image = apply_sepia(filtered_image)
            elif current_filter == 2:
                filtered_image = apply_negative(filtered_image)
            elif current_filter == 3:
                filtered_image = apply_blur(filtered_image)
            elif current_filter == 4:
                filtered_image = apply_glitch(filtered_image)
            elif current_filter == 5:
                filtered_image = apply_edge(filtered_image)
            elif current_filter == 6:
                filtered_image = apply_cartoon(filtered_image)

    cv2.putText(filtered_image, f"Filter: {filter_names[current_filter]}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(filtered_image, "Thumb+Index: Photo | Thumb+Middle: Sepia<->Neg", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(filtered_image, "Thumb+Ring: Blur<->Glitch | Thumb+Pinky: Edge<->Cartoon", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    cv2.imshow('Hand Gesture Filter Camera', filtered_image)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()