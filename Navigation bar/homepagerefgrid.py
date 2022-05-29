# from tkinter import Padding
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.videoplayer import VideoPlayer
from numpy import source


Window.size = (350, 580)

# //pillow ffpyplayer for video   pip install ffpyplayer

class Layout_(FloatLayout):
    pass


class MainApps(MDApp):
    
    def build(self):
        # pip install Padding

        Builder.load_file("ui.kv")
        return Layout_()
        
    

MainApps().run()