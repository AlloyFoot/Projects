import cv2
import numpy as np
import os

def apply_color_filter(image, filter_type):
    filtered_image = image.copy()
    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 0] = 0
    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0
    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0
    elif filter_type == "increase_red":
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], 50)
    elif filter_type == "decrease_blue":
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], 50)
    elif filter_type == "increase_green":
        filtered_image[:, :, 1] = cv2.add(filtered_image[:, :, 1], 50)
    elif filter_type == "decrease_red":
        filtered_image[:, :, 2] = cv2.subtract(filtered_image[:, :, 2], 50)
    return filtered_image

image_path = "image7.png"
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found")
else:
    filter_type = "original"

    print("Press the following keys to apply filters: ")
    print("r - red tint")
    print("b - blue tint")
    print("g - green tint")
    print("i - increase red")
    print("d - decrease blue")
    print("up arrow - increase green intensity")
    print("down arrow - decrease red intensity")
    print("s - save current filtered image")
    print("q - quit")

    while True:
        filtered_image = apply_color_filter(image, filter_type)
        cv2.imshow("Filtered Image", filtered_image)
        key = cv2.waitKeyEx(0)

        if key == ord('r'):
            filter_type = "red_tint"
        elif key == ord('b'):
            filter_type = "blue_tint"
        elif key == ord('g'):
            filter_type = "green_tint"
        elif key == ord('i'):
            filter_type = "increase_red"
        elif key == ord('d'):
            filter_type = "decrease_blue"
        elif key in (82, 2490368, 63232):
            filter_type = "increase_green"
        elif key in (84, 2621440, 63233):
            filter_type = "decrease_red"
        elif key == ord("s"):
            cv2.imwrite("newImage.jpg", filtered_image)
            print("Image has been saved as \"newImage.jpg\".")
        elif key == ord('q'):
            print("Exiting...")
            break
        else:
            print("invalid key")
        
cv2.destroyAllWindows()