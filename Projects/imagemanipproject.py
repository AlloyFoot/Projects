import cv2
import numpy as np
import matplotlib.pyplot as plt

IMAGE_FILE = "image5.jpg"
OUTPUT_FOLDER = "output_images"

def load_image(filename):
    img = cv2.imread(filename)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {filename}")
    return img

def show_image(title, img, cmap=None):
    plt.figure(figsize=(8, 6))
    if cmap:
        plt.imshow(img, cmap=cmap)
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

def convert_to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def crop_image(img, x1=100, y1=200, x2=400, y2=500):
    return img[y1:y2, x1:x2]

def rotate_image(img, angle=45):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, matrix, (w, h))

def brighten_image(img, value=50):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

def save_image(filename, img):
    cv2.imwrite(filename, img)

def main():
    img = load_image(IMAGE_FILE)

    gray = convert_to_grayscale(img)
    cropped = crop_image(img)
    rotated = rotate_image(img, 45)
    brightened = brighten_image(img, 50)

    show_image("Original", img)
    show_image("Grayscale", gray, cmap="gray")
    show_image("Cropped", cropped)
    show_image("Rotated", rotated)
    show_image("Brightened", brightened)

    save_image("1grayscale.jpg", gray)
    save_image("1cropped.jpg", cropped)
    save_image("1rotated.jpg", rotated)
    save_image("1brightened.jpg", brightened)

    print(f"Saved transformed images")

if __name__ == "__main__":
    main()
