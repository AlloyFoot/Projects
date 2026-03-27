import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access camera.")
    exit()

print("Hand Tracking Started! Press q to quit!")

prev_x, prev_y = None, None
shape_x, shape_y = 300, 300
color = (255, 0, 0)
size = 40
SMOOTHING = 0.7

def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    tip_ids = [4, 8, 12, 16, 20]
    pip_ids = [2, 6, 10, 14, 18]
    extended = 0

    # Thumb (x-axis check)
    if abs(landmarks[tip_ids[0]].x - landmarks[pip_ids[0]].x) > 0.04:
        extended += 1
    
    # Other fingers (y-axis check)
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
            extended += 1
    
    if extended >= 4:
        return "Open"
    elif extended <= 1:
        return "Closed Fist"
    else:
        return "Partial"

def get_direction(curr_x, curr_y):
    global prev_x, prev_y
    direction = None

    if prev_x is not None and prev_y is not None:
        dx = curr_x - prev_x
        dy = curr_y - prev_y

        if abs(dx) > abs(dy):
            if dx > 10:
                direction = "RIGHT"
            elif dx < -10:
                direction = "LEFT"
        else:
            if dy > 10:
                direction = "DOWN"
            elif dy < -10:
                direction = "UP"

    prev_x, prev_y = curr_x, curr_y
    return direction


import math
def get_hand_size(landmarks):
    x1, y1 = landmarks[0].x, landmarks[0].y
    x2, y2 = landmarks[12].x, landmarks[12].y
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    gesture = "No hand detected"
    hand_detected = False

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_detected = True
            hand_label = results.multi_handedness[idx].classification[0].label
            gesture = detect_gesture(hand_landmarks)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingertip_ids = [4, 8, 12, 16, 20]

            for tip_id in fingertip_ids:
                lm = hand_landmarks.landmark[tip_id]
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
                cv2.putText(frame, str(tip_id), (x - 5, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            wrist = hand_landmarks.landmark[0]
            wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)

            # Movement tracking (use index finger tip)
            index_tip = hand_landmarks.landmark[8]
            curr_x, curr_y = int(index_tip.x * w), int(index_tip.y * h)

            direction = get_direction(curr_x, curr_y)

            if direction == "RIGHT":
                shape_x += 10
            elif direction == "LEFT":
                shape_x -= 10
            elif direction == "UP":
                shape_y -= 10
            elif direction == "DOWN":
                shape_y += 10

            # Dynamic size based on hand distance
            hand_size = get_hand_size(hand_landmarks.landmark)
            size = int(hand_size * 300)

            # Gesture-based color change
            if gesture == "Open":
                color = (0, 255, 0)
            elif gesture == "Closed Fist":
                color = (0, 0, 255)

            cv2.putText(frame, f"{hand_label} Hand", (wrist_x - 40, wrist_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    if not hand_detected:
        prev_x, prev_y = None, None

    status_color = (0, 255, 0) if gesture in ["Open", "Closed Fist"] else (0, 165, 255)

    cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
    cv2.circle(frame, (shape_x, shape_y), max(10, size), color, -1)
    cv2.imshow("Hand Gesture Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
