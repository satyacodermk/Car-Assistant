import numpy as np
import cv2
import pickle

#======================= Inintailize the web cam parameters,fonts and threshold ================================
frameWidth=640      #camera width
frameHeight=480     #camera height
brightness=180
threshold=0.75      #probablity threshold
font=cv2.FONT_HERSHEY_SIMPLEX


#=============================== Setup the video camera =======================================================
cap=cv2.VideoCapture(0)
cap.set(3,frameWidth) #3=> to specify the frame width
cap.set(4,frameHeight) #4=> to specify the frame height
cap.set(10,brightness) #10=> to specify the brightness

#====================================== import the trained model ==============================================
pickle_in=open("model_trained.p","rb") # rb=> read byte
model=pickle.load(pickle_in)

#============ Converting image to grayscale ===============
def grayscale(img):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img

#================ Applying histogram equalization to make image clear ===========================
def equalize(img):
    img=cv2.equalizeHist(img)
    return img

#========================= Image preprocessing =====================
def preprocessing(img):
    img=grayscale(img)
    img=equalize(img)
    img=img/255     #to normalize the image
    return img
#=========================== getting the class nmae ===================
def getCalssName(classNo):
    text=''
    if classNo==0:
        text=text+"speed limit 20 km/h"
    elif classNo==1:
        text=text+"speed limit 30 km/h"
    elif classNo==2:
        text=text+"speed limit 50 km/h"
    elif classNo==3:
        text=text+"speed limit 60 km/h"
    elif classNo==4:
        text=text+"speed limit 70 km/h"
    elif classNo==5:
        text=text+"speed limit 80 km/h"
    elif classNo==6:
        text=text+"end of speed limit 80 km/h"
    elif classNo==7:
        text=text+"speed limit 100 km/h"
    elif classNo==8:
        text=text+"speed limit 120 km/h"
    elif classNo==9:
        text=text+"No passing"
    elif classNo==10:
        text=text+"no passing for vehicles over 3.5 metric tons"
    elif classNo==11:
        text=text+"right of way at the next intersection"
    elif classNo==12:
        text=text+"priority road"
    elif classNo==13:
        text=text+"yield"
    elif classNo==14:
        text=text+"stop"
    elif classNo==15:
        text=text+"no vehicles"
    elif classNo==16:
        text=text+"vehicals ober 3.5 metric tons prohibited"
    elif classNo==17:
        text=text+"No entry"
    elif classNo==18:
        text=text+"general caution"
    elif classNo==19:
        text=text+"dangerous curve to the left"
    elif classNo==20:
        text=text+"dangerous curve to the right"
    elif classNo==21:
        text=text+"double curve"
    elif classNo==22:
        text=text+"bumpy road"
    elif classNo==23:
        text=text+"slippery road"
    elif classNo==24:
        text=text+"road narrows on the right"
    elif classNo==25:
        text=text+"road work"
    elif classNo == 26:
        text = text + "traffic signal"
    elif classNo == 27:
        text = text + "pedestrains"
    elif classNo == 28:
        text = text + "children crossing"
    elif classNo == 29:
        text = text + "bicycle crossing"
    elif classNo == 30:
        text = text + "beware of ice or snow"
    elif classNo == 31:
        text = text + "wild animals crossing"
    elif classNo == 32:
        text = text + "end of all speed and passing limits"
    elif classNo == 33:
        text = text + "turn right ahead"
    elif classNo == 34:
        text = text + "turn left ahead"
    elif classNo == 35:
        text = text + "ahead only"
    elif classNo == 36:
        text = text + "go straight or right"
    elif classNo == 37:
        text = text + "go straight or left"
    elif classNo == 38:
        text = text + "keep right"
    elif classNo == 39:
        text = text + "keep left"
    elif classNo == 40:
        text = text + "round about mandatory"
    elif classNo == 41:
        text = text + "end of no passing"
    elif classNo == 42:
        text = text + "end of no passing by vechiles over 3.5 metric tons"
    else:
        text=text+"Sorry no such Symbol is found"
    return text

while True:
    #=============== Read image =======================
    success,imgOriginal=cap.read()

    #====================== Process image -=============
    img=np.asarray(imgOriginal)
    img=cv2.resize(img,(32,32)) # resizing the image
    img=preprocessing(img)      #calling the preprocessing method to process image
    cv2.imshow("Processed Image",img)
    img=img.reshape(1,32,32,1)
    cv2.putText(imgOriginal,"calss:",(20,35),font,0.75,(0,0,255),2,cv2.LINE_AA)
    cv2.putText(imgOriginal,"Probability:",(20,75),font,0.75,(0,0,255),2,cv2.LINE_AA)

    #================= Predict image =================
    predictions=model.predict(img)
    #note that predict_calsses() function is depricted by the tensorflow
    #classIndex=model.predict_calsses(img)
    #use the following to get exact result as above code
    classIndex=np.argmax(model.predict(img),axis=-1)

    #probability value for the model
    probabilityValue=np.amax(predictions)

    if probabilityValue>threshold:
        #print(getCalssName(calssIndex)) # to get index of calss
        cv2.putText(imgOriginal,str(classIndex)+" "+str(getCalssName(classIndex)),(120,35),font,0.75,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(imgOriginal,str(round(probabilityValue*100,2))+"%",(180,75),font,0.75,(0,0,255),2,cv2.LINE_AA)
        cv2.imshow('Result',imgOriginal)

    if cv2.waitKey(1) and 0xFF==ord('q'):   #to exit the loop
        break


