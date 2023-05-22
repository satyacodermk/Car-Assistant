import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy
import carvis as carvis
# ================================== load the trained model to classify sign ==========================================
from keras.models import load_model
model = load_model(r'C:\car assistant\traffic_classifier.h5')

# ================================ dictionary to label all traffic signs class. =======================================
classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)',
            3:'Speed limit (50km/h)',
            4:'Speed limit (60km/h)',
            5:'Speed limit (70km/h)',
            6:'Speed limit (80km/h)',
            7:'End of speed limit (80km/h)',
            8:'Speed limit (100km/h)',
            9:'Speed limit (120km/h)',
           10:'No passing',
           11:'No passing vehicle over 3.5 tons',
           12:'Right-of-way at intersection',
           13:'Priority road',
           14:'Yield',
           15:'Stop',
           16:'No vehicles',
           17:'Veh > 3.5 tons prohibited',
           18:'No entry',
           19:'General caution',
           20:'Dangerous curve left',
           21:'Dangerous curve right',
           22:'Double curve',
           23:'Bumpy road',
           24:'Slippery road',
           25:'Road narrows on the right',
           26:'Road work',
           27:'Traffic signals',
           28:'Pedestrians',
           29:'Children crossing',
           30:'Bicycles crossing',
           31:'Beware of ice/snow',
           32:'Wild animals crossing',
           33:'End speed + passing limits',
           34:'Turn right ahead',
           35:'Turn left ahead',
           36:'Ahead only',
           37:'Go straight or right',
           38:'Go straight or left',
           39:'Keep right',
           40:'Keep left',
           41:'Roundabout mandatory',
           42:'End of no passing',
           43:'End no passing veh > 3.5 tons' }

# ========================================== Traffic_recognizer Open Traffic Recognizer window ===========================
def traffic_recognizer():
    # ============================= classify the image or predict traffic sign ================================================
    def classify(file_path):
        global label_packed
        image = Image.open(file_path).convert("RGB")
        cvimg = numpy.asarray(image)
        # cv2.imshow("Image", cvimg)
        image = image.resize((30, 30), Image.ANTIALIAS)
        image = numpy.array(image.getdata()).reshape(-1, 30, 30, 3)
        print(image.shape)
        # pred = model.predict_classes([image])
        pred = model.predict([image])
        class_pred = numpy.argmax(pred, axis=1)
        pred = class_pred[0]  # to get class index
        sign = classes[pred + 1]
        print(sign + " index=>", (pred + 1))
        # ============= use of voice ================================
        text = "This symbol is tells about " + sign
        carvis.speak(text)
        status="Status: "+sign
        label.configure(text=status)


    # =================================== Image processing ===============

    def showgrayimg(file_path):
        img = Image.open(file_path)
        img = img.convert('L')
        img.thumbnail((300, 300))
        final_img = ImageTk.PhotoImage(img)
        gray_img = Label(topWind)
        gray_img.configure(image=final_img)
        gray_img.image = final_img
        gray_img.place(x=300, y=240)

    def showbinaryimage(file_path):
        img = Image.open(file_path)
        img = img.convert('1', dither=Image.NONE)
        img.thumbnail((300, 300))
        final_img = ImageTk.PhotoImage(img)

        gray_img = Label(topWind)
        gray_img.configure(image=final_img)
        gray_img.image = final_img
        gray_img.place(x=300, y=240)

    def showFeatureimage(file_path):
        img=cv2.imread(file_path)
        gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Creating the function
        fast=cv2.FastFeatureDetector_create()
        #fast.setNonmaxSupperssion(False)

        # drawing the keypoints or feature points
        feature=fast.detect(gray_img,None)
        img=cv2.drawKeypoints(img,feature,None,color=(0,255,0))

        # to show image use pillow functions
        img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        pil_image=Image.fromarray(img_rgb)
        pil_image.thumbnail((300, 300))
        final_img = ImageTk.PhotoImage(pil_image)

        gray_img = Label(topWind)
        gray_img.configure(image=final_img)
        gray_img.image = final_img
        gray_img.place(x=300, y=240)

    # ========================= Display More Buttons ======================================================
    def showAllButton():
        # =============================================== Display different buttons to show image processing options =====================================
        show_gray_img = Button(topWind, text="Gray Image", font=('helvetica', 15, 'bold'), bg='#00ffff', fg='#ff99ff',command=lambda path=file_path:showgrayimg(path))
        show_gray_img.place(x=630, y=240)

        show_feature_img = Button(topWind, text="Extract Feature", font=('helvetica', 15, 'bold'), bg='#00ffff',fg='#ff99ff',command=lambda path=file_path:showFeatureimage(path))
        show_feature_img.place(x=630, y=300)

        show_Binary_img = Button(topWind, text="Binary Image", font=('helvetica', 15, 'bold'), bg='#00ffff',fg='#ff99ff',command=lambda path=file_path:showbinaryimage(path))
        show_Binary_img.place(x=630, y=360)

        show_exit = Button(topWind, text="Exit", font=('helvetica', 15, 'bold'), bg='#00ffff',
                                 fg='#ff99ff', command=topWind.destroy)
        show_exit.place(x=630, y=420)


    # ================================== after uploading image display classify button which call classify function  ================================
    def show_classify_button(file_path):
        classify_b = Button(topWind, text="Classify sign", padx=10, pady=5, command=lambda: classify(file_path))
        classify_b.configure(background='#00ffff', foreground='#ff99ff', font=('helvetica', 15, 'bold'))
        classify_b.place(x=390,y=520)

    def upload_image():
        try:
            global file_path
            file_path = filedialog.askopenfilename()
            uploaded = Image.open(file_path)
            # to display uploaded image
            sign_image = Label(topWind)
            sign_image.place(x=50, y=240)

            #uploaded.thumbnail(((topWind.winfo_width() / 2.25), (topWind.winfo_height() / 2.25)))
            uploaded.thumbnail((300,300))
            im = ImageTk.PhotoImage(uploaded)
            sign_image.configure(image=im)
            sign_image.image = im

            label.configure(text='Status: Image Selected,(Now Click on Classify Button)')
            status="Status Image Selected Now Click on Classify Button"
            carvis.speak(status)
            show_classify_button(file_path)
            showAllButton()
        except:
            pass

    # =============================================== initialise GUI ===================================================================
    topWind = tk.Toplevel()
    topWind.geometry('800x600+70+50')
    topWind.title('Traffic Symbol Detection and Recognise ( TSDR )')
    topWind.configure(background='#6699ff')

    label = Label(topWind,text="Status: Select Image",fg="#00ff00", background='#6699ff', font=('helvetica', 18, 'bold'),borderwidth=1,relief='ridge',padx=10,pady=5)

    upload = Button(topWind, text="Upload", command=upload_image, padx=10, pady=5)
    upload.configure(background='#00ffff', foreground='#ff99ff', font=('helvetica', 15, 'bold'))


    # ========================= placing widgets on tkinter window =========================================
    upload.place(x=250,y=520)

    label.place(x=110,y=120)

    heading = Label(topWind, text="Classify Traffic Sign", padx=20,pady=10, font=('helvetica', 20, 'bold'),borderwidth=2,relief='ridge')
    heading.configure(fg="black",bg="#12ff21")
    heading.place(x=250,y=20)

    # ============================== Adding voice command ======================
    text="Welcome to TSDR System"
    carvis.speak(text)
    status="To Classify image please upload image, by clicking on Upload button"
    carvis.speak(status)

    topWind.mainloop()

if __name__=='__main__':
    traffic_recognizer()