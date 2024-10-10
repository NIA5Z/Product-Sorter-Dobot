import cv2
import time
from dependency.QRread import ReadCV

def video(Source=0,Width=640,Height=480,frame_rate = 5):
    prev_time = 0
    fps = 0

    cam = cv2.VideoCapture(Source)   
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, Width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, Height)

    while True:
        success, frame = cam.read()
        if not success:
            break

        time_elapsed = time.time() - prev_time

        if time_elapsed > 1.0 / frame_rate:
            prev_time = time.time()

            if time_elapsed > 0:
             fps = 1 / time_elapsed 
            cv2.putText(frame, f"FPS: {round(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            Decoded = ReadCV(frame)
            cv2.putText(frame, str(Decoded), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

            _, jpeg_frame = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg_frame.tobytes()

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

video()