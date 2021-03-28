import pyautogui
import cv2
import numpy as np
from datetime import datetime
from tkinter import * 
from tkinter.ttk import *
import os

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))

class Recorder:

  def __init__(self, live=False):
    self.width = Tk().winfo_screenwidth()
    self.height = Tk().winfo_screenheight()
    self.fps = 30.0
    self.codec = cv2.VideoWriter_fourcc(*"XVID")
    self.live = live
    self.output_file = os.path.join(ABSOLUTE_PATH, "output\Recording_{}.avi".format(datetime.now().strftime("%d_%b_%y_%H_%M_%S").replace("/", "_")))
    self.writer = cv2.VideoWriter(self.output_file, self.codec, self.fps, (int(self.width), int(self.height)))
  
  def rec(self):

    while True:

      img = pyautogui.screenshot()
      frame = np.array(img)
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      self.save(frame)

      if self.live:
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Live", int(self.width/1.5), int(self.height/1.5))
        cv2.imshow('Live', frame)
      
      if cv2.waitKey(1) == ord('q'):
          break
    
    self.writer.release()
    cv2.destroyAllWindows()

  def save(self, frame):
    self.writer.write(frame)


if __name__ == "__main__":
  r = Recorder(live=True)
  print(r.output_file)
  r.rec()