import serial
from serial.tools import list_ports
from pydobot import Dobot
from dependency.Speech import speak

Init = 0
device = None

def init():
 global Init, device
 available_ports = list_ports.comports()
 print(f'Available Ports: {[x.device for x in available_ports]}')

 if not available_ports:
    print("No available serial ports found. Make sure Dobot is connected.")
    return

 port = available_ports[0].device
 print(f"Using port: {port}")

 try:
    device = Dobot(port=port, verbose=True)
    home()
    print("Dobot connected successfully!")
 except Exception as e:
    print(f"Failed to connect to Dobot: {e}")
    return

def move(x,y,z,r,s=False,v=50,a=50):
   global Init, device

   if Init == 0:
      print("Library haven't been initialized yet.")
      return
   
   device.speed(v,a)
   device.move_to(x,y,z,r,wait=True)
   device.suck(s)

def position():
    global Init, device

    if Init == 0:
      print("Library haven't been initialized yet.")
      return

    x, y, z, r, j1, j2, j3, j4 = device.pose()
    return x, y, z, r, j1, j2, j3, j4 

def home(overwrite=False):
   global Init
   if (Init == 0 or overwrite==True):
    try:
     xh, yh, zh, rh = position()[:4]
    except:
      return
    Init = 1
    print("Forward Home Set")
   else:
      speak("Returning Home.")
      move(xh,yh,zh,rh)

def close():
   global Init, device

   if Init == 0:
    print("Library haven't been initialized yet.")
    return
   device.close()