# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 06:33:37 2020

@author: vijaynchakole

"""

from imutils.video import VideoStream
import  matplotlib.pyplot as plt
import face_recognition
import cv2
import pickle
from sklearn.externals import joblib 
# Save the model as a pickle in a file 
#joblib.dump(classifier, 'classifier.pkl')

# Load the model from the file 
classifier_from_joblib = joblib.load('classifier.pkl') 

# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
# 0 = inbuild camera

path = "C:\\Users\\hp\\Desktop\\Face_Recognition\\videos\\He Speaks Very Good English But_ PM Modi Laughs At Trump Remark.mp4"
vs = VideoStream(path).start()
writer = None
import time
time.sleep(2.0)


# loop over frames from the video file stream
while True :
    frame = vs.read()
    test_image = face_recognition.load_image_file(frame)
    
    # Find all the faces in the test image using the default HOG-based model 
    face_locations = face_recognition.face_locations(frame)
    
    number = len(face_locations)
    
    print("Number of faces detected: ", number) 
    
    # Predict all the faces in the test image using the trained classifier 
    print("Found:")

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
        
        
     
    # plt.imshow(img[:,:,::-1])


    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter("output.avi", fourcc, 20,
    			(frame.shape[1], frame.shape[0]), True)
    
    # if the writer is not None, write the frame with recognized
	# faces to disk
	
	#writer.write(frame)
        
    cv2.imshow("Frame", frame)
    if cv2.waitKey(20) & 0xFF == ord('q') :
            break 
    
    
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
# check to see if the video writer point needs to be released
writer.release()