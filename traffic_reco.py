import numpy as np
import cv2
from carvis import *
# load the trained model to classify sign
from PIL import ImageTk, Image
from keras.models import load_model
model = load_model('traffic_classifier.h5')

# ================= Dictionary that helps to get the calss name =======================================
#dictionary to label all traffic signs class.
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
           17:'Vehicle > 3.5 tons prohibited',
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


#============ Converting image to grayscale ===============
def grayscale(img):
    img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    return img

#================ Applying histogram equalization to make image clear ===========================
def equalize(img):
    img=cv2.equalizeHist(img)
    return img

# ========================= Image preprocessing =====================
def preprocessing(img):
    img=grayscale(img)
    img=equalize(img)
    img=img/255     #to normalize the image
    return img

#
#
# # ======================= Inintailize the web cam parameters,fonts and threshold ================================
frameWidth=640      # camera width
frameHeight=480     # camera height
brightness=180
threshold=0.75      #  threshold
font=cv2.FONT_HERSHEY_SIMPLEX


def traffic_recognization():

    # =============================== Setup the video camera =======================================================
    cap = cv2.VideoCapture(r"C:\car assistant\Test_traffic.mp4")
    cap.set(3, frameWidth)  # 3=> to specify the frame width
    cap.set(4, frameHeight)  # 4=> to specify the frame height
    cap.set(10, brightness)  # 10=> to specify the brightness

    while True:
        # =============== Read image =======================
        success, imgOriginal = cap.read()

        # ====================== Process image -=============

        """
        image=image.resize((30,30),Image.ANTIALIAS)
        image=numpy.array(image.getdata()).reshape(-1,30,30,3)
        """
        imgOriginal = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
        img = np.asarray(imgOriginal)
        img = cv2.resize(img, (30,30))  # resizing the image
        img=np.array(img).reshape(-1,30,30,3)
        #img = preprocessing(img)  # calling the preprocessing method to process image
        #cv2.imshow("Processed Image", img)
        img = img.reshape(-1, 30, 30, 3)
        cv2.putText(imgOriginal, "calss:", (20, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(imgOriginal, "Probability:", (20, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

        # ================= Predict image =================
        # pred = model.predict_classes([image])
        pred = model.predict([img])
        class_pred = np.argmax(pred, axis=1)
        pred = class_pred[0]  # to get class index
        sign = classes[pred + 1]
        print(sign + " index=>", (pred + 1))
        # ==================================
        # predictions = model.predict([img])
        # # note that predict_calsses() function is depricted by the tensorflow
        # # classIndex=model.predict_calsses(img)
        # # use the following to get exact result as above code
        # classIndex = np.argmax(model.predict([img]), axis=-1)
        # print(classIndex)
        #
        # # probability value for the model
        # probabilityValue = np.amax(predictions)

        # if probabilityValue > threshold:
        #     # print(classes(calssIndex)) # to get index of calss
        #     #speak(classes[classIndex])
        #
        #     cv2.putText(imgOriginal, str(classIndex) + " " + str(classes[classIndex]), (120, 35), font, 0.75,
        #                 (0, 0, 255), 2, cv2.LINE_AA)
        #     cv2.putText(imgOriginal, str(round(probabilityValue * 100, 2)) + "%", (180, 75), font, 0.75, (0, 0, 255), 2,
        #                 cv2.LINE_AA)
        cv2.imshow('Result', imgOriginal)

        if cv2.waitKey(0) and 0xFF == ord('q'):  # to exit the loop
            break


if __name__=='__main__':
    traffic_recognization()
