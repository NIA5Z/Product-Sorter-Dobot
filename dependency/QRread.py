from qreader import QReader
from pyzbar.pyzbar import decode 
import numpy as np
import cv2

qreader = QReader()

def Read(Image):
 decoded_text = []
 for item in Image: 
  image = cv2.cvtColor(cv2.imread(item), cv2.COLOR_BGR2GRAY)
  decoded_text.append(qreader.detect_and_decode(image=image))
 return np.array(decoded_text)

def ReadCV(frame):
  decoded_text = []
  image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  decoded_text.append(qreader.detect_and_decode(image=image))
  if decoded_text is not None and len(decoded_text) > 0:
   return decoded_text
 
def BarcodeReader(frame): 
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detectedBarcodes = decode(image) 
    for barcode in detectedBarcodes:   
      if barcode.data!="": 
        return barcode.data,barcode.type
                
 