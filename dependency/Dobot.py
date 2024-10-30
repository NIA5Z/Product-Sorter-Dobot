from serial.tools import list_ports
import pydobot
import torch
from time import sleep
Init = 1
device = None
Marker=[]

def init(d):
 global Init, device
 device=d
 home(overwrite=True)
 #available_ports = list_ports.comports()
 #print(f'Available Ports: {[x.device for x in available_ports]}')

 #if not available_ports:
 #   print("No available serial ports found. Make sure Dobot is connected.")
 #   return

 #port = available_ports[0].device
 #print(f"Using port: {port}")

 #device = pydobot.Dobot(port="COM3", verbose=True)
 #Init = 1
 #print("Dobot connected successfully!")

def move(x,y,z,r,s=False,v=100,a=100,w=True):
   global Init, device

   if Init == 0:
      print("Library haven't been initialized yet.")
      return
   try:
    device.speed(v,a)
    device.suck(s)
    device.move_to(x,y,z,r,wait=w)
   except:
     print("Mission Failed Retrying")
     return

def position():
    global Init, device

    if Init == 0:
      print("Library haven't been initialized yet.")
      return

    x, y, z, r, j1, j2, j3, j4 = device.pose()
    return x, y, z, r, j1, j2, j3, j4 

def home(recall=False,overwrite=False):
   global Init,xh, yh, zh, rh
   if overwrite:
    xh, yh, zh, rh = position()[:4]
    print("Forward Home Set")
   elif recall:
     return xh,yh,zh,rh
   else:
    move(xh,yh,zh,rh)

def close():
   global Init, device

   if Init == 0:
    print("Library haven't been initialized yet.")
    return
   device.close()

def MarkLoc(Data=None,Recall=False,MarkerDump=False):
  global Marker
  try:
   if not Recall:
    if not any(item[0] == Data for item in Marker): 
     x, y, z, r, j1, j2, j3, j4 = device.pose()
     Marker.append([Data,x, y, z, r, j1, j2, j3, j4])
    else:
      return
   else:
     return Marker

   if MarkerDump:
    Marker=[]
    print("You have dumped marked location")
  except:
   print("Task Failed")
   return

cpar=0
def partol(z=5.309715270996094):
  global cpar
  movements = [
    [235.9379425048828, 8.170378684997559, 5.309715270996094, 1.9833234548568726, True],
    [219.79217529296875, -87.26564025878906, 5.309715270996094, -21.654911041259766, True],
    [163.7543487548828, -170.5627899169922, 5.309715270996094, -46.16667556762695, True],
    [235.9379425048828, 8.170378684997559, 5.309715270996094, 1.9833234548568726, True],
    [52.93641662597656, -230.35374450683594, 5.309715270996094, -77.05785369873047, True],
    [186.04794311523438, 98.2791519165039, 5.309715270996094, 27.845088958740234, True],
    [91.06847381591797, 191.6711883544922, 5.309715270996094, 64.58626556396484, True],
    [-7.536583423614502, 220.5813446044922, 5.309715270996094, 91.95685577392578, True],
    [235.9379425048828, 8.170378684997559, 5.309715270996094, 1.9833234548568726, True],
    [209.1031951904297, 216.96316528320312, -9.302131652832031, 46.056854248046875, True],
    [282.0387878417969, -106.8825912475586, -6.935401916503906, -20.754911422729492,True],
    [212.19943237304688, -174.7347869873047, -5.416999816894531, -39.4696159362793, True]
  ]
  move(movements[cpar][0],movements[cpar][1],z,movements[cpar][3],w=True)
  cpar+=1
  if cpar == 3:
    cpar = 0