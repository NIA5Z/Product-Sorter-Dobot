import cv2
import time
import json
from dependency.QRread import ReadCV,BarcodeReader
from dependency.Prediction import init,predict

DecodedQR = None
DecodedBar = None

def video(Source=0,Width=640,Height=480,frame_rate = 5):
    global DecodedQR,DecodedBar
    init("./Model/Gen_I/weights/best.pt")
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
            results=predict(frame)

            boxes=results[0].boxes.xyxy
            classes=results[0].boxes.cls
            confidences=results[0].boxes.conf

            for box, cls, conf in zip(boxes, classes, confidences):
             x1, y1, x2, y2 = map(int, box)
             label = f"{results[0].names[int(cls)]} {conf:.2f}" 
             cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2) 
             cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)


            if time_elapsed > 0:
             fps = 1 / time_elapsed 
            cv2.putText(frame, f"FPS: {round(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

            DecodedQR = ReadCV(frame)
            if DecodedQR is None or DecodedQR == [()]:
             cv2.putText(frame, "No QR Code Detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            else:
             cv2.putText(frame, str(DecodedQR), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

            DecodedBar = BarcodeReader(frame)
            if DecodedBar is None:
                Data, Type = None, None
                cv2.putText(frame, "No Barcode Detected.", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            else:
                Data, Type = DecodedBar
                cv2.putText(frame, f"Data: {str(Data)}, Type: {str(Type)}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

            _, jpeg_frame = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg_frame.tobytes()

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def getDecoded():
    global DecodedQR,DecodedBar
    while True:
     if DecodedBar is None:
        Data, Type = None, None
     else:
        Data, Type = DecodedBar

     response_data = {"QR": DecodedQR,"Data": Data,"Type": Type}
     yield json.dumps(response_data).encode('utf-8')