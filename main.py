import kivy
#from datetime import datetime, timedelta

kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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
#mngr="start"
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
            on_release: root.start=2
        Label:
            text: ''
        Button:
            text: '5 min'
            on_release: root.start=5
        Label:
            text: ''
        Button:
            text: 'Back to start?'
            on_release: app.root.current = 'startscreen'
<PlanScreen>:
    name: 'planscreen'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
''')

class PlanScreen(Screen):
	def __init__ (self,**kwargs):
		super (PlanScreen, self).__init__(**kwargs)
		pass

class MFScreen(Screen):
	
	start = 0
	limit = 0
	endtime = 0
	nowtime = 0
	nr = 0
	parts = ["Breath calm and Relax muscles","Feel muscles and organs","Feel sensations","Feel inner state","Feel inner awareness"]

	#def __init__ (self,**kwargs):
		#super (MFScreen, self).__init__(**kwargs)
		#pass

	def update(self,dt):
		
		if self.start != 0:
			self.endtime = self.start 
			self.limit = self.start 
			self.start = 0
			box = BoxLayout(orientation='vertical')
			popup1 = Popup(title='%s min mindfulness'%(self.start), content=box, auto_dismiss=True, size_hint=(None, None), size=(400, 400))

			a1slider = ProgressBar(
			value= self.nowtime,
			max=self.endtime,
			min=0,
			size_hint_y=None,
			size_hint_x=1,
			orientation='horizontal'#,
			#id="a1slider",
			#height= 7*(a1text00.height)
			
			)
		
			a1slider.bind(height=a1slider.setter('self.minimum_height'))
			box.add_widget(a1slider)
		
			box.add_widget(Label(text=self.parts[self.nr]))

			next_btn = Button(text='next mindfulness')
			next_btn.bind(on_release=lambda store_btn: self.nextpopup(popup1))
			box.add_widget(next_btn)

			exit_btn = Button(text='Exit mindfulness')
			exit_btn.bind(on_release=lambda store_btn: self.exitpopup(popup1))
			box.add_widget(exit_btn)
			
			popup1.open()
		self.nowtime -= 1

	def five(self):
		box = BoxLayout(orientation='vertical')
		popup1 = Popup(title='5 min mindfulness', content=box, auto_dismiss=True, size_hint=(None, None), size=(400, 400))
	
		box.add_widget(Label(text='take a deep breath...'))

		exit_btn = Button(text='Exit mindfulness')
		exit_btn.bind(on_release=lambda store_btn: self.exitpopup(popup1))
		box.add_widget(exit_btn)
		
		popup1.open()
		
	def exitpopup(self,popup1):
		popup1.dismiss()
		
	def nextpopup(self,popup1):
		popup1.dismiss()
		if self.nr < 4:
			self.nr += 1
		box = BoxLayout(orientation='vertical')
		popup1 = Popup(title='2 min mindfulness', content=box, auto_dismiss=True, size_hint=(None, None), size=(400, 400))
	
		box.add_widget(Label(text=self.parts[self.nr]))

		if self.nr < 4:
			next_btn = Button(text='next step')
			next_btn.bind(on_release=lambda store_btn: self.nextpopup(popup1))
			box.add_widget(next_btn)
		if self.nr > 0:
			next_btn = Button(text='previous step')
			next_btn.bind(on_release=lambda store_btn: self.prevpopup(popup1))
			box.add_widget(next_btn)

		exit_btn = Button(text='Exit mindfulness')
		exit_btn.bind(on_release=lambda store_btn: self.exitpopup(popup1))
		box.add_widget(exit_btn)
		
		popup1.open()

	def prevpopup(self,popup1):
		popup1.dismiss()
		if self.nr > 0:
			self.nr -= 1
		box = BoxLayout(orientation='vertical')
		popup1 = Popup(title='2 min mindfulness', content=box, auto_dismiss=True, size_hint=(None, None), size=(400, 400))
	
		box.add_widget(Label(text=self.parts[self.nr]))

		if self.nr > 0:
			next_btn = Button(text='next step')
			next_btn.bind(on_release=lambda store_btn: self.nextpopup(popup1))
			box.add_widget(next_btn)
		if self.nr > 0:
			next_btn = Button(text='previous step')
			next_btn.bind(on_release=lambda store_btn: self.prevpopup(popup1))
			box.add_widget(next_btn)

		exit_btn = Button(text='Exit mindfulness')
		exit_btn.bind(on_release=lambda store_btn: self.exitpopup(popup1))
		box.add_widget(exit_btn)
		
		popup1.open()
		

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
	#global my_screenmanager
	def build(self):
		#global my_screenmanager
		the_screenmanager = ScreenManager()
		startscreen = StartScreen(name='startscreen')
		reviewscreen = ReviewScreen(name='reviewscreen')
		mfscreen = MFScreen(name='mfscreen')
		planscreen = PlanScreen(name='planscreen')
		Clock.schedule_interval(mfscreen.update, 0.25)
		#if mngr=='start':
		the_screenmanager.add_widget(startscreen)
		the_screenmanager.add_widget(reviewscreen)
		the_screenmanager.add_widget(mfscreen)
		the_screenmanager.add_widget(planscreen)
		return the_screenmanager
		#return HomeScreen()
		
if __name__ == '__main__':
	GnomieApp().run()
