import cv2
import os

image_name = "image4.png"

input_path = image_name
output_path = "annotated" + image_name

img = cv2.imread(input_path)

if img is None:
    print("Image not found")
    exit()

h, w, _ = img.shape

y = h // 2

cv2.arrowedLine(img, (0, y), (w, y), (0, 255, 0), 3, tipLength=0.05)
cv2.arrowedLine(img, (w, y), (0, y), (0, 255, 0), 3, tipLength=0.05)

text = f"{w}px"

text_x = w // 2 - 40
text_y = y - 10

cv2.putText(
    img,
    text,
    (text_x, text_y),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2,
    cv2.LINE_AA
)

cv2.imwrite(output_path, img)

print("Saved to:", output_path)
