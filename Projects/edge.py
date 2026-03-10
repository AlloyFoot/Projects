import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_images(title1, img1, title2, img2):
    plt.figure(figsize=(12,6))

    plt.subplot(1,2,1)
    if len(img1.shape) == 2:
        plt.imshow(img1, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    plt.title(title1)
    plt.axis("off")

    plt.subplot(1,2,2)
    if len(img2.shape) == 2:
        plt.imshow(img2, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    plt.title(title2)
    plt.axis("off")

    plt.show()

def interactive_edge_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = image.copy()
    display_images("Original Image", image, "Grayscale", gray_image)

    print("Select an option: ")
    print("1. Sobel Edge Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge detection")
    print("4. Gaussian Smoothening")
    print("5. Median Filtering")
    print("6. Save Processed Image")
    print("7. Exit")

    while True:
        choice = int(input("Enter your choice (1-7): "))

        if choice == 1:
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            processed_image = combined_sobel
            display_images("Original", gray_image, "Sobel", combined_sobel)
        elif choice == 2:
            print("Adjust thresholds for Canny (default: 100 and 200)")
            lower_thr = int(input("Enter lower threshold: "))
            upper_thr = int(input("Enter upper threshold: "))
            edges = cv2.Canny(gray_image, lower_thr, upper_thr)
            processed_image = edges
            display_images("Original", gray_image, "Canny", edges)
        elif choice == 3:
            lapalacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            laplacian_img = np.abs(lapalacian).astype(np.uint8)
            processed_image = laplacian_img
            display_images("Original", gray_image, "Laplacian", laplacian_img)
        elif choice == 4:
            print("Adjust kernel size for gaussian blur (must be odd, default 5)")
            kernel = int(input("Enter kernel size (odd number): "))
            blurred = cv2.GaussianBlur(image, (kernel, kernel), 0)
            processed_image = blurred
            display_images("Original", image, "Gaussian Blur", blurred)
        elif choice == 5:
            print("Adjust kernel size for median filtering (must be odd, default 5)")
            kernel = int(input("Enter kernel size (odd number): "))
            filtered = cv2.medianBlur(image, kernel)
            processed_image = filtered
            display_images("Original", image, "Median Filter", filtered)
        elif choice == 6:
            filename = input("Enter filename to save (without extension): ")
            safe = "".join(c for c in filename if c.isalnum() or c in ('_','-'))
            if safe == "":
                safe = "saved_image"
            path = f"{safe}.png"
            cv2.imwrite(path, processed_image)
            print(f"Image saved to {path}")

        elif choice == 7:
            print("exiting")
            break
        else:
            print("invalid")

img_name = "image2.png"
interactive_edge_detection(img_name)