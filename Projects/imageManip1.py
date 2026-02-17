import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image5.jpg")

imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(imageRGB)
plt.title("RGB Image")
plt.show()

imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(imageGray, cmap='gray')
plt.title("Grayscale Image")
plt.show()

croppedImage = image[100:300, 200:400]
cropped_rgb = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)
plt.imshow(cropped_rgb)
plt.title("Cropped RGB Image")
plt.show()