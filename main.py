import kivy
#from datetime import datetime, timedelta

kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.button import Button
#from kivy.uix.gridlayout import GridLayout
#from functools import partial
from kivy.lang import Builder
from kivy.uix.popup import Popup
#from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
#from kivy.uix.treeview import TreeView, TreeViewNode
#from kivy.uix.treeview import TreeViewLabel
#from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
#import time

from kivy.uix.progressbar import ProgressBar
#from kivy.clock import Clock

#from kivy.uix.bubble import Bubble
#from kivy.uix.bubble import BubbleButton



#class TreeViewButton(Button, TreeViewNode):
#	pass

#thedate = thedate=datetime.now().strftime("%Y%m%d")
#markedlines=list()

#my_screenmanager = ScreenManager()
mngr="start"
Builder.load_string('''
<StartScreen>:
	name: 'startscreen'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Welcome to gnomie!'
            Button:
                text: 'About'
                on_release: root.About
        Label:
            text: ''
        Button:
            text: 'How are you?'
            on_release: app.root.current = 'reviewscreen'
        Label:
            text: ''
        Button:
            text: 'Are you really sure you are there?'
            on_release: app.root.current = 'mfscreen'
        Label:
            text: ''
        Button:
            text: 'What are your plans?'
            on_release: app.root.current = 'planscreen'
<ReviewScreen>:
    name: 'reviewscreen'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
<MFScreen>:
    name: 'mfscreen'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        Label:
            text: 'For how long time do you want to exercise mindfulness?'
        Label:
            text: ''
        Button:
            text: '2 min?'
            on_release: root.two()
        Label:
            text: ''
        Button:
            text: '4 min'
            on_release: root.four()
        Label:
            text: ''
        Button:
            text: 'Back to start?'
            on_release: app.root.current = 'startscreen'
<ExeScreen>:
    name: 'exescreen'
    orientation: 'vertical'
    MFExe:
    
<MFExe>:
    anchor_x: 'center'
    anchor_y: 'top'
    orientation: 'vertical'
    padding: 50
    ProgressBar:
        value: root.nowtime
        max: root.limit
    Label:
        text: root.parts[root.nowpart]
    Button:
        text: "Next"
        #on_release: if root.nowpart < 4: root.nowpart += 1
        on_release: root.Next()
    Button:
        text: "Previous"
        on_release: root.Prev()
    Button:
        text: "Exit"
        on_release: root.Exit()
<PlanScreen>:
    name: 'planscreen'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
''')
the_screenmanager = ScreenManager()
endtime = 0	
class PlanScreen(Screen):
	def __init__ (self,**kwargs):
		super (PlanScreen, self).__init__(**kwargs)
		pass

class MFScreen(Screen):
	global endtime
	global the_screenmanager
	global mngr
	def __init__ (self,**kwargs):
		global endtime
		super (MFScreen, self).__init__(**kwargs)
	def two(self):
		global the_screenmanager
		global endtime
		global mngr
		mngr='exescreen'		
		endtime=120
		the_screenmanager.current = 'exescreen'

	def four(self):
		global the_screenmanager
		global endtime
		global mngr
		mngr='exescreen'		
		endtime=240
		the_screenmanager.current = 'exescreen'

class ExeScreen(Screen):
	pass		
	
class MFExe(BoxLayout):
	global mngr
	global the_screenmanager
	global endtime
	nowtime = NumericProperty(0)
	#limit=NumericProperty(eval(str(endtime)))
	limit=NumericProperty(0)
	parts = ["Breath calm and Relax muscles","Feel muscles and organs","Feel sensations","Feel inner state","Feel inner awareness","End of mindfulness"]
	nowpart = NumericProperty(0)
	def __init__ (self,**kwargs):
		#global the_screenmanager
		#global endtime
		super (MFExe, self).__init__(**kwargs)
		#if mngr == 'exescreen':
		#	Clock.schedule_interval(self.update, 0.25)
		Clock.schedule_interval(self.update, 0.2)
		
	def update(self, dt):
		self.limit=endtime
		global mngr
		if mngr == "exescreen":
			if self.nowtime >= self.limit and self.nowpart < 5 and self.nowpart >= 0:
				if self.nowpart == 5:
					self.nowtime = 0
				else:
					self.nowpart+=1
					self.nowtime = 0
			elif self.nowpart != 5:		
				self.nowtime+=1
		#print self.nowtime
		#print mngr
		#print self.limit
	
	def Next(self):
		if self.nowpart < 5:
			self.nowpart += 1
			self.nowtime=0

	def Prev(self):
		if self.nowpart > 0:
			self.nowpart -= 1
			self.nowtime=0
			
	def Exit(self):
		global the_screenmanager
		global mngr
		self.nowpart = 0
		self.nowtime=0						
		mngr = 'start'
		the_screenmanager.current = 'mfscreen'
			
		
		
#https://stackoverflow.com/questions/40341674/update-kivy-label-using-screen-manager

class ReviewScreen(Screen):
	def __init__ (self,**kwargs):
		super (ReviewScreen, self).__init__(**kwargs)
		#print "hej"
		pass


class StartScreen(Screen):
	#global thedate
	def __init__ (self,**kwargs):
		#global thedate
		super (StartScreen, self).__init__(**kwargs)
	def About():
		pass		
		
class GnomieApp(App):
	global my_screenmanager
	def build(self):
		global my_screenmanager
		#the_screenmanager = ScreenManager()
		startscreen = StartScreen(name='startscreen')
		reviewscreen = ReviewScreen(name='reviewscreen')
		mfscreen = MFScreen(name='mfscreen')
		exescreen = ExeScreen(name='exescreen')
		planscreen = PlanScreen(name='planscreen')
		
		#if mngr=='start':
		the_screenmanager.add_widget(startscreen)
		the_screenmanager.add_widget(reviewscreen)
		the_screenmanager.add_widget(mfscreen)
		the_screenmanager.add_widget(exescreen)
		the_screenmanager.add_widget(planscreen)
		return the_screenmanager
		
		
		
if __name__ == '__main__':
	GnomieApp().run()
