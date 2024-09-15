import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import mediapipe as mp
import random
from tensorflow.keras.models import load_model
import streamlit as st
import keyboard as key
import os


mpHolistic = mp.solutions.holistic #holistic model
mpDrawing = mp.solutions.drawing_utils #drawing utils


def mediaDetect(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #color conversion
    image.flags.writeable = False #no longer writeable
    results = model.process(image) #make predictions
    image.flags.writeable = True #image now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #color conversion 
    return image, results


def drawLandMarks(image, results):
    mpDrawing.draw_landmarks(image, results.face_landmarks, mpHolistic.FACEMESH_TESSELATION) #draws face connections/landmarks
    mpDrawing.draw_landmarks(image, results.pose_landmarks, mpHolistic.POSE_CONNECTIONS) #draws pose connections/landmarks
    mpDrawing.draw_landmarks(image, results.right_hand_landmarks, mpHolistic.HAND_CONNECTIONS) #draws right hand connections/landmarks
    mpDrawing.draw_landmarks(image, results.left_hand_landmarks, mpHolistic.HAND_CONNECTIONS) #draws left hand connections/landmarks
    

def extractKeypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])  


def styledLandMarks(image, results):
    
    mpDrawing.draw_landmarks(image, results.face_landmarks, mpHolistic.FACEMESH_TESSELATION,
                            mpDrawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1), 
                            mpDrawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)) 
                             #draws face connections/landmarks
        
    mpDrawing.draw_landmarks(image, results.pose_landmarks, mpHolistic.POSE_CONNECTIONS,
                            mpDrawing.DrawingSpec(color=(80, 22, 10), thickness=1, circle_radius=1), 
                            mpDrawing.DrawingSpec(color=(80, 44, 121), thickness=1, circle_radius=1))
                            #draws pose connections/landmarks
        
    mpDrawing.draw_landmarks(image, results.right_hand_landmarks, mpHolistic.HAND_CONNECTIONS,
                            mpDrawing.DrawingSpec(color=(121, 22, 76), thickness=1, circle_radius=1), 
                            mpDrawing.DrawingSpec(color=(121, 44, 250), thickness=1, circle_radius=1)) 
                            #draws right hand connections/landmarks
        
    mpDrawing.draw_landmarks(image, results.left_hand_landmarks, mpHolistic.HAND_CONNECTIONS,
                            mpDrawing.DrawingSpec(color=(245, 117, 66), thickness=1, circle_radius=1), 
                            mpDrawing.DrawingSpec(color=(245, 66, 230), thickness=1, circle_radius=1)) 
                            #draws left hand connections/landmarks


ASL_translate = load_model(r"C:\Users\Alex_\Desktop\Computer-Vision-with-Python\Computer-Vision-with-Python\OPENASL.h5")

actions = dict()
for x in os.listdir(r"C:\Users\Alex_\Desktop\MP_Data"):
    	actions[int(x.split("_")[1])] = x.split("_")[0]


showFlag = True 
frameCount = 0
frameCache = []

def TRANSLATE():
    cap = cv2.VideoCapture(0)
    framePlaceHolder = st.empty()

    with mpHolistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            global showFlag, frameCount, frameCache
            ret, frame = cap.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frameHeight  = cap.get(3)
            frameWidth = cap.get(4)

            if showFlag == True:
                cv2.putText(frame, "START MOVEMENT: Enter 's' to begin", (40, 200),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                framePlaceHolder.image(frame, channels="RGB")

            elif showFlag == False:
                if frameCount <= 29:
                    detectedImage, results = mediaDetect(frame, holistic)
                    cv2.putText(detectedImage, "RECORDING MOVEMENT", (120, 120),
                                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    styledLandMarks(detectedImage, results)
                    frameCache.append(extractKeypoints(results))
                    frameCount += 1
                    framePlaceHolder.image(detectedImage, channels="RGB")

                else:
                    showFlag = True
                    frameCacheArray = np.array(frameCache)
                    frameCacheArray = np.expand_dims(frameCacheArray, axis=0)
                    print(frameCacheArray.shape)

            if key.is_pressed("t"):
                    randomKey = random.randint(0, 1000000)
                    translation = ASL_translate(frameCacheArray)
                    translation = np.argmax(translation)
                    st.text_area("ASL translation: ", actions[translation], key=randomKey)

            if key.is_pressed("q"):
                zeros = np.zeros((int(frameWidth), int(frameHeight)))
                framePlaceHolder.image(zeros, channels="RGB")
                break

            if key.is_pressed("s"):
                showFlag = False 
                frameCount = 0
                frameCache = []

        cap.release()
        cv2.destroyAllWindows()



savePath = fr"C:\Users\Alex_\Desktop\MP_Data"
length = len(os.listdir(r"C:\Users\Alex_\Desktop\MP_Data"))

def RECORDNCACHE(word):
    
    cap = cv2.VideoCapture(0)
    framePlaceHolder = st.empty()

    #Reminder: savePath = fr"C:\Users\Alex_\Desktop\MP_Data"
    wordPath = os.path.join(savePath, word)

    checkSet = []
    for x in range(length):
        if os.path.isdir(wordPath+f"_{x}"):
            wordPath = wordPath+f"_{x}"
            checkSet.append(1)
        
        else:
            checkSet.append(0)
    
    if sum(checkSet) == 0:
        os.mkdir(wordPath+f"_{length}")
        wordPath = wordPath+f"_{length}"
   
    
    files = os.listdir(wordPath)
    instanceCount = len(files)
    folderPath = os.path.join(wordPath, str(instanceCount))
    
    try:
        os.mkdir(folderPath)
    except: 
        pass


    with mpHolistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            global showFlag, frameCount, frameCache
            ret, frame = cap.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frameHeight  = cap.get(3)
            frameWidth = cap.get(4)


            if showFlag == True:
                cv2.putText(frame, "START MOVEMENT: Enter 's' to begin", (40, 200),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                framePlaceHolder.image(frame, channels="RGB")

            elif showFlag == False:
                if frameCount <= 29:
                    
                    detectedImage, results = mediaDetect(frame, holistic)
                    cv2.putText(detectedImage, "RECORDING MOVEMENT", (120, 120),
                                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    
                    styledLandMarks(detectedImage, results)
                    keyPnts = extractKeypoints(results)
                    frameCache.append(keyPnts)
                    framePlaceHolder.image(detectedImage, channels="RGB")
                    
                
                    filePath = os.path.join(folderPath, str(frameCount)+".npy")
                    arrayFile = open(filePath, "wb")
                    np.save(arrayFile, keyPnts)

                    frameCount += 1

                else:
                    showFlag = True
                    frameCacheArray = np.array(frameCache)
                    frameCacheArray = np.expand_dims(frameCacheArray, axis=0)
                    print(frameCacheArray.shape)

            #Unecessary stuff but could be useful one day
            if key.is_pressed("t"):
                    translation = ASL_translate(frameCacheArray)
                    translation = np.argmax(translation)
                    st.write("ASL translation: ", actions[translation])

            if key.is_pressed("q"):
                zeros = np.zeros((int(frameWidth), int(frameHeight)))
                framePlaceHolder.image(zeros, channels="RGB")
                break

            if key.is_pressed("s"):
                showFlag = False 
                frameCount = 0
                frameCache = []
      
        cap.release()
        cv2.destroyAllWindows()               
            

