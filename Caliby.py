import cv2

# Set up video capture
cap = cv2.VideoCapture(1)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Set the frame dimensions to 640x640
frame_width, frame_height = 640, 640

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize frame to 640x640
    frame = cv2.resize(frame, (frame_width, frame_height))

    # Calculate center of the frame
    center_x, center_y = frame_width // 2, frame_height // 2

    # Draw crosshair lines in red
    color = (0, 0, 255)  # Red color in BGR
    thickness = 1

    # Draw horizontal line
    cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), color, thickness)
    
    # Draw vertical line
    cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), color, thickness)

    # Display the resulting frame
    cv2.imshow('Video with Crosshair', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()