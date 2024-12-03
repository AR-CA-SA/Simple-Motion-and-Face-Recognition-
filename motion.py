from picamera2 import Picamera2
import cv2
import numpy as np
from datetime import datetime



def getCurrentstate(isMoving):
    current_time = datetime.now()
    if isMoving:
        print("Movement has been detected | Time : ", current_time)
    else:
        print("No movement detected | Time : ", current_time)

def motionMain():

    picam2 = Picamera2()

    # Load pre-trained Haar cascades for face and eye detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    preview_config = picam2.create_preview_configuration()
    picam2.configure(preview_config)
    picam2.start()

    prev_frame = None
    movement_detected = False 

    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray_frame
            continue

     
        frame_diff = cv2.absdiff(prev_frame, gray_frame)
        _, thresh_frame = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

      
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = None
        max_area = 0

     
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:  
                if area > max_area:
                    largest_contour = contour
                    max_area = area
                    cv2.putText(frame, "Movement Detected", (100, 100), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=1.0, color=(0, 0, 255))
        
                    if  not movement_detected: 
                        getCurrentstate(True)  
                        movement_detected = True  
           
        if largest_contour is None and movement_detected:
           
            getCurrentstate(False)  
            movement_detected = False  

   
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
         
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
       


            roi_gray = gray_frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:

                cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 0, 255), 2)


        cv2.imshow("Motion Detection with Face and Eye Recognition", frame)

        prev_frame = gray_frame

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    picam2.stop()
    cv2.destroyAllWindows()
