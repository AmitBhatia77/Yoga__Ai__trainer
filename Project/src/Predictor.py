import cv2
import mediapipe as mp
import os
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
import threading
from keras.models import load_model
import tkinter.messagebox as mb

global frame_copy

class Predictor(): 
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    pose = mpPose.Pose()
    ls_landmark = [] 
    N_TIME = 10
    color=(0, 0, 255)
    tim=0
    model = load_model('../models/best.h5')
    label ="None"
    temp=""
    def __init__(self,frame,panel,sign):
        
        self.frame=frame
        self.frame_copy=None
        self.panel=panel
        self.sign=sign
        self.result = "B"
        

        if(frame=="None" and panel=="None" and sign=="None"):
            self.__class__.ls_landmark = []
            #self.__class__.N_TIME = 0
            self.frame_copy = None
            self.result = None
            print("Destroyed")
        else:
            files = os.listdir('../data')
            self.classes = []
            for path in files:
                self.classes.append(path.split('.')[0])
            list.sort(self.classes)
            self.predicting()

    def make_landmark_timestamp(self,poseRet):
        ret = []
        for idx, lm in enumerate(poseRet.pose_landmarks.landmark):
            ret.append(lm.x)
            ret.append(lm.y)
            ret.append(lm.z)
            ret.append(lm.visibility)
        #print("ret",ret)
        return ret

    def draw_landmark(self,mpDraw, poseRet, frame,colors):
        self.mpDraw.draw_landmarks(frame, poseRet.pose_landmarks, self.mpPose.POSE_CONNECTIONS,self.mpDraw.DrawingSpec(color=colors, thickness=2, circle_radius=2))
        return frame

    def draw_label(self,tim, frame):
        #text = "Class: {}".format(lbl)
        text="Time: "+str(tim)+"s"
        pos = (10,30)
        scale = 1
        thickness = 2
        lineType = 2
        fontColor = (0, 0, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,
                    text,
                    pos,
                    font,
                    scale,
                    self.color,
                    thickness,
                    lineType)
        return frame

    def detect(self,model, ls_landmark):
        tensor = np.expand_dims(self.ls_landmark,axis=0)
        result = model.predict(tensor)
        self.label = self.classes[np.argmax(result[0])]
        self.__class__.temp=self.label
        print("model",self.label)
        #print(np.round(np.array(result[0]),2))

    def predicting(self):
        self.frame_copy = cv2.flip(self.frame, 1)
        rgb = cv2.cvtColor(self.frame_copy, cv2.COLOR_BGR2RGB)
        poseRet = self.pose.process(rgb)
        if (poseRet.pose_landmarks):
            landmark = self.make_landmark_timestamp(poseRet)
            self.ls_landmark.append(landmark)
            print("landdd",self.sign)
            self.frame_copy = self.draw_landmark(self.mpDraw, poseRet, self.frame_copy,self.color)
        print(len(self.ls_landmark),self.N_TIME)
        if (len(self.ls_landmark)==self.N_TIME):
            self.detect(self.model, self.ls_landmark)
##            t = threading.Thread(
##                target = self.detect,
##                args = (self.model, self.ls_landmark)
##            )
##            t.start()
            self.__class__.ls_landmark = []
            self.frame_copy = self.draw_label(self.tim, self.frame_copy)
            if self.label==self.sign:
                self.__class__.color=(0, 255, 0)
                self.__class__.tim=self.__class__.tim+1
                if self.__class__.tim==10:
                     mb.showinfo("Yoga Pose Detector", "Good Job Buddy! Now Try Another Pose")
                    
            else:
                self.__class__.color=(0, 0, 255)
                self.__class__.tim=0
        else:
            self.frame_copy = self.draw_label(self.tim, self.frame_copy)

        #print(self.label)
        
        self.result = "some"
        return self.frame_copy    

    #def __del__(self):
   #     print("released")
