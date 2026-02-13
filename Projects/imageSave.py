import cv2
img = cv2.imread("image3.png")
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
resizedImg = cv2.resize(grayImg, (224, 224))

cv2.imshow("Loaded Image", img)
key = cv2.waitKey(0)

if key == ord("s"):
    cv2.imwrite("grayscale_resized_image.jpg", resizedImg)
    print("Image has been saved as \"grayscale_resized_image.jpg\".")
else:
    print("Image not saved.")

cv2.destroyAllWindows()
print(f"Image Dimensions: {resizedImg.shape}")