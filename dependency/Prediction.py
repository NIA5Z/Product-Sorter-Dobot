from ultralytics import YOLO
import cv2

model = None
Init = 0

def init(Model_Path="./Model/Gen_I/weights/best.pt"):
    global model,Init
    try:
     model = YOLO(Model_Path)
     Init = 1
     print("Model Loaded")
     return
    except:
     print("Failed to load Model.")
     return
    
def predict(frame):
    global model, Init
    if Init == 0:
        print("Model not initialized. Please initialize the model first.")
        return

    try:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(image)
        return results
    except Exception as e:
        print("Prediction failed:", e)
        return
    
#init()
#cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#while True:
# success, frame = cam.read()

# results = predict(frame)
# print(results[0].boxes.xyxy)

