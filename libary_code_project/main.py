from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import tkinter
import cv2
import PIL.Image,PIL.ImageTk
from threading import Thread
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d
import matplotlib
from data import data
from tkinter import messagebox

class App(object):
  def __init__(self):

    self.window = Tk()
    self.window.title('GUI LVTN')
    self.window.iconbitmap("ctu.ico")
    self.window.geometry('640x480')

    # On camera
    self.cap = cv2.VideoCapture(0)

    self.V_frame = tk.Frame(self.window) # the tich frame
    self.so_phan_chia_frame = tk.Frame(self.window) # so phan duoc chia
    self.the_tich_moi_phan_frame = tk.Frame(self.window) # the tich cua moi phan
    self.fig_frame = tk.Frame(self.window  ,padx=3.3, pady=3) # figure frame 
    self.img_frame = tk.Frame(self.window ,width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2,height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 3 + 42) # image frame
    
    self.menubar =  Menu(self.window, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
    self.menuBar()
    # header 
    self.label = Label(self.window, text='name')
    
    self.count = 0

    self.photo = None 

    self.creat_canvas_image()

    #Figure 
    self.fig = Figure(figsize=(3.1,2),dpi = 100)
    self.fig.tight_layout()

    self.canvas_plot()
    self.plot_data()
    self.plot_settings()
    

    # Image
    self.update_frame_image()
    
    #Layout
    self.layout()

    self.window.config(menu = self.menubar)
    self.window.mainloop()

  
  def canvas_plot(self):
    self.fig_canvas = FigureCanvasTkAgg(self.fig,self.fig_frame )
    self.fig_canvas.draw()

  def plot_settings(self):
    self.fig_canvas.get_tk_widget().pack(fill=BOTH)
    ax = self.fig.add_subplot(111, projection="3d")
    ax.grid(False)

    ax.set(xlim=(min(self.xs)*3,max(self.xs)*3), ylim=(min(self.ys)*3,max(self.ys)*3) , zlim = (min(self.zs)*3,max(self.zs)*3))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.axis('off')

    ax.scatter(self.xs, self.ys, self.zs, lw=0.01,color='black').set_sizes([2])


  def creat_canvas_image(self):
      self.canvas = Canvas(self.img_frame,width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2,height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 3 + 42,bg='white')

  def update_frame_image(self):
      ret , frame = self.cap.read()

      frame = cv2.resize(frame,dsize=None,fx = 0.5 , fy = 0.5)

      frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

      # Chuyển đổi ma trận điểm ảnh sang ảnh 
      self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

      self.canvas.create_image(0,0,image = self.photo , anchor =NW)

      self.count +=  1 

      # Thread cho phần sau
      if self.count % 10 == 0 :
        thread1 = Thread(target = self.printName )
        thread1.start()

      self.window.after(15,self.update_frame_image)

  def printName(self):
    pass

  def plot_data(self):
    self.xs = [1,2,3,4,5,6,7,8,9,10,11]
    self.ys = [1,2,3,4,5,6,7,8,9,10,11]
    self.zs = [1,2,3,4,5,6,7,8,9,10,11]

  def layout(self):
      self.label.grid(column=1 ,row= 0 )

      # Fill img_frame
      self.canvas.pack(fill=BOTH)

      self.fig_frame.grid(column=1,row=1)
      self.img_frame.grid(column=0,row=1)

  def menuBar(self):
    #File
    file = Menu(self.menubar, tearoff=1, background='#ffcc99', foreground='black')  
    file.add_command(label="New")  
    file.add_command(label="Open")  
    file.add_command(label="Save")  
    file.add_command(label="Save as")    
    file.add_separator()  
    file.add_command(label="Exit", command=self.window.quit)  
    self.menubar.add_cascade(label="File", menu=file)  

    #edit 
    edit = Menu(self.menubar, tearoff=0)  
    edit.add_command(label="Undo")  
    edit.add_separator()     
    edit.add_command(label="Cut")  
    edit.add_command(label="Copy")  
    edit.add_command(label="Paste")  
    edit.add_command(label = "Toolbar", command=self.ToolBar)
    self.menubar.add_cascade(label="Edit", menu=edit)  

    #help
    help = Menu(self.menubar, tearoff=0)  
    help.add_command(label="About", command=self.about)  
    self.menubar.add_cascade(label="Help", menu=help)

  def about(self):
    messagebox.showinfo('PythonGuides', 'Python Guides aims at providing best practical tutorials')

  def ToolBar(self):
    toolbar = NavigationToolbar2Tk(self.fig_canvas, self.fig_frame )
    toolbar.update()

if __name__ == '__main__':
  App()