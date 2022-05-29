# from tkinter import Padding
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.videoplayer import VideoPlayer
from matplotlib.pyplot import flag
from numpy import source
from kivy.uix.screenmanager import ScreenManager, Screen


Window.size = (350, 580)

# //pillow ffpyplayer for video   pip install ffpyplayer

class Layout_(FloatLayout):
    pass
sm = ScreenManager()
sm.add_widget(Layout_(name = 'reg'))

class MainApps(MDApp): 
    def build(self):
        # pip install Padding

        Builder.load_file("ki.kv")
        return Layout_()

    def condi(self,*args):
        # key = ord('s')
        sm.current="reg"
        criminal_name = self.strng.get_screen('reg').ids.criminal_name.text
        sm.get_screen('home').manager.current = 'home'
        
    


MainApps().run()


# layout =GridLayout(cols=2,spacing=10,padding=10)#height ="210dp",evaluation=5,border_radius=20,radius=[15])
        # btn1=Button(text='Hello 1',background_normal=video())
        # btn2=Button(text='Hello 2')
        # btn3=Button(text='Hello 3')
        # btn4=Button(text='Hello 4')
        # layout.add_widget(btn1)
        # layout.add_widget(btn2)
        # layout.add_widget(btn3)
        # layout.add_widget(btn4)
        # layout


# def video(self,*args):
    #     player=VideoPlayer(source="Home Alone 3.mp4")
    #     player.state='play'
    #     player.options={'eos':'loop'}
    #     player.allow_stretch=True
    #     return player