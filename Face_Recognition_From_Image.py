# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:00:16 2020

@author: vijaynchakole

"""

# import neccessary libraries
import face_recognition
import cv2
import os
from sklearn import svm 
import pickle
from sklearn.externals import joblib 
import  matplotlib.pyplot as plt

current_dir = os.getcwd()
encodings = []
names = []

def face_recognize(train_dir):
    global encodings
    global names
    #train_dir = "training"
    # loop through each person
    for label_folder in os.listdir(train_dir) :
        images = os.listdir(train_dir+'/'+label_folder)
        print(label_folder)
        
        for person_img in images:
            print(person_img)
            face = face_recognition.load_image_file(train_dir+'/'+label_folder+'/'+person_img)
            
            face_bounding_boxes = face_recognition.face_locations(face)
            
            # If training image contains exactly one face 
            if len(face_bounding_boxes) == 1 :
                face_enc = face_recognition.face_encodings(face)[0]
                # add face encoding for current image
                # with corresponding label (name)
                print("labeling")
                names.append(label_folder)
                print("encoding")
                encodings.append(face_enc)
                print("*****************************")
                
            else:
                print("person image can't be used for training purpose ")
            
   
        
def Model_build(encodings, names) :
    # create and train SVC classifier
    classifier = svm.SVC(gamma = 'scale', probability=True)
    classifier.fit(encodings, names)
    return classifier


def Model_save(classifier):
    #save_classifier = pickle.dumps(classifier)
    # Pickled model as a file using joblib
    # Save the model as a pickle in a file 
    joblib.dump(classifier, 'classifier.pkl')
    


def predict_faces(test):
    
    test_image = face_recognition.load_image_file(test)
    
    # Find all the faces in the test image using the default HOG-based model 
    face_locations = face_recognition.face_locations(test_image)
    
    number = len(face_locations)
    
    print("Number of faces detected: ", number) 
    
    # Predict all the faces in the test image using the trained classifier 
    names = []
    probabilities = []
    
    
    for i in range(number):
        test_image_enc = face_recognition.face_encodings(test_image)[i]
        name = classifier_from_joblib.predict([test_image_enc])
        probability = classifier_from_joblib.predict_proba([test_image_enc])
        img = cv2.imread(test,1)
        if (probability.max()) > 0.50 :    
            names.append(name)
        else :
            names.append("unknown")
        
        #cv2.imshow('image', img )
        #plt.imshow(img[:,:,::-1])
        print(names)
        print(probability.max())
    
    for ( (top,right, bottom, left), name ) in zip(face_locations, names):
        if name != "unknown":
            cv2.rectangle(img, (left,top), (right,bottom), (0,255,0), 2)
            y = top - 15 if top -15 > 15 else top + 15
            cv2.putText(img, name[0], (left,y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0,255,0), 2)
        
    plt.imshow(img[:,:,::-1])
    #names[1][0]

face_recognize("training")
classifier = Model_build(encodings, names)
Model_save(classifier)
# Load the model from the file 
classifier_from_joblib = joblib.load('classifier.pkl') 
test = "C:\\Users\\hp\\Desktop\\Face_Recognition\\3.jpeg"
predict_faces(test)

