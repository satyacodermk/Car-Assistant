# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
# face_utils for basic operations of conversion
from imutils import face_utils
# import time module
import time
# import carvis
import carvis as carvis


blink_ratio=0
def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist


def blinked(a, b, c, d, e, f):
    global blink_ratio
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    blink_ratio=ratio

    # Checking if it is blinked
    if (ratio > 0.25):
        return 2
    elif (ratio > 0.21 and ratio <= 0.25):
        return 1
    else:
        return 0


def d_detector():
    global blink_ratio
    # Initializing the camera and taking the instance
    cap = cv2.VideoCapture(r'C:\car assistant\Testeye1.mp4')

    # Initializing the face detector and landmark detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # status marking for current state
    sleep = 0
    drowsy = 0
    active = 0
    status = ""
    color = (0, 0, 0)
    # Initialization for calculating FPS (Frame Per Second)
    prev_frame_time = 0
    new_frame_time = 0
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame=cv2.resize(frame,(800,700))
        # Display FPS on window
        new_frame_time = time.time()  # to get new frame time
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = "FPS: " + str(int(fps))  # first convert fps to integer and then to string to pass this as text
        cv2.rectangle(frame, (5, 40), (140, 100), (255, 0, 0), 2)
        cv2.putText(frame, fps, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        faces = detector(gray)
        # detected face in faces array
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            face_frame = frame.copy()
            cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            # The numbers are actually the landmarks which will show eye
            left_blink = blinked(landmarks[36], landmarks[37],
                                 landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43],
                                  landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            # ==================== Now judge what to do for the eye blinks ======================
            if (left_blink == 0 or right_blink == 0):
                sleep += 1
                drowsy = 0
                active = 0
                if (sleep > 6):
                    status = "Sleeping"
                    color = (255, 0, 0)

            elif (left_blink == 1 or right_blink == 1):
                sleep = 0
                active = 0
                drowsy += 1
                if (drowsy > 6):
                    status = "Drowsy"
                    color = (0, 0, 255)

            else:
                drowsy = 0
                sleep = 0
                active += 1
                if (active > 6):
                    status = "Active"
                    color = (0, 255, 0)
            # =========================== Display Eye Status ==============================
            lefteye,righteye="",""
            if left_blink==0:
                lefteye="Closed"
            else:
                lefteye="Open"

            if right_blink==0:
                righteye="Closed"
            else:
                righteye="Open"

            l_eye="Left Eye: "+lefteye
            r_eye="Right Eye: "+righteye

            cv2.putText(frame,"Eye Status" , (430, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, l_eye, (430, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, r_eye, (430, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # =========================== Display Blink ratio =============================
            rationstatus="Blink Ratio: "+str(round(blink_ratio,2))
            cv2.putText(frame, rationstatus, (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # =========================== Showing the status ==================================
            textstatus="Status: "+status
            cv2.putText(frame, textstatus, (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # ===================== if drowsy or sleeping driver then alarming ==================
            if status == "Drowsy":
                text = "are you drowsy please wake up"
                carvis.speak(text)

            elif status == "Sleeping":
                # print("count active=>",active)
                text = "Alert please wake up"
                carvis.speak(text)


            for n in range(0, 68):
                (x, y) = landmarks[n]
                cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

        # ========================== resizing the window =======================
        cv2.namedWindow("Drowsiness System",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Drowsiness System",800,700)
        cv2.imshow("Drowsiness System", frame)
        # cv2.imshow("Result of detector", face_frame
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
if __name__=='__main__':
    d_detector()