
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem, ThreeLineListItem
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
import os
from PIL import Image
class DemoApp(MDApp):

    def build(self):
        
        screen = Screen()

        # Creating a Simple List
        scroll = ScrollView()

        list_view = MDList()

        path = "D:/Micro/train"
        for file in os.listdir(path):
            f_name, f_ext = os.path.splitext(file)
            icons = IconLeftWidget(icon="alert-circle-check")
            items = OneLineIconListItem(text=f_name)
            items.add_widget(icons)
            list_view.add_widget(items)

    

        scroll.add_widget(list_view)
        # End List

        screen.add_widget(scroll)
        return screen


DemoApp().run()