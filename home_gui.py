# from tkinter import *
# from tkinter import ttk
# from PIL import Image,ImageTk
from carvis import *
from testdrowsiness import *
from traffic import *


# ======================================== Main Page or Home page =======================================

def main_page():
    # call change function present in carvis file( module )
    change()
    root1 = Toplevel()
    #fix the window size
    root1.title("Carvis-Car Assistant")
    root1.geometry("900x500+100+100")
    root1.resizable(False,False) #if we want to change the image dynamically then comment this

    # ========================== To resize the background image =============================
    def resize_image(event):
        new_width = event.width     #getting new width after event is called
        new_height = event.height   #getting new width after evetn is called
        image = copy_of_image.resize((new_width, new_height))   #resize function is used to resize image
        photo=ImageTk.PhotoImage(image) #conveting phtoimage to tkinter image
        label.config(image=photo)   #setting the background image
        label.image=photo   #to avoid garbage collection

    #=========================== Set background image =========================================
    image=Image.open("C:\car assistant\car1img.jfif")
    copy_of_image=image.copy()
    photo=ImageTk.PhotoImage(image)
    label=ttk.Label(root1,image=photo)
    label.bind('<Configure>',resize_image)
    label.pack(fill=BOTH,expand=YES)

    #============================== Dropdown combobox ================================================
    options=["Select","Traffic Recognize","Detect Drowsiness"]
    clicked=StringVar()
    #setting the default mode as select
    clicked.set(options[0])

    # ====================================== Get Selected for checking purpose ========================
    def get_selected(event):
        mode=clicked.get()
        print("Get selected called=>"+mode)
        #return mode
    # ================================= Test function-> for testing purpose ===============================
    # ================================== Go live ======================
    def go_live():
        mode=clicked.get()
        print("Mode Selected in go live=>",mode)
        if mode=="Detect Drowsiness":
            text="Wait the DDD system is get activated"
            speak(text)
            d_detector()
            # root1.destroy()
        elif mode=="Traffic Recognize":
            text="Wait the TDRS System is get activated"
            speak(text)
            traffic_recognizer()
        else:
            text="Selected option is not available"
            print("Selected option is not available...")
            speak(text)

    # function called after selected the mode
    def test_selected(flag):
        mode=clicked.get()
        print("Selected Option=",mode)
        speak("Hye you have selected "+mode)
        if flag==1:
            return mode
        else:
            print("no mode selected")
    def test_selected1():
        mode=clicked.get()
        print("Selected Option=",mode)
        speak("Hye you have selected "+mode)

    # ======================================= Select drop down menu ============================
    drop=OptionMenu(root1,clicked,*options,command=get_selected) # the * astric symbol show variablearguments
    #mode=clicked.get() #get() function is used to get selected value
    #print("Selected Option=",mode)
    drop.config(bg="#12ff21",fg="blue",font=("helvetica",10,'bold'))
    drop.place(x=730,y=150)
    print(drop)
    mode=clicked.get()
    # ============================================= check button ===========================================
    test_but=Button(root1,text="Test Mode",font=("helvetica",15,'bold'),fg="#f3f3f3",bg="#12ff21",command=test_selected1)
    test_but.place(x=730,y=250)

    # ============================== Adding text and buttons for making UI interactive ===================
    head_text=Label(root1,text="Welcome, I am Carvis ",font=("helvetica",30,'bold'),fg="#12ff21",bg="black")
    head_text.place(x=250,y=50)

    activate_crvs=Button(root1,text="Acivate Carvis",font=("helvetica",15,'bold'),fg="#f3f3f3",bg="#12ff21",command=lambda m=mode:gui_carvis(m))
    activate_crvs.place(x=50,y=150)
    #Add buttons to root window
    live_btn=Button(root1,text="Go Live!",font=("helvetica",20,"bold"),fg="#f3f3f3",bg="#12ff21",command=go_live)
    live_btn.place(x=50,y=250)

    #Add Learn more button
    learn_btn=Button(root1,text="Learn",font=("helvetica",15,'bold'),fg="#f3f3f3",bg="#12ff21")
    learn_btn.place(x=50,y=350)

    root1.mainloop() #,width=15,height=10

