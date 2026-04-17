import cv2
import mediapipe as mp
import numpy as np
import subprocess
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access camera.")
    raise SystemExit

print("Hand Gesture Control Started! Press q to quit.")
print("Thumb-index distance controls brightness and volume.")

def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def map_range(value, in_min, in_max, out_min, out_max):
    value = clamp(value, in_min, in_max)
    if in_max == in_min:
        return out_min
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_volume_percent(percent):
    percent = clamp(int(percent), 0, 100)
    subprocess.run([
        "osascript",
        "-e",
        f"set volume output volume {percent}"
    ])

def brightness_up():
    subprocess.run([
        "osascript",
        "-e",
        'tell application "System Events" to key code 144'
    ])

def brightness_down():
    subprocess.run([
        "osascript",
        "-e",
        'tell application "System Events" to key code 145'
    ])

def adjust_brightness(percent):
    percent = clamp(int(percent), 0, 100)
    if percent > 55:
        brightness_up()
    elif percent < 45:
        brightness_down()

def draw_bar(img, x1, y1, x2, y2, value, color, label):
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    fill_y = int(map_range(value, 0, 100, y2, y1))
    cv2.rectangle(img, (x1, fill_y), (x2, y2), color, cv2.FILLED)
    cv2.putText(img, f"{label}: {int(value)}%", (x1 - 15, y1 - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

last_action_time = 0
ACTION_DELAY = 0.2
last_volume = None
last_brightness = None

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    status_text = "No hand detected"

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        lm = hand_landmarks.landmark
        thumb_x, thumb_y = int(lm[4].x * w), int(lm[4].y * h)
        index_x, index_y = int(lm[8].x * w), int(lm[8].y * h)

        cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (index_x, index_y), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)

        distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
        volume_level = map_range(distance, 20, 250, 0, 100)
        brightness_level = map_range(distance, 20, 250, 0, 100)

        current_time = time.time()
        if current_time - last_action_time > ACTION_DELAY:
            set_volume_percent(volume_level)
            adjust_brightness(brightness_level)
            last_action_time = current_time
            last_volume = volume_level
            last_brightness = brightness_level

        status_text = f"Distance: {int(distance)}"
        cv2.putText(frame, f"Thumb-Index Distance: {int(distance)}", (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Volume: {int(volume_level)}%", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Brightness: {int(brightness_level)}%", (10, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    draw_bar(frame, 30, 420, 80, 150, 0 if last_volume is None else last_volume, (0, 255, 255), "Volume")
    draw_bar(frame, 110, 420, 160, 150, 0 if last_brightness is None else last_brightness, (255, 255, 0), "Brightness")

    cv2.putText(frame, status_text, (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Hand Volume + Brightness Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
