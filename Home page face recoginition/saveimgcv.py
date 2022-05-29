#  pip install cmake 
# conda install -c conda-forge dlib 
# pip install face_recognition 
# pip install opencv-python 
 
import face_recognition 
import cv2 
import numpy as np 
import os 
import smtplib
import imghdr
import os
from PIL import Image
from email.message import EmailMessage
import notifypy

path = "D:/Micro/train/" 
 
known_face_names = [] 
known_face_encodings = [] 
 
images = os.listdir(path) 
for _ in images: 
    image = face_recognition.load_image_file(path + _) 
    image_path = path + _ 
    encoding = face_recognition.face_encodings(image)[0] 
    known_face_encodings.append(encoding) 
    known_face_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize()) 
 
# Get a reference to webcam #0 (the default one) 
video_capture = cv2.VideoCapture(0) 
 
 
face_locations = [] 
face_encodings = [] 
face_names = [] 
process_this_frame = True 
key = cv2. waitKey(1) 
global criminal_name
global flag
flag=0
global names

while True: 
    # Grab a single frame of video 
    ret, frame = video_capture.read() 
 
    # Resize frame of video to 1/4 size for faster face recognition processing 
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) 
 
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses) 
    rgb_small_frame = small_frame[:, :, ::-1] 
 
    # Only process every other frame of video to save time 
    if process_this_frame: 
        # Find all the faces and face encodings in the current frame of video 
        face_locations = face_recognition.face_locations(rgb_small_frame) 
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) 
 
        face_names = [] 
        for face_encoding in face_encodings: 
            # See if the face is a match for the known face(s) 
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding) 
            global name
            name = "Unknown" 
 
            # Or instead, use the known face with the smallest distance to the new face 
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding) 
            best_match_index = np.argmin(face_distances) 
            if matches[best_match_index]: 
                name = known_face_names[best_match_index] 
 
            face_names.append(name) 
    process_this_frame = not process_this_frame 
 
 
    # Display the results 
    for (top, right, bottom, left), name in zip(face_locations, face_names): 
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size 
        top *= 4 
        right *= 4 
        bottom *= 4 
        left *= 4 
 
        # Draw a box around the face 
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) 
 
        # Draw a label with a name below the face 
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED) 
        font = cv2.FONT_HERSHEY_DUPLEX 
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1) 
 
    # Display the resulting image 
    cv2.imshow('Video', frame) 
    key = cv2. waitKey(1) 
    
    criminal_name="sanu"
    if flag==0:
        filenames="D:/Micro/test/save.jpg"
        
        
    else:
        filenames="D:/Micro/train/"+criminal_name+".jpg"
    if key == ord('s'):  
        
            cv2.imwrite(filename=filenames, img=frame) 
            img_new = cv2.imread(filenames, cv2.IMREAD_GRAYSCALE) 
            cv2.waitKey(1) 
#             Processing image... 
            img_ = cv2.imread(filenames, cv2.IMREAD_ANYCOLOR) 
            print("Converting RGB image to grayscale...") 
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY) 
            print("Converted RGB image to grayscale...") 
            print("Resizing image to 28x28 scale...") 
            img_ = cv2.resize(gray,(128,128)) 
            print("Resized...") 
            img_resized =cv2.imwrite(filename='D:/Micro/test/saved_img-final.jpg', img=img_) 
            print("Image saved!") 
            Sender_Email ="saniya61shaikh@gmail.com"
            Reciever_Email ="saniya61shaikh@gmail.com"
            Password = "saniya786"

            newMessage = EmailMessage()                         
            newMessage['Subject'] = "Alert criminal is detected" 
            newMessage['From'] = Sender_Email                   
            newMessage['To'] = Reciever_Email                   
            newMessage.set_content('See the files. Image attached!') 
            path="D:/Micro/test/"
            for file in os.listdir(path):
                p=path+file
                if file=="save.jpg":
                    with open(p, 'rb') as f:
                        file_data = f.read()
                        file_name = f.name
                    try:
                        im=Image.open(file)
                        image_type = imghdr.what(f.name)
                        maintypes='image'
                        subtypes=image_type

                    except IOError:
                        maintypes='application'
                        subtypes='octet-stream'
                
                    newMessage.add_attachment(file_data, maintype=maintypes, subtype=subtypes, filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    
                    smtp.login(Sender_Email, Password)              
                    smtp.send_message(newMessage)
            notific=notifypy.Notify()
            notific.title="Alert"
            notific.application_name="Sensing"
            notific.message="The Criminal is found .... for more detail se the maile"
            notific.icon="D:/micfi/Temp-256x256.jpg"
            notific.send()
            flag=0
             
    elif key == ord('q'): 
            print("Turning off camera.") 
            video_capture.release() 
            print("Camera off.") 
            print("Program ended.") 
            cv2.destroyAllWindows() 
            break 
         
 
