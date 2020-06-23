# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 07:04:04 2020

@author: video

"""

# import the required packages
import cv2
import argparse
import  matplotlib.pyplot as plt
from sklearn.externals import joblib 
import face_recognition
#import dlib
import cv2
#import os
#from sklearn import svm 
# Save the model as a pickle in a file 
# joblib.dump(classifier, 'classifier.pkl')

# Load the model from the file 
classifier_from_joblib = joblib.load('classifier.pkl') 

# first we create Argumentparser object
# The created object 'parser' will have the necessary information
# to parse the command-line arguments into data types.
parser = argparse.ArgumentParser()


# we add video path argument using add_argument() methed:
parser.add_argument("video_path", help = "path to the video file")
# We add 'output_video_path' argument using add_argument() including a help.
#parser.add_argument("output_video_path", help = "path to video file to write")
args = parser.parse_args()


def Face_Recognition(frame):
    
    # Find all the faces in the test image using the default HOG-based model 
    face_locations = face_recognition.face_locations(frame)
    
    number = len(face_locations)
    
    #print("Number of faces detected: ", number) 
    
    # Predict all the faces in the test image using the trained classifier 
    #print("Found:")
    names = []
    probabilities = []
    
    for i in range(number):
        test_image_enc = face_recognition.face_encodings(frame)[i]
        name = classifier_from_joblib.predict([test_image_enc])
        probability = classifier_from_joblib.predict_proba([test_image_enc])
        #img = cv2.imread(test,1)
        if (probability.max()) > 0.60 :    
            names.append(name)
        else :
            names.append("unknown")
        
        #cv2.imshow('image', img )
        #plt.imshow(img[:,:,::-1])
     #   print(names)
      #  print(probability.max())
    
    for ( (top,right, bottom, left), name ) in zip(face_locations, names):
        if name != "unknown":
            cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2)
            y = top - 15 if top -15 > 15 else top + 15
            cv2.putText(frame, name[0], (left,y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0,255,0), 2)
        # convert video file frame grayscale
        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    return frame
        



# create video capture object
# In this case, the argument is the video file name 
capture = cv2.VideoCapture(args.video_path)

# Get some properties of VideoCapture (frame width, frame height and frames per second (fps)):
frame_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = capture.get(cv2.CAP_PROP_FPS)


# Print these values:
print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(frame_width))
print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(frame_height))
print("CAP_PROP_FPS : '{}'".format(fps))


# FourCC (four charecter code ) is a 4-byte code used to specify the video codec and it is platform dependent !
# In this case, define the codec XVID
# This line also works:
# fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')MJPG
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# Create VideoWriter object. We use the same properties as the input camera.
# Last argument is False to write the video in grayscale. True otherwise (write the video in color)
#out_frame = cv2.VideoWriter(args.output_video_path, fourcc, int(fps), (int(frame_width), int(frame_height)), False)

#icnt = 0
# check if video is opened successfully
while capture.isOpened():
    # capture frame by frame from the video file
    ret, frame = capture.read()
    
    if ret is True :
        # Display the resulting frame
        #cv2.imshow("Original frame from videa file", frame)
        
        
        #test_image = face_recognition.load_image_file(test)
        frame = Face_Recognition(frame)
        
        # Write the grayscale frame to the video
        #out_frame.write(frame)
        #print(f"frame : {icnt} written successfully ")
        #icnt+=1
        # display the gray frame
        cv2.imshow("frame", frame)
    
    # press 'q' on keyboard to exit program
        if cv2.waitKey(20) & 0xFF == ord('q') :
            break 
    # break the loop
    else :
        break

# release everything 
capture.release()
cv2.destroyAllWindows()