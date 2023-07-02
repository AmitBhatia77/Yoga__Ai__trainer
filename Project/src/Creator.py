import cv2
import mediapipe as mp
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


class Creator():
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    pose = mpPose.Pose()
    ls_landmark = []
    N_FRAME = 100
    def __init__(self,frame,panel,sign):
        self.frame=frame
        self.frame_copy=None
        self.panel=panel
        self.sign=sign
        self.result = "B"
        if(frame=="None" and panel=="None" and sign=="None"):
            #self.__class__.N_FRAME = 0
            self.frame_copy = None
            self.result = None
            print("Destroyed")
        else:
            self.creating()

    def make_landmark_timestamp(self,poseRet):
        self.ret = []
        for idx, lm in enumerate(poseRet.pose_landmarks.landmark):
            self.ret.append(lm.x)
            self.ret.append(lm.y)
            self.ret.append(lm.z)
            self.ret.append(lm.visibility)
        return self.ret

    def draw_landmark(self,frame, mpDraw, pose_landmarks=None, face_landmarks = None):
        if (pose_landmarks is not None):
            self.mpDraw.draw_landmarks(frame, pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        if (face_landmarks is not None):
            self.mpDraw.draw_landmarks(frame, face_landmarks, self.mpPose.FACEMESH_CONTOURS)
        return frame

    def draw_count_frame(self, cnt, total, frame):
        text = "Frame: {}/{}".format(cnt, total)
        pos = (10,30)
        scale = 1
        thickness = 2
        lineType = 2
        fontColor = (0, 0, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            frame,
            text,
            pos,
            font,
            scale,
            fontColor,
            thickness,
            lineType
        )
        return frame

    def creating(self):
        if len(self.ls_landmark) < self.N_FRAME:
            self.frame_copy = cv2.flip(self.frame, 1)
            rgb = cv2.cvtColor(self.frame_copy, cv2.COLOR_BGR2RGB)
            poseRet = self.pose.process(rgb)
            if (poseRet.pose_landmarks):
                landmark = self.make_landmark_timestamp(poseRet)
                self.ls_landmark.append(landmark)
                self.frame_copy = self.draw_landmark(self.frame_copy, self.mpDraw, pose_landmarks=poseRet.pose_landmarks, face_landmarks = None)
                #fig = plt.figure(figsize = [10, 10])
                #plt.title("Output");plt.axis('off');plt.imshow(self.frame_copy[:,:,::-1]);plt.show()
                #self.mpDraw.plot_landmarks(poseRet.pose_world_landmarks, self.mpPose.POSE_CONNECTIONS)
            self.frame_copy = self.draw_count_frame(len(self.ls_landmark), self.N_FRAME,self.frame_copy)
        else:
            cv2.destroyAllWindows()
            self.__class__.ls_landmark = []
            self.result = None
            return None
            # Show pose
            #cv2.imshow('pose', self.frame)
        if self.sign!=None:    
            df = pd.DataFrame(self.ls_landmark)
            df.to_csv("../data/{}.csv".format(self.sign),index=False)
        return self.frame_copy

    def __del__(self):
        print("released")
