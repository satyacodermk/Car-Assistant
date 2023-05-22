import tkinter as tk

import drowsiness as dd

"""
def on_enter(e):
    start_but.config(bg='blue',fg='red')

def on_leave(e):
    start_but.config(bg='green',fg='black')
"""

def start_app():
    root=tk.Tk() #creating window
    root.title('Drowiness Detector')
    root.geometry("700x500+250+100") #700=>width, 500=>height, 250=> form left 100=> from top
    root.resizable(False,False)
    root.config(bg="blue")   
    #adding label
    main_title=tk.Label(root,text="Welcome To Car Assistant",font=('Arial',25),fg='#12ff21',bg="blue")
    main_title.place(x=150,y=200)

    #adding the button to call the d_detector function to start the window
    start_but=tk.Button(root,text="Start Detecting",font=("Arial",20),fg="blue",bg="green",command=dd.d_detector) #command will call the function
    start_but.place(x=240,y=250)
    
    #applying the hover effect using event in tkinter use bind function to bind elements
    def on_enter(e):
        start_but.config(bg='white',fg='blue')

    def on_leave(e):
        start_but.config(bg='green',fg='black')


    start_but.bind('<Enter>',on_enter)
    start_but.bind('<Leave>',on_leave)

    tk.mainloop()


if __name__=="__main__":
    start_app()  #calling the start function