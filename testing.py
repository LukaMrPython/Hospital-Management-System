
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import sys
from kivy.factory import Factory
from kivy.clock import Clock
#Load kv file
Builder.load_file('test.kv')

class ScreenAdmin(Screen):
    pass

class ScreenDoctor(Screen):
    pass

class ImageButton(ButtonBehavior, Image):  
    def on_press(self):  
        print ('pressed')

class Screen2(BoxLayout):
   pass

class ScreenLogin(Screen):
 
   def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
class Manage_Profile(ScrollView):
    pass

#Initialize Screens and Start App
class MyScreenManager(ScreenManager):

    screen_login = ObjectProperty()
    screen_doctor = ObjectProperty()
    screen_accountant = ObjectProperty()
#Main application
class SampleApp(App):

    def build(self):
        self.sm = MyScreenManager()
        self.dashboard = Screen2()
        return self.sm

if __name__ == '__main__':
    SampleApp().run()
