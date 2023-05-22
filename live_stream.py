# ===================== Showing opencv video inside tkinter frame ==========================================
from tkinter import *
from PIL import ImageTk,Image
import cv2
"""

# flag
flag=True

root=Tk()
root.geometry("600x600+100+50")
root.configure(background='#6699ff')
# create a frame
app=Frame(root,bg="white",borderwidth=2,relief="ridge")
app.place(x=100,y=100)

# create a label in the frame
lmain=Label(app) # to add label as image
lmain.grid()

# stop function
def stop_video():
    global flag
    flag=False

# creating buttons
stop_but=Button(root,text="Stop",font=('helvatica',20,'bold'),background='#00ffff', foreground='#ff99ff',command=stop_video)
stop_but.place(x=150,y=450)

# resume function
def resume_video():
    global flag
    flag = True
    video_stream()

# creating buttons
resume_but = Button(root, text="Resume", font=('helvatica', 20, 'bold'),background='#00ffff', foreground='#ff99ff',command=resume_video)
resume_but.place(x=240, y=450)

# capture from camera
cap=cv2.VideoCapture(r'C:\car assistant\Testeye1.mp4')


#function for video streaming
def video_stream():
    global flag
    # get the frame from video capture
    _,frame=cap.read()
    # image to rgb
    cv2image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
    # convert array into image using pillow
    img=Image.fromarray(cv2image)
    # resize the image
    img.thumbnail((400,400))
    # convert image to tkinter image using PhotoImage
    imgtk=ImageTk.PhotoImage(image=img)

    lmain.imgtk=imgtk
    lmain.configure(image=imgtk)
    if flag==True:
        lmain.after(1,video_stream)

video_stream()
root.mainloop()
"""
class videoGUI: