import pyautogui
import cv2
import numpy as np
from datetime import datetime
from tkinter import * 
import os
from PIL import ImageTk, Image

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))

class Recorder:

  def __init__(self, live=False, gui=True):
    self.root = Tk()
    self.width = self.root.winfo_screenwidth()
    self.height = self.root.winfo_screenheight()
    self.fps = 30.0
    self.codec = cv2.VideoWriter_fourcc(*"XVID")
    self.live = live
    self.output_file = os.path.join(ABSOLUTE_PATH, "output\Recording_{}.avi".format(datetime.now().strftime("%d_%b_%y_%H_%M_%S").replace("/", "_")))
    self.writer = cv2.VideoWriter(self.output_file, self.codec, self.fps, (int(self.width), int(self.height)))
    self.recording = False
    self.rec_button = None
    self.stop_button = None
    self.imageFrame = None
    self.gui = gui
    self.called = gui
    if gui:
      self.initialize_gui_window()
  
  def initialize_gui_window(self):
    self.rec_button = Button(self.root, text="Start", command=self.rec, state=ACTIVE, bg="blue")
    self.rec_button.grid(row=1, column=1, padx=1, pady=5)
    self.stop_button = Button(self.root, text="Stop", command=self.stopRecording, state=DISABLED, bg="red")
    self.stop_button.grid(row=1, column=2, padx=1)
    self.imageFrame = Frame(self.root, width=int(self.width/1.5), height=int(self.height/1.5))
    self.imageFrame.grid()
    self.label = Label(self.imageFrame)
    self.label.grid()
    self.root.title('Screen Recorder')
    self.root.attributes("-topmost", 0)

  def isRecording(self):
    return self.recording

  def stopRecording(self):
    self.recording = False

  def stream(self):
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if self.gui:
      img = Image.fromarray(cv2.resize(frame, (int(self.width/1.5), int(self.height/1.5))))
      imgTk = ImageTk.PhotoImage(image=img)
      self.label.configure(image=imgTk)
      self.label.after(1, self.stream)
      self.save(frame)
    return True

  def rec(self):
    
    self.recording = True
    
    if self.gui:
      self.rec_button.config(state=DISABLED)
      self.stop_button.config(state=ACTIVE)  

    while self.isRecording():
      
      img = pyautogui.screenshot()
      frame = np.array(img)
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

      if self.gui:
        img = Image.fromarray(cv2.resize(frame, (int(self.width/1.5), int(self.height/1.5))))
        imgTk = ImageTk.PhotoImage(image=img)
        self.label.configure(image=imgTk)
        if self.called:
          self.label.after(1, self.rec)
          self.called = False
          self.root.mainloop()

      self.save(frame)

      if self.live and not self.gui:
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Live", int(self.width/1.5), int(self.height/1.5))
        cv2.imshow('Live', frame)
      
      if cv2.waitKey(1) == ord('q'):
          self.recording = False
          break
          
    self.writer.release()
    cv2.destroyAllWindows()

  def save(self, frame):
    self.writer.write(frame)


if __name__ == "__main__":
  r = Recorder(live=True, gui=False)
  r.rec()