import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    elif filter_type == "sobel":
            gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            filtered_image = combined_sobel
    elif filter_type == "canny":
            gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
            filtered_image = cv2.Canny(gray_image, 100, 200)
    elif filter_type == "cartoon":
        gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.medianBlur(gray_image, 5)
        e = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        c = cv2.bilateralFilter(filtered_image, 9, 250, 250)
        filtered_image = cv2.bitwise_and(c, c, mask=e)
        return filtered_image
    return filtered_image

def display_image(title, image):
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

def get_filter():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not found")
        return


    print("Press the following keys to apply filters: ")
    print("s: Sobel Edge Detection")
    print("c: Canny Edge Detection")
    print("a: Cartoon Filter")
    print("r: Red Tint")
    print("b: Blue Tint")
    print("g: Green Tint")
    print("q: Exit")

    filter_type = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("failed to get frame")
            break

        if filter_type:
            filtered_frame = apply_color_filter(frame, filter_type)
            cv2.imshow("Filtered Frame", filtered_frame)
        else:
            cv2.imshow("Filtered Frame", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            filter_type = "red_tint"
        elif key == ord('b'):
            filter_type = "blue_tint"
        elif key == ord('g'):
            filter_type = "green_tint"
        elif key == ord('s'):
            filter_type = "sobel"
        elif key == ord('c'):
            filter_type = "canny"
        elif key == ord('a'):
            filter_type = "cartoon"
        elif key == ord('q'):
            print("Exiting...")
            break
        else:
            continue
        
    cap.release()
    cv2.destroyAllWindows()
get_filter()