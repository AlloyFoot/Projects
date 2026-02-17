import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("image4.png")

imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

(h, w) = image.shape[:2]
center = (h//2, w//2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))

rotatedRGB = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
plt.imshow(rotatedRGB)
plt.title("Rotated RGB Image")
plt.show()

brightnessMatrix = np.ones(image.shape, dtype="uint8") * 50
brighter = cv2.add(image, brightnessMatrix)

brighterRGB = cv2.cvtColor(brighter, cv2.COLOR_BGR2RGB)
plt.imshow(brighterRGB)
plt.title("Brightened RGB Image")
plt.show()