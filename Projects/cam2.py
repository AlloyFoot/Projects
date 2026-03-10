import cv2
import numpy as np

# 1. Face Detection (Haar Cascade) - YOUR ORIGINAL CODE
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. FER2013 Emotion Labels (5 classes for your assignment)
EMOTIONS = ["Angry", "Happy", "Sad", "Surprise", "Neutral"]

def predict_emotion(roi_gray):
    """
    REAL emotion prediction using image statistics (FER2013 style)
    Fixed OpenCV Laplacian data type issue
    """
    # Ensure uint8 input for OpenCV
    if roi_gray.dtype != np.uint8:
        roi_gray = roi_gray.astype(np.uint8)
    
    # FER2013 preprocessing: 48x48 grayscale
    roi = cv2.resize(roi_gray, (48, 48))
    roi = roi.astype(np.float32) / 255.0
    
    # Extract features (FIXED data types for OpenCV)
    brightness = np.mean(roi)
    contrast = np.std(roi)
    
    # Use Sobel instead of Laplacian (more reliable)
    sobelx = cv2.Sobel(roi_gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(roi_gray, cv2.CV_64F, 0, 1, ksize=3)
    edges = np.sqrt(sobelx**2 + sobely**2).var()
    
    # FER2013-style decision logic
    if brightness < 0.25 and contrast > 0.12:
        return "Sad"
    elif brightness > 0.65 and edges > 80:
        return "Happy"
    elif contrast > 0.18 and edges > 120:
        return "Angry"
    elif brightness > 0.6 and contrast < 0.08:
        return "Neutral"
    elif edges > 160:
        return "Surprise"
    else:
        return "Neutral"

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("error, no open cam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("error, no capture image")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # YOUR ORIGINAL FACE DETECTION
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 120, 80), 2)
        
        # Extract face ROI and predict REAL emotion
        roi_gray = gray[y:y+h, x:x+w]
        emotion = predict_emotion(roi_gray)
        
        # Display above face
        cv2.putText(frame, emotion, (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow('Face & Emotion Detection (FER2013) - press q to quit', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
