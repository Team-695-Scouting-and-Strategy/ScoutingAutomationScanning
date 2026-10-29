import cv2

# 0 is usually the built-in webcam. Use 1 or 2 if you have external cameras.

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Can't receive frame.")
        break

    # Display the live stream
    cv2.imshow('Live Camera Feed', frame)

    # Press 'q' on the keyboard to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up and release resources
cap.release()
cv2.destroyAllWindows()
