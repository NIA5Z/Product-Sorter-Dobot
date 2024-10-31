import cv2
import time
from Req import get
import math
from dependency.QRread import ReadCV
from dependency.Prediction import init,predict
from dependency.Dobot import move,position,MarkLoc,home,partol
  
DecodedQR = None
classes,boxes = None,None

def video(Model="./Model/Gen_II/Sub_Model/QRBar_Model/NCNN/best_ncnn_model",Source=0,Width=640,Height=640,frame_rate = 5,web=None):
    global DecodedQR,boxes,classes,Type,PID
    init(Model)
    prev_time = 0
    fps = 0
    posx,posy=None,None
    distance = 0
    Bypass = False
    lock=[]

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
            for result in results:
             boxes=result.obb.xyxy
             classes=result.obb.cls
             confidences=result.obb.conf

            if classes.cpu().numpy().size == 0 or Bypass: 
              z = position()[2]
              partol(z)
            print(lock)
            x,y,d = frame.shape
            Screen_x, Screen_y = y // 2, x // 2
            cv2.line(frame, (Screen_x - 10, Screen_y), (Screen_x + 10, Screen_y), (0, 0, 255), 2)
            cv2.line(frame, (Screen_x, Screen_y - 10), (Screen_x, Screen_y + 10), (0, 0, 255), 2)

            try:
             Type,PID = str(DecodedQR[0][0]).split()
             print(Type,PID)
            except:
              pass
            
            try:
              if  DecodedQR[0][0] in lock:
                Bypass = True
              else:
                Bypass = False
            except:
              pass

            for box, cls, conf in zip(boxes, classes, confidences):
             x1, y1, x2, y2 = map(int, box)
             center_x = (x1 + x2) // 2
             center_y = (y1 + y2) // 2  
             distance = math.sqrt((Screen_x - center_x) ** 2 + (Screen_y - center_y) ** 2)
             tx,ty,tz,tr = position()[:4]
             print(MarkLoc(Recall=True))
             label = f"{results[0].names[int(cls)]} {distance:.2f} {posx} {posy}" 
             cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2) 
             cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
             cv2.circle(frame, (center_x, center_y), radius=5, color=(0, 255, 0), thickness=-1) 
             cv2.circle(frame, (Screen_x, Screen_y), radius=20, color=(0, 0, 255), thickness=1) 
             cv2.line(frame, (center_x, center_y), (Screen_x, Screen_y), (0, 255, 255), 2) 

             if time_elapsed > 0:
              fps = 1 / time_elapsed 
             cv2.putText(frame, f"FPS: {round(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

             DecodedQR = ReadCV(frame)
             if DecodedQR is None or DecodedQR == [()]:
              cv2.putText(frame, "No QR Code Detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
             else:
              cv2.putText(frame, str(DecodedQR), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
             if None not in (tx,ty,tz,tr,distance):
              if distance > 200:
                step=15
              elif (distance > 150 and distance < 200):
                step=5
              else:
                step=2

              if center_x < Screen_x:
               posx = "Left"
               ty+=step
              elif center_x > Screen_x:
               posx = "Right"
               ty-=step
              else:
               posx = "Center"

              if center_y < Screen_y:
               posy = "Above"
               tx+=step
              elif center_y > Screen_y:
               posy = "Below"
               tx-=step
              else:
               posy = "Middle"
             
             if distance > 15:
              move(tx,ty,tz,tr)

             if distance <= 15 and None not in DecodedQR:
               try:
                if "LOC" == Type:
                 MarkLoc(DecodedQR[0][0])
                 lock.append(DecodedQR[0][0])
                 home()

                if "ITEM" == Type:
                  for item in MarkLoc(Recall=True):
                    if PID in item[0]:
                      xr,yr,zr,rr = item[1],item[2],item[3],item[4]
                      x,y,z,r = position()[:4]
                  move(x,y,z-50,r,s=True) 
                  move(x,y,z,r,s=True)
                  move(xr,yr,zr,rr,s=True)
                  move(xr,yr,zr-50,rr,s=True)
                  move(xr,yr,zr,rr)
                  home()
                  pull = web + f"/fetch?CODE={PID}"
                  respond = get(pull).content.decode("utf-8").replace("[","").replace("]","").split(',')
                  code = int(respond[1])
                  brand = respond[2].replace('"', "")
                  name = respond[3].replace('"', "")
                  type_ = respond[4].replace('"', "")
                  punit = float(respond[5])
                  pbase = int(respond[6])
                  qty_adjust = int(respond[7])-1 
                  push = (
                     f"{web}/update?CODE={code}&BRAND={brand}&NAME={name}"
                     f"&TYPE={type_}&PUnit={punit}&PBase={pbase}&QTY={qty_adjust}"
                    )
                  get(push)
                  if qty_adjust == 0: 
                   lock.append(f"{Type} {PID}")
                  xr,yr,zr,rr = x,y,z,r

               except:
                 pass
               
            _, jpeg_frame = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg_frame.tobytes()

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()