#========================================== Carvis Setting Windows ==================================
def gui_carvis(mode):
    root = Toplevel()
    # fix the window size
    root.title("Carvis-Setting")
    root.geometry("500x300+300+200")
    root.resizable(False, False)  # if we want to change the image dynamically then comment this
    # root.iconbitmap() #specify the icon i.e. .ico

    # exception handling for background image
    try:
        # To resize the background image
        def resize_image(event):
            new_width = event.width  # getting new width after event is called
            new_height = event.height  # getting new width after evetn is called
            image = copy_of_image.resize((new_width, new_height))  # resize function is used to resize image
            photo = ImageTk.PhotoImage(image)  # conveting phtoimage to tkinter image
            label.config(image=photo)  # setting the background image
            label.image = photo  # to avoid garbage collection

        # =========================== Set background image =========================================
        image = Image.open("C:\car assistant\jarv1.png")
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(root, image=photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=BOTH, expand=YES)
    except:
        root.config(bg="#0f0f0f")

    # ========================== Applying the changes made by the User =======================

    def apply():
        #print(hor_slid.get()) #comment out to check value
        #==================== Speed Setup ===================
        # changing speed
        engine.setProperty('rate',int(hor_slid.get()))
        # changing the voice type male or female
        voices=engine.getProperty('voices')
        #print(voices)
        voice_type=clicked.get() # to get selected item
        print(voice_type)
        if voice_type=="Male":
            i=0
        else:
            i=1
        engine.setProperty('voice',voices[i].id)

        #==================== Volume Setup ===================
        new_vol=int(hor_slid_volume.get())/100
        print(new_vol)
        engine.setProperty("volume",new_vol)


    # =================================== Slider for Speed Setup ===================

    set_speed=Label(root,text="Set Voice Speed ", font=("helvetica", 15, 'bold'), fg="#f3f3f3", bg="#0f0f0f")
    set_speed.place(x=10,y=50)
    hor_slid=Scale(root,from_=50,to=300,orient=HORIZONTAL)
    hor_slid.config(bg="#0f0f0f",fg="#ffffff",sliderlength=10,length=200) #length to fix how longer should the slider
    hor_slid.place(x=200,y=50)
    speed=hor_slid.get() # return the value selected
    print(speed)

    # ========================= Slider for Volume Setup =======================================
    set_volume=Label(root,text="Set Voice Speed ", font=("helvetica", 15, 'bold'), fg="#f3f3f3", bg="#0f0f0f")
    set_volume.place(x=10,y=100)
    hor_slid_volume=Scale(root,from_=0,to=100,orient=HORIZONTAL)
    hor_slid_volume.config(bg="#0f0f0f",fg="#ffffff",sliderlength=10,length=200) #length to fix how longer should the slider
    hor_slid_volume.place(x=200,y=100)
    volume_set=hor_slid_volume.get() # return the value selected
    print(volume_set)


    # ====================== Select Voice type male or female ==========
    options=["Male","Female"]
    clicked=StringVar()
    # setting the default mode as select
    clicked.set(options[0])
    drop=OptionMenu(root,clicked,*options) # the * astric symbol show variablearguments
    # mode=clicked.get() #get() function is used to get selected value
    #print("Selected Option=",mode)
    set_type= Label(root,text="Set Voice Type ", font=("helvetica", 15, 'bold'), fg="#f3f3f3", bg="#0f0f0f")
    set_type.place(x=10, y=150)
    drop.config(bg="#12ff21",fg="blue",font=("helvetica",10,'bold'))
    drop.place(x=200,y=150)

    # ============================= Apply button to apply the changes made =========================
    aply_but=Button(root,text='Apply',font=("helvetica", 15, 'bold'), fg="#f3f3f3", bg="#12ff21",
                      command=apply)
    aply_but.place(x=170,y=230)

    # root.config(bg="#0f0f1f")
    text = "Welcome I am Carvis this is me your friend"+mode
    test_but = Button(root, text="Test Voice", font=("helvetica", 15, 'bold'), fg="#f3f3f3", bg="#12ff21",
                      command=lambda a=text: speak(a))
    test_but.place(x=270, y=230)

    root.mainloop()

# ==================================== change function ===========================================

def change():
    user_name = name.get()
    print(user_name)
    greetUser(user_name)
    text=Label(windroot,text="Carvis is running....",font=("helvetica", 15, 'bold'), fg="#12ff21", bg="black")
    text.place(x=50,y=20)
    exit_btn=Button(windroot,text="Exit",font=("helvetica", 15, 'bold'), fg="#f3f3f3", bg="#12ff21",command=lambda a=user_name:[byfun(a),windroot.destroy()])
    exit_btn.place(x=120,y=100)
    start_but.place(x=190,y=100)

# ======================================== running the main app ==========
if __name__=='__main__':
    windroot=Tk()
    windroot.geometry("500x200+300+200")
    windroot.config(bg="black")
    # ====================== Label to show details ================
    name_txt=Label(windroot,text="Enter your name ",font=("helvetica", 15, 'bold'), fg="#12ff21", bg="black")
    name_txt.place(x=0,y=50)
    # ================ Taking user name ===================
    name=StringVar()
    name_box=Entry(windroot,textvariable=name)
    name_box.config(font=('helvetica',15,'bold'))
    name_box.place(x=200,y=50)

    #use of lambda to call multiple functions at a time, note=> put all functions in list
    start_but=Button(text="Start",font=('helvetica',15,'bold'),bg="#12ff21",fg="#ffffff",command=lambda :[main_page()])
    start_but.place(x=120,y=100)

    windroot.mainloop()
    # ============================= to run only main page but not make as whole working of it ===========================
    # main_page()

