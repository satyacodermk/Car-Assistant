
# =============================== Importing all the required packages ==============================

# import OpenCV Library for basic image processing
import cv2
# import Numpy for array related operation proforming
import numpy as np
# import Dlib for deep learning based modules and face landmark detection
import dlib 
# import face_utils for basic operations of conversion
from imutils import face_utils
# import the carvis file to access speak function
import carvis
# time module to print FPS
import time

# defining the function that compute euclidean distance between two points
def compute(pta,ptb): #pta=> point A and ptb=> point B
    distance=np.linalg.norm(pta-ptb)
    return distance         # it must return the disatance calculated

#for one eye there are 6 points 
def blinked(a,b,c,d,e,f):
    try:
        up=compute(b,d)+compute(c,e)
        down=compute(a,f)
        ratio=up/(2.0*down) #using this ratio we can check weather eye is open or not

        if ratio>0.25: #eye is open
            return 2
        elif ratio>0.21 and ratio<=0.25:
            return 1
        else:
            return 0
    except:
        print("Error occur while detecting.....")


def d_detector():    
    # Opening the camera and taking the instance
    cap=cv2.VideoCapture(r'C:\car assistant\Testeye1.mp4')  #keep the first t capital of your test video because \t as its own meaning

    # from dlib initialize the detector and landmark detector, for extracting landmark points
    detector=dlib.get_frontal_face_detector() # it detects frontal face more reliable than haar-cascade files
    predictor=dlib.shape_predictor(r"C:\car assistant\shape_predictor_68_face_landmarks.dat") # returns face marks

    # Initialize variables will help to analyse the status (i.e. define for current state)
    sleep=0
    drowsy=0
    active=0
    status=""
    color=(0,0,0) #

    # Initialization for calculating FPS (Frame Per Second)
    prev_frame_time = 0
    new_frame_time = 0
    
    while True:
        _,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        faces=detector(gray)

        # Display FPS on window
        new_frame_time = time.time()  # to get new frame time
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = "FPS: " + str(int(fps))  # first convert fps to integer and then to string to pass this as text
        cv2.rectangle(frame, (5, 40), (150, 100), (255, 0, 0), 2)
        cv2.putText(frame, fps, (8, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # detect face in faces it will detect multiple frame for one faces so to avoid that we use loop
        for face in faces:
            x1=face.left()  
            y1=face.top()
            x2=face.right()
            y2=face.bottom()

            # Draw Frame for face detected
            face_frame=frame.copy()
            cv2.rectangle(face_frame,(x1,y1),(x2,y2),(0,255,0),2)

            # Predicting landmarks using predictor(img,face) function
            landmarks=predictor(gray,face) # getting all 68 landmarks by passing face detected
            landmarks=face_utils.shape_to_np(landmarks) # to convert it to numpy array shape
        
            # The numbers are actually the landmarks which will show eye and calling blinked function to get ratio
            left_blink=blinked(landmarks[36],landmarks[37],landmarks[38],landmarks[41],landmarks[40],landmarks[39])
            right_blink=blinked(landmarks[42],landmarks[43],landmarks[44],landmarks[47],landmarks[46],landmarks[45])


            # now judge what to do for the eye blinks
            if( left_blink==0 or right_blink==0):
                #print("left_blink=>",left_blink)
                #print("right_blink=>",right_blink)
                sleep+=1
                drowsy=0
                active=0
                # check code in this part only
                if (sleep>6):
                    status="Sleeping"
                    color=(255,0,0) # red color

            elif( left_blink==1 or right_blink==1):
                sleep=0
                active=0
                drowsy+=1
                if drowsy>6:
                    status="Drowsy"
                    print("Are you drowise...")
                    color=(0,0,255)
            else:
                drowsy=0
                sleep=0
                active+=1
                if active>6:
                    status="Active"
                    color=(0,255,0) #Green color

            cv2.putText(frame,status,(100,150),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)

            if status == "Drowsy":
                text = "are you drowsy please wake up"
                carvis.speak(text)

            elif status == "Sleeping":
                # print("count active=>",active)
                text = "Alert please wake up"
                carvis.speak(text)

            for n in range(0,68): # for 68 landmarks
                (x,y)=landmarks[n]
                cv2.circle(face_frame,(x,y),1,(255,0,0),-1)

        cv2.imshow("Drowsiness System", frame)



        # cv2.imshow("Drowsiness Detector",face_frame) #to check frame and landmarks detected
        # print("running")

        if cv2.waitKey(1) & 0xFF==ord('q'):  # press escape to exit the program
            text="It was nice time to assist you sir have a nice day"
            carvis.speak(text)
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    d_detector()