import os
from PIL import Image
import numpy as np
import cv2
import pickle
def train(sclass):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "train_folder/"+sclass)

    face_cascade = cv2.CascadeClassifier(r'cascades/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    current_id = 0
    label_ids ={}
    y_labels = []
    x_train = []

    for root,dirs,files in os.walk(image_dir):
        for file in files:
            if file.endswith("PNG") or file.endswith("jpg") or file.endswith("png") or file.endswith("jpeg") or file.endswith("JPEG") or file.endswith("JPG"):
                path = os.path.join(root, file)
                label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()  
                #print(label,path)
                if label not in label_ids:
                    label_ids[label] = current_id
                    current_id+=1
                id_=label_ids[label]
                print(id_)####
                print(label_ids)###
                pil_image = Image.open(path).convert("L") #grayscale

                image_array = np.array(pil_image, "uint8")
    
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.3, minNeighbors=5,minSize=(10, 10))
                for(x,y,w,h) in faces:
                    roi = cv2.resize(image_array[y:y+h,x:x+w],(110,110)) #cv2.resize(gray[y:y+h,x:x+w],(110,110))
                    roi_np = np.array(roi, 'uint8')
                    x_train.append(roi_np)
                    y_labels.append(id_)
    #print(y_labels)

    fw=open("train_folder/"+sclass+"/"+"labels.pickle","wb")
    pickle.dump(label_ids,fw)
    fw.close()

    recognizer.train(x_train,np.array(y_labels))
    recognizer.save("train_folder/"+sclass+"/"+"trainer.yml")
    return "Done"
