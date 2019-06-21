import os
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen,WipeTransition
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
#from kivy.graphics.context_instructions import Color
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
#from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle
#from kivy.uix.image import AsyncImage
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from KivyCalendar import CalendarWidget
from KivyCalendar import DatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import sqlite3 as lite
from kivy.uix.image import Image
from kivy.factory import Factory
import sys
import re
import random
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior



con = lite.connect('test.db')
c = con.cursor()

        
class CustomDropDown(DropDown):
    pass


################################## patient List / Edit column ############################################

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''
    selected_row = NumericProperty(0)

    def get_nodes(self):
        nodes = self.get_selectable_nodes()
        if self.nodes_order_reversed:
            nodes = nodes[::-1]
        if not nodes:
            return None, None

        selected = self.selected_nodes
        if not selected:    # nothing selected, select the first
            self.select_node(nodes[0])
            self.selected_row = 0
            return None, None

        if len(nodes) == 1:     # the only selectable node is selected already
            return None, None

        last = nodes.index(selected[-1])
        self.clear_selection()
        return last, nodes

    def select_next(self):
        ''' Select next row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if last == len(nodes) - 1:
            self.select_node(nodes[0])
            self.selected_row = nodes[0]
        else:
            self.select_node(nodes[last + 1])
            self.selected_row = nodes[last + 1]

    def select_previous(self):
        ''' Select previous row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if not last:
            self.select_node(nodes[-1])
            self.selected_row = nodes[-1]
        else:
            self.select_node(nodes[last - 1])
            self.selected_row = nodes[last - 1]

    def select_current(self):
        ''' Select current row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        self.select_node(nodes[self.selected_row])


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        

    def on_press(self,*args):
        select_patient = Manage_Prescription()
        select_patient.man_selected_patient()
        
class EditStatePopup(Popup):
    patient_id: ObjectProperty(None)
    patient_name:ObjectProperty(None)
    patient_email:ObjectProperty(None)
    patient_address:ObjectProperty(None)
    patient_fon:ObjectProperty(None)
    patient_sex:ObjectProperty(None)
    patient_dob:ObjectProperty(None)
    patient_age:ObjectProperty(None)
    patient_blood:ObjectProperty(None)
    

    def __init__(self, obj, **kwargs):
        super(EditStatePopup, self).__init__(**kwargs)
        self.obj = obj
        self.editpatient()

    def editpatient(self):
        
        c.execute("SELECT ID ,NAME , EMAIL, ADDRESS, PHONE, SEX , DOB, AGE, BLOOD FROM Patients  WHERE ID=?", (self.obj,))
        self.row_data = c.fetchone()

        self.patient_id.text=str(self.row_data[0])
        self.patient_name.text = self.row_data[1]
        self.patient_email.text = self.row_data[2]
        self.patient_address.text= self.row_data[3]
        self.patient_fon.text= str(self.row_data[4])
        self.patient_sex.text =  self.row_data[5]
        self.patient_dob.text = str(self.row_data[6])
        self.patient_age.text = str(self.row_data[7])
        self.patient_blood.text= self.row_data[8]
        
    def update(self):

        patient_id = self.patient_id.text
        name = self.patient_name.text
        email = self.patient_email.text
        address = self.patient_address.text
        fon = self.patient_fon.text
        sex = self.patient_sex.text
        dob = self.patient_dob.text
        age = self.patient_age.text
        blood = self.patient_blood.text
        
        c.execute(" UPDATE Patients SET ID =?, NAME=? , EMAIL=?, ADDRESS = ?, PHONE = ?, SEX = ? , DOB = ?, AGE = ?, BLOOD = ? WHERE ID =?",
                   (patient_id, name, email, address,fon, sex ,dob,age, blood, patient_id,))
        con.commit()
        callback = Patient_list()
        try:
            callback.refresh()
        except:
            print("popup_refresh error")

class Add_patient(GridLayout):
    patient_id: ObjectProperty(None)
    patient_name:ObjectProperty(None)
    patient_email:ObjectProperty(None)
    patient_address:ObjectProperty(None)
    patient_fon:ObjectProperty(None)
    patient_sex:ObjectProperty(None)
    patient_dob:ObjectProperty(None)
    patient_age:ObjectProperty(None)
    patient_blood:ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Add_patient, self).__init__(**kwargs)
        self.create_table_patients()
        self.buildLists()
        
    def buildLists(self):
        c. execute("SELECT Class FROM classes")
        result = c.fetchall()
         
         
        self.pickType = [str(t[0]) for t in result]
        
    def regenerate(self):
        self.gen_patient_id()
    
    def gen_patient_id(self):
        gen = random.randint(500, 50000)
        c.execute("SELECT * FROM Patients WHERE ID = ?",(gen,))
        results = c.fetchall()
        
        if results:
            return self.regenerate()
        else:
            self.patient_id.text = str(gen)
            
                 
         
    def create_table_patients(self):
        try:
            c.execute("CREATE TABLE IF NOT EXISTS Patients (ID INT,NAME TEXT , EMAIL TEXT,ADDRESS TEXT,PHONE INT,SEX TEXT, DOB TEXT, AGE TEXT,BLOOD TEXT)")
            con.commit()
        except:
            print("Error")
            
    

    def insert_patients(self, **kwargs):
        patient_id = self.patient_id.text
        name = self.patient_name.text
        email = self.patient_email.text
        address = self.patient_address.text
        fon = self.patient_fon.text
        sex = self.patient_sex.text
        dob = self.patient_dob.text
        age = self.patient_age.text
        blood = self.patient_blood.text
        
        try:
            c.execute("INSERT INTO Patients(ID ,NAME , EMAIL,ADDRESS,PHONE,SEX , DOB, AGE,BLOOD) VALUES (?,?,?,?,?,?,?,?,?) " ,(patient_id,name,email,address,fon,sex,dob,age,blood) )
            con.commit()
            self.save_succefull()
            
        except lite.Error:
            return self.save_popup()
    def save_popup(self):
        self.content = Label(text=' Data not saved!!!')
        self.popup = Popup(title='Error!!!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()
        
    def save_succefull(self):
        self.content = Label(text=' Registration Successfull!!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def  validateif(self):
        if self.patient_name.text and self.patient_email.text and self.patient_address.text and self.patient_fon.text and self.patient_sex.text and self.patient_dob.text and self.patient_age.text and self.patient_blood.text:
            return self.insert_patients()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()
        

class Patient_list(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Patient_list, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_Patients()
    
    def adding_patient(self):
        layout = Factory.Add_patient()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def patient_list(self):
        layout = Factory.Return_patientList()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def man_selected_patient(self):
        
        layout = Factory.Selected_patient()
        
        self.ids['manage_selected'].clear_widgets()
        self.ids['manage_selected'].add_widget(layout)
        print("pressed")

    def get_table_column_headings(self):
        
        try:
            
            c.execute("PRAGMA table_info(Patients)")
            col_headings = c.fetchall()
            self.total_col_headings = 6
        except lite.Error:
            print('not connected')

    def get_Patients(self):
        
        
        c.execute("SELECT ID ,NAME , AGE ,SEX , BLOOD ,DOB FROM Patients ")
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

    def realtime_select(self):
        search = self.real_change.text
        
        if search:
            return self.realtime_search()
        else:
            pass
    
    def realtime_search(self):
        search = self.real_change.text
        
        search +='%'
        c.execute("SELECT ID ,NAME , AGE ,SEX , BLOOD ,DOB FROM Patients WHERE NAME LIKE ?  ", (search,))
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

       

    def popup_callback(self, instance):
        
        self.row_data  = self.data_items[instance.index]['Index']
        
        ''' Instantiate and Open Popup '''
        popup = EditStatePopup(self.row_data)
        popup.open()

    def refresh(self):
        
        call = App.get_running_app().root.screen_doctor.patient()
        return call()
        print('yes refreshed')
        
################################ Appointment List/ EDit Appointment##########

        
class SelectableButton1(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableButton1, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton1, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton1, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        

    def on_press(self,*args):
        select_patient = Manage_Prescription()
        select_patient.man_selected_patient()
        
class EditAppointmentPopup(Popup):
    appointment_id:ObjectProperty(None)
    appointment_doctor:ObjectProperty(None)
    appointment_patient:ObjectProperty(None)
    appointment_date:ObjectProperty(None)
    

    def __init__(self, obj, **kwargs):
        super(EditAppointmentPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editappointment()

    def editappointment(self):
        
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments  WHERE ID=?", (self.obj,))
        self.row_data = c.fetchone()

        self.appointment_id.text=str(self.row_data[0])
        self.appointment_patient.text = self.row_data[1]
        self.appointment_doctor.text = self.row_data[2]
        self.appointment_date.text= self.row_data[3]
      
        
    def update(self):

        patient_id = self.appointment_id.text
        name = self.appointment_patient.text
        doctor = self.appointment_doctor.text
        date = self.appointment_date.text
        
        c.execute(" UPDATE Appointments SET ID =?, NAME=? , DOCTOR =?, DATE=? WHERE ID =?",
                   (patient_id, name, doctor,date,patient_id,))
        con.commit()
        callback = Appointment()
        try:
            callback.refresh()
        except:
            print("popup_refresh error")



class Appointment(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Appointment, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_appointments()
        
    def adding_appointement(self):
        layout = Factory.Add_appointment()
        self.manage_appointment.clear_widgets()
        self.manage_appointment.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Return_appointmentList()
        self.manage_appointment.clear_widgets()
        self.manage_appointment.add_widget(layout)

    def man_selected_patient(self):
        
        layout = Factory.Selected_patient()
        
        self.ids['manage_selected'].clear_widgets()
        self.ids['manage_selected'].add_widget(layout)
        print("pressed")
    def get_table_column_headings(self):
        
        try:
            
            c.execute("PRAGMA table_info(Patients)")
            col_headings = c.fetchall()
            self.total_col_headings = 4
        except lite.Error:
            print('not connected')

    def get_appointments(self):
        
        
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments ")
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

    def realtime_select(self):
        search = self.real_change.text
        
        if search:
            return self.realtime_search()
        else:
            pass
    
    def realtime_search(self):
        search = self.real_change.text
        
        search +='%'
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments WHERE NAME LIKE ?  ", (search,))
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

       

    def popup_callback(self, instance):
        
        self.row_data  = self.data_items[instance.index]['Index']
        
        ''' Instantiate and Open Popup '''
        popup = EditAppointmentPopup(self.row_data)
        popup.open()
        print('ok got it')

    def refresh(self):
        
        call = App.get_running_app().root.screen_doctor.appointment_list()
        return call()
        print('yes refreshed')


class Add_appointment(GridLayout):
    appointment_id:ObjectProperty(None)
    appointment_doctor:ObjectProperty(None)
    appointment_patient:ObjectProperty(None)
    appointment_date:ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Add_appointment, self).__init__(**kwargs)
        self.create_table_appointments()
        self.buildLists()
        
    def buildLists(self):
        c. execute("SELECT Name FROM Doctor ")
        result = c.fetchall()
        self.pickType = [str(t[0]) for t in result]
        if result:
            return self.pickType
        else:
            pass
    
   
                 
         
    def create_table_appointments(self):
        try:
            c.execute("CREATE TABLE IF NOT EXISTS Appointments (ID INT ,NAME TEXT , DOCTOR TEXT, DATE TEXT)")
            con.commit()
        except:
            print("Error")
            
    

    def insert_appointment(self, **kwargs):
        patient_id = self.appointment_id.text
        name = self.appointment_patient.text
        doctor = self.appointment_doctor.text
        date = self.appointment_date.text
        
        try:
            c.execute("INSERT INTO Appointments(ID ,NAME , DOCTOR, DATE) VALUES (?,?,?,?) " ,(patient_id,name,doctor,date) )
            con.commit()
            self.save_succefull()
            
        except lite.Error:
            return self.save_popup()
    def save_popup(self):
        self.content = Label(text=' Data not saved!!!')
        self.popup = Popup(title='Error!!!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()
        
    def save_succefull(self):
        self.content = Label(text=' Registration Successfull!!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def  validateif(self):
        if self.appointment_id.text and self.appointment_patient.text and self.appointment_doctor.text and self.appointment_date.text:
            return self.insert_appointment()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()
        
    def realtime_appointment_id(self):
        search = self.appointment_id.text
        
        #search +='%'
        c.execute("SELECT NAME  FROM Patients WHERE ID = ?  ", (search,))
        rows = c.fetchone()
        if rows:
            self.appointment_patient.text = str(rows[0])
        else:
            print('error')
            
        print(rows)





############################### Prescription management##################################################
class SelectableButton2(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton2, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        

    def on_press(self,*args):
        select_patient = Manage_Prescription()
        select_patient.man_selected_patient()
        
class EditPrescriptionPopup(Popup):
    
    appointment_id:ObjectProperty(None)
    appointment_doctor:ObjectProperty(None)
    appointment_patient:ObjectProperty(None)
    appointment_date:ObjectProperty(None)
    

    def __init__(self, obj, **kwargs):
        super(EditPrescriptionPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editappointment()

    def editappointment(self):
        
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments  WHERE ID=?", (self.obj,))
        self.row_data = c.fetchone()

        self.appointment_id.text=str(self.row_data[0])
        self.appointment_patient.text = self.row_data[1]
        self.appointment_doctor.text = self.row_data[2]
        self.appointment_date.text= self.row_data[3]
      
        
    def update(self):

        patient_id = self.appointment_id.text
        name = self.appointment_patient.text
        doctor = self.appointment_doctor.text
        date = self.appointment_date.text
        
        c.execute(" UPDATE Appointments SET ID =?, NAME=? , DOCTOR =?, DATE=? WHERE ID =?",
                   (patient_id, name, doctor,date,patient_id,))
        con.commit()
        callback = Appointment()
        try:
            callback.refresh()
        except:
            print("popup_refresh error")


   
class Doctor_dashboard(GridLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Doctor_dashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

class Manage_Prescription(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)

    
    #manage_selected:ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Manage_Prescription, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_appointments()
        #Clock.schedule_once(lambda *args: self.man_selected_patient())
    
    def adding_prescription(self):
        layout = Factory.Add_prescription()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)
        
    def priscription_list(self):
        layout = Factory.Return_priscriptionList()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)
        
    
    def man_selected_patient(self):
        
        layout = Factory.Selected_patient()
        
        self.ids['manage_selected'].clear_widgets()
        self.ids['manage_selected'].add_widget(layout)
        print("pressed")


    def get_table_column_headings(self):
        
        try:
            
            c.execute("PRAGMA table_info(Patients)")
            col_headings = c.fetchall()
            self.total_col_headings = 4
        except lite.Error:
            print('not connected')

    def get_appointments(self):
        
        
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments ")
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]


        
    def realtime_select(self):
        search = self.real_change.text
        
        if search:
            return self.realtime_search()
        else:
            pass
    
    def realtime_search(self):
        search = self.real_change.text
        
        search +='%'
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments WHERE NAME LIKE ?  ", (search,))
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

       

    def popup_callback(self, instance):
        
        self.row_data  = self.data_items[instance.index]['Index']
        
        ''' Instantiate and Open Popup '''
        popup = EditPrescriptionPopup(self.row_data)
        popup.open()
        print('ok got it')

        
class Add_prescription(GridLayout):
    pass
class Return_priscriptionList(BoxLayout):
    
    pass

##################### Accountant ###############################################  
class ScreenAccountant(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenAccountant, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)
        
    def account_dashboard(self):
        layout = Factory.Accountantdashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    
    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)




class Accountantdashboard(BoxLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Accountantdashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    


###################  Labaratorist ###################################
        
class ScreenLabaratorist(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenLabaratorist, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_donor(self):
        layout = Factory.Manage_Donor()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def lab_dashboard(self):
        layout = Factory.Labdashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

class Labdashboard(BoxLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Labdashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

#################### Nurse ###############################################        
        
class ScreenNurse(Screen):
    state = BooleanProperty(False)
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenNurse, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())
        
    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def patient(self):
        layout = Factory.Patient_list()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
    def dashboard(self):
        layout = Factory.Doctor_dashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Appointment()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def prescription_list(self):
        layout = Factory.Manage_Prescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def allotment_list(self):
        layout = Factory.Bed_allotement()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
    def bed(self):
        layout = Factory.Manage_Bed()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_donor(self):
        layout = Factory.Manage_Donor()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def report_list(self):
        layout = Factory.Manage_Report()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

################## reussable Classes ####################################
        
        
class Manage_Donor(GridLayout):
    def adding_donor(self):
        layout = Factory.Add_donor()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_donorList(self):
        layout = Factory.Return_donorList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_donor(GridLayout):
    pass
class Return_donorList(BoxLayout):
    pass

class Manage_Bed(GridLayout):
    def adding_bed(self):
        layout = Factory.Add_bed()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_bedList(self):
        layout = Factory.Return_bedList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_bed(GridLayout):
    pass

class Return_bedList(BoxLayout):
    pass


########################  Pharmascist ##########################################

 
class ScreenPharmascist(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenPharmascist, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def medcategory(self):
        layout = Factory.Med_Category()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def med(self):
        layout = Factory.Manage_med()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def medprescription(self):
        layout = Factory.Manage_medprescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def dashboard(self):
        layout = Factory.Pharmdashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

class Med_Category(GridLayout):
    def adding_medcategory(self):
        layout = Factory.Add_medcategory()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_medcategoryList(self):
        layout = Factory.Return_medcategoryList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_medcategory(GridLayout):
    pass

class Return_medcategoryList(BoxLayout):
    pass

class Manage_med(GridLayout):
    def adding_med(self):
        layout = Factory.Add_med()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_medList(self):
        layout = Factory.Return_medList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_med(GridLayout):
    pass

class Return_medList(BoxLayout):
    pass

class Pharmdashboard(GridLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Pharmdashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)


class Manage_medprescription(GridLayout):
    def adding_prescription(self):
        layout = Factory.Add_medprescription()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_medprescriptionList(self):
        layout = Factory.Return_medprescriptionList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_medprescription(GridLayout):
    pass

class Return_medprescriptionList(BoxLayout):
    pass


################# Admin ##############################################

class ScreenAdmin(Screen):
    state = BooleanProperty(False)
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenAdmin, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())
        

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def patient(self):
        layout = Factory.Patient_list()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
    def dashboard(self):
        layout = Factory.Doctor_dashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Appointment()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def prescription_list(self):
        layout = Factory.Manage_Prescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def allotment_list(self):
        layout = Factory.Bed_allotement()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def report_list(self):
        layout = Factory.Manage_Report()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def department_list(self):
        layout = Factory.Manage_department()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def doctor_list(self):
        layout = Factory.Manage_doctor()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def nurse_list(self):
        layout = Factory.Manage_nurse()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)  


    def pharm_list(self):
        layout = Factory.Manage_pharm()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)  

    def lab_list(self):
        layout = Factory.Manage_Lab()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def accountant_list(self):
        layout = Factory.Manage_Accountant()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        

class Manage_department(GridLayout):
    def adding_deparment(self):
        layout = Factory.Add_department()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_departmentList(self):
        layout = Factory.Return_departmentList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
  


class Add_department(GridLayout):
    pass

class Return_departmentList(BoxLayout):
    pass
class Manage_doctor(GridLayout):
    def adding_doctor(self):
        layout = Factory.Add_doctor()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_doctorList(self):
        layout = Factory.Return_doctorList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_doctor(GridLayout):
    pass

class Return_doctorList(BoxLayout):
    pass

class Manage_nurse(GridLayout):
    def adding_nurse(self):
        layout = Factory.Add_nurse()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_nurseList(self):
        layout = Factory.Return_nurseList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_nurse(GridLayout):
    pass

class Return_nurseList(BoxLayout):
    pass

class Manage_pharm(GridLayout):
    def adding_pharm(self):
        layout = Factory.Add_pharm()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_pharmList(self):
        layout = Factory.Return_pharmList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_pharm(GridLayout):
    pass

class Return_pharmList(BoxLayout):
    pass

class Manage_Lab(GridLayout):
    def adding_lab(self):
        layout = Factory.Add_lab()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_labList(self):
        layout = Factory.Return_labList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_lab(GridLayout):
    pass

class Return_labList(BoxLayout):
    pass


################### manage accountx ##############################

class Manage_Accountant(GridLayout):
    def adding_accountant(self):
        layout = Factory.Add_accountant()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_accountantList(self):
        layout = Factory.Return_accountantList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_accountant(GridLayout):
    pass

class Return_accountantList(BoxLayout):
    pass
################ Doctor ###########################

class ScreenDoctor(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenDoctor, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def patient(self):
        layout = Factory.Patient_list()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def dashboard(self):
        layout = Factory.Doctor_dashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Appointment()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def prescription_list(self):
        layout = Factory.Manage_Prescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def allotment_list(self):
        layout = Factory.Bed_allotement()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def report_list(self):
        layout = Factory.Manage_Report()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def patient_select(self):
        
        layout = Factory.Selected_patient()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        print("pressed")
        
    def reallotment_list(self):
        layout = Factory.Return_allotmentList()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

    def adding_Allotment(self):
        layout = Factory.Add_allotment()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

    
        


class Bed_allotement(GridLayout):
    def adding_Allotment(self):
        layout = Factory.Add_allotment()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

    def allotment_list(self):
        layout = Factory.Return_allotmentList()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)


class Add_allotment(GridLayout):
    pass

class Return_allotmentList(BoxLayout):
    pass
    
class Manage_Report(GridLayout):
    def adding_report(self):
        layout = Factory.Add_Report()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

    def Report_list(self):
        layout = Factory.Return_reportList()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

class Add_Report(GridLayout):
    pass

class Return_reportList(BoxLayout):
    pass
class Manage_Blood(GridLayout):
    pass
class Manage_Profile(GridLayout):
    pass
    
class ImageButton(ButtonBehavior, Image):  
    def on_press(self):  
        print ('pressed')

class Selected_patient(GridLayout):
    pass

######################### login #################################

class ScreenLogin(Screen):
    password = ObjectProperty()
    username = ObjectProperty()
    tablename = ObjectProperty()
    
    def user_input(self):
        if self.username.text and self.password.text:
            return self.validate_login()
        
        else:
            return self.input_empty()

    def input_empty(self):

        self.content = Label(text='username or password cannot be empty')
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.4, .3))
        
        self.popup.open()
        a = self.manager.current = 'Login' 
        
        
    def validate_login( self,**kwargs):
        tablename = self.tablename.text
        c.execute("SELECT * FROM {tn} WHERE Name = ? AND Password = ?".format(tn = tablename),(self.username.text, self.password.text))
        data = c.fetchall()
        #a = self.manager.current = 'Doctor'
        if data:
            return self.validate_table()
        else:
            return self.relogin_popup()

    def validate_table(self):
        tablename = self.tablename.text
        if tablename == 'Doctor':
            self.manager.current ='Doctor'
        else:
            pass
        if tablename == 'Admin':
            self.manager.current ='Admin'
        else:
            pass
        if tablename == 'Pharm':
            self.manager.current ='Pharmascist'
        else:
            pass
        if tablename == 'Nurse':
            self.manager.current ='Nurse'
        else:
            pass
        if tablename == 'Lab':
            self.manager.current ='Labaratorist'
        else:
            pass
        if tablename == 'Account':
            self.manager.current ='Accountant'
        else:
            pass
        
    def relogin_popup(self):
        self.content = Label(text='Invalid username or password')
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()
        a = self.manager.current = 'Login' 



class Manager(ScreenManager):

    screen_login = ObjectProperty()
    screen_doctor = ObjectProperty()
    screen_accountant = ObjectProperty()
    screen_labaratorist = ObjectProperty()
    screen_Nurse = ObjectProperty()
    screen_pharmascist = ObjectProperty()
    screen_admin = ObjectProperty()

class ScreenApp(App):
    title = 'Hospital Management System'
    change_layout =Manage_Prescription()
    rv = Patient_list()
    
    rv1 = Appointment()
    rv2 = Manage_Prescription()
    def build(self):
        
        n= Manager(transition=WipeTransition())
        
        
        return n 

if __name__ == "__main__":
    ScreenApp().run()
