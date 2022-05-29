from asyncio import streams
from xmlrpc.client import Boolean
from kivymd.app import MDApp  
from kivy.app import App  
from kivy.uix.floatlayout import FloatLayout  
from kivy.lang import Builder  
from kivy.core.window import Window   
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from numpy import source  
from kivy.properties import ListProperty,BooleanProperty,NumericProperty,ObjectProperty,StringProperty
from kivy.clock import Clock
import os 
import face_recognition
import numpy as np
import cv2
  
Window.size = (350, 580)  
# //pillow ffpyplayer for video   pip install ffpyplayer  
  
class Layout_(FloatLayout):  
    # Traing Data Image Path
    path = StringProperty('src/img/')
    known_face_encodings = ListProperty()
    known_face_names = ListProperty()
    stream_status = BooleanProperty(False)
    capture = ObjectProperty()
    face_locations = ListProperty()
    face_encodings = ListProperty()
    face_names = ListProperty()
    process_this_frame = BooleanProperty(True)
    key = cv2. waitKey(1) 


    def get_trained_data(self,path=None):
        try:
            # check isdir 
            if not os.path.isdir(path):
                # raise Exception("Path is not a directory")
                return None, None

            images = os.listdir(path) 
            for _ in images: 
                if _.startswith('.'):
                    continue
                image = face_recognition.load_image_file(path + _) 
                image_path = path + _ 
                encoding = face_recognition.face_encodings(image)[0] 
                self.known_face_encodings.append(encoding) 
                self.known_face_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize()) 

            return self.known_face_names, self.known_face_encodings
        except Exception as e:
            print(e)
            return None, None
 

    def start_stream(self,instance):
        
        if not self.stream_status:
            try:

                self.known_face_names, self.known_face_encodings = self.get_trained_data(self.path)
                print(self.known_face_names)
                print(self.known_face_encodings)
                self.stream_status = True
                # farme_widget
                self.img1=Image()
                instance.add_widget(self.img1)
                # Get a reference to webcam #0 (the default one)
                self.capture = cv2.VideoCapture(0)
                Clock.schedule_interval(self.update, 1.0/33.0)

            except Exception as e:
                print(e)

        else:
            print("Stream is already running")



    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing 
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) 
        rgb_small_frame = small_frame[:, :, ::-1] 
        # Only process every other frame of video to save time 
        if self.process_this_frame: 
            # Find all the faces and face encodings in the current frame of video 
            self.face_locations = face_recognition.face_locations(rgb_small_frame) 
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations) 
            self.face_names = []
            for face_encoding in self.face_encodings: 
                # See if the face is a match for the known face(s) 
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding) 
                name = "Unknown" 
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding) 
                best_match_index = np.argmin(face_distances) 
                if matches[best_match_index]: 
                    name = self.known_face_names[best_match_index] 
                self.face_names.append(name) 
    
        self.process_this_frame = not self.process_this_frame 
        # Display the results 
        for (top, right, bottom, left), name in zip(self.face_locations,  self.face_names): 
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
    

        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1


class MainApps(MDApp):  
      
    def build(self):  
        # pip install Padding  
  
        Builder.load_file("demo.kv")  
        return Layout_()  
          
    def video(self,*args):  
        player=VideoPlayer(source="Home Alone 3.mp4")  
        player.state='play'  
        player.options={'eos':'loop'}  
        player.allow_stretch=True  
        return player  
  
MainApps().run()