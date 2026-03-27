

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

color_mode = None   # 'r', 'g', 'b'
edge_mode = None    # 'sobel', 'canny'

def apply_color_filter(frame, mode):
    if mode == 'r':
        frame[:, :, 1] = 0
        frame[:, :, 0] = 0
    elif mode == 'g':
        frame[:, :, 2] = 0
        frame[:, :, 0] = 0
    elif mode == 'b':
        frame[:, :, 2] = 0
        frame[:, :, 1] = 0
    return frame

def apply_sobel(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    sobel = cv2.magnitude(sobelx, sobely)
    return cv2.convertScaleAbs(sobel)

def apply_canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 200)

print("Press r/g/b for color filters")
print("Press s for Sobel, c for Canny")
print("Press q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    output = frame.copy()

    # Apply color filter
    if color_mode:
        output = apply_color_filter(output, color_mode)

    # Apply edge detection
    if edge_mode == 'sobel':
        edges = apply_sobel(output)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif edge_mode == 'canny':
        edges = apply_canny(output)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    cv2.imshow("Filters", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key in [ord('r'), ord('g'), ord('b')]:
        color_mode = chr(key)
        print(f"Color mode: {color_mode}")
    elif key == ord('s'):
        edge_mode = 'sobel'
        print("Edge mode: Sobel")
    elif key == ord('c'):
        edge_mode = 'canny'
        print("Edge mode: Canny")
    elif key != 255:
        print("Invalid key pressed")

cap.release()
cv2.destroyAllWindows()