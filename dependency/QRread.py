from qreader import QReader
import numpy as np
import cv2

qreader = QReader()

def Read(Image):
 decoded_text = []
 for item in Image: 
  image = cv2.cvtColor(cv2.imread(item), cv2.COLOR_BGR2RGB)
  decoded_text.append(qreader.detect_and_decode(image=image))
 return np.array(decoded_text)

def ReadCV(frame):
  decoded_text = []
  image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  decoded_text.append(qreader.detect_and_decode(image=image))
  if decoded_text is not None and len(decoded_text) > 0:
   return decoded_text
 