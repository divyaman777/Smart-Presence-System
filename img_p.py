import os
from PIL import Image
import numpy as np
import cv2
import pickle
a=set()
recognizer = cv2.face.LBPHFaceRecognizer_create(2,2,7,7,20)

def img(sclass,img_loc):

    recognizer.read("train_folder/"+sclass+"/"+"trainer.yml")##

    fr=open("train_folder\\"+sclass+"\\"+"labels.pickle","rb")
    og_labels=pickle.load(fr)
    labels = {v:k for k,v in og_labels.items()}
    

    face=cv2.CascadeClassifier('cascades\\data\\haarcascade_frontalface_alt2.xml')
    a=set()
    recognise = cv2.face.EigenFaceRecognizer_create()

    img = cv2.imread('uploads/'+img_loc)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray,1.5,5)

    for (x,y,w,h) in faces:
        gray_face = cv2.resize(gray[y:y+h,x:x+w],(250,210))

        id_,conf  =  recognizer.predict(gray_face)
        if conf<=70:
            print(conf)
            print(labels[id_])
            a.add(labels[id_])
        else:
            print("Unknown")
        
        color = (0,0,255)
        stroke = 1
        cv2.rectangle(img, (x,y),(x+w,y+h),color,stroke)
        cv2.imwrite('static/detect/'+img_loc,img)
        cv2.waitKey(10)
    return(a)
