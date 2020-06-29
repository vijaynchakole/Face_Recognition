# Face_Recognition

#### Project Files : Face_Recognition_From_Image.py, Face_Recognition_from_Video.py

###### file for images download from google : images_download.py 

#### Dependencies : face_recognition, cv2, sklearn, matplotlib, selenium (for images download from google), svm(sklearn), pickle
short overview:

I have done this project from scratch 

I have selected 5 famous people for the Face Recognition Model.

##### Names of those people : Modi, Trump, Putin, Xi Jin Ping, Kim Jong Un 

and downloaded their images from google using selenium for creating training and testing dataset.

I have created a Face Recognition Model. which recognizes the faces of above mentioned people.

code explanation in short :
with the help of selenium library I have downloaded all images for my project

1
with the help of face_recognition library I have created face encodings once I get face encodings then 
I have used them for Model build.

2
I have built an SVC (Support Vector Classifier) model by using face encodings

3
Once model is built then it is used for face recognition in given image
