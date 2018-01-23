# coding:utf-8
import kivy
kivy.require('1.7.2') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.storage.jsonstore import JsonStore
from kivy.uix.gridlayout import GridLayout
from functools import partial
#from kivy.uix.treeview import TreeView, TreeViewNode
#from kivy.uix.treeview import TreeViewLabel
#from kivy.uix.scrollview import ScrollView
try:
	from plyer import sms
except:
	pass
	
from kivy.core.text import LabelBase  
KIVY_FONTS = [
    {"name":"DejaVuSerif",  
                   "fn_regular":"ttf/DejaVuSerif.ttf",
                   "fn_bold":"ttf/DejaVuSerif-Bold.ttf",
                   "fn_italic":"ttf/DejaVuSerif-Italic.ttf",
                   "fn_bolditalic":"ttf/DejaVuSerif-BoldItalic.ttf"
                   }
                   ]
for font in KIVY_FONTS:
    LabelBase.register(**font)

#Declaration of global variables:
settingdata = JsonStore('settingdata.json')

Builder.load_string('''
<MainScreen>:
    name: 'mainscreen'
    canvas.before:
        Color:
            rgba: 0, .125, .125, 1
        Rectangle:
            pos: self.pos
            size: self.size
    GridLayout:
    
        row_default_height:root.height / 8
		cols:1
        orientation: 'vertical'
        ActionBar:
            
            width:root.width
            height:root.height / 8
            background_color:255,0,0,.5
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    #title: 'gnomie'
                    title: ''
                    app_icon: 'gnomie.png'
                    with_previous: False
                    on_release: root.start()
                ActionGroup:
                    mode: 'spinner'
                    text: 'MENU'
                    font_name: 'DejaVuSerif-Bold'
                    ActionButton:
                        text: 'mindfulness'
                        font_name: 'DejaVuSerif'
                        on_release: root.mindf()
                        background_color:255,0,0,1
                    ActionButton:
                        text: 'statements'
                        font_name: 'DejaVuSerif'
                        on_release: root.state()
                        background_color:255,0,0,1
                    ActionButton:
                        text: 'statistics'
                        font_name: 'DejaVuSerif'
                        on_release: root.stast()
                        background_color:255,0,0,1
                    ActionButton:
                        text: 'about'
                        font_name: 'DejaVuSerif'
                        on_release: root.about()
                        background_color:255,0,0,1                        
        ScrollView:
            size: self.size
            GridLayout:
                cols:1
                orientation:'vertical'
                #height:self.minimum_height
                #height:root.main_height
                padding: root.width * 0.02, root.height * 0.02
                spacing: root.width * 0.02, root.height * 0.02            
                size_hint_y: None
                size_hint_x: 1            
                do_scroll_x: False
                do_scroll_y: True
                id: main_box

''')  

class MainScreen(Screen):
	nownr=0
	main_height=NumericProperty()
	fontheight=15
	line_len=30
	main_choices = {
	'start': "\n\nWelcome to my little home!\nI'm Gnomie the gnome.\nWhat choice pleases, when you\nwill pick from the menu?",
	'mindf': '\n\n',
	'state': '\n\n',
	'stast': '\n\n'}
	#print "dict['Name']: ", dict['Name']
	topic='start'
	mindf_time=NumericProperty(0)
	mindf_part=0
	mindf_limit=0
	mindf_speed=0
	box = BoxLayout(orientation='vertical')
	popup1 = Popup(content=box, size_hint=(.75, .75))
	def __init__ (self,**kwargs):
		super (MainScreen, self).__init__(**kwargs)
		self.planupdate()
	
	def planupdate(self,*args):
		self.main_height=0
		try:
			self.ids.main_box.clear_widgets()
		except:
			pass
		if self.topic != 'mindf' :
			try:
				Clock.unschedule(self.planupdate)
			except:
				pass
		try:
			self.popup.clear_widgets()
		except:
			pass	
		try:
			self.popup1.dismiss()
		except:
			pass	
			
		self.ids.main_box.height=self.main_height
		if self.fontheight*(len(self.main_choices[self.topic])/self.line_len) > self.fontheight :
			txt_height=0*self.fontheight+self.fontheight*(len(self.main_choices[self.topic])/self.line_len)
		else:
			txt_height=self.fontheight
		main_txt=Label(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(txt_height)),font_name="DejaVuSerif")#, font_size=self.fontheight)
		main_txt.bind(width=lambda s, w:
			   s.setter('text_size')(s, (self.width-.1*self.ids.main_box.width, None)))
		main_txt.bind(height=main_txt.setter('texture_size[1]'))
		main_txt.bind(height=main_txt.setter('self.minimum_height'))
		main_txt.text=str("%s"%self.main_choices[self.topic])
		
		if self.topic == "start":
			pass
		if self.topic == "mindf":
			parts = ["Breath calm and Relax muscles","Feel muscles and organs","Feel sensations","Feel inner state","Feel inner awareness","End of mindfulness"]
			main_txt.text=parts[0]
			mindf_bar=ProgressBar(
				value=self.mindf_time,
				max=self.mindf_limit
				)
			self.ids.main_box.add_widget(mindf_bar)
			if self.mindf_time >= self.mindf_limit and self.mindf_part < 5 and self.mindf_part >= 0:
				if self.mindf_part == 5:
					self.mindf_time = 0
				else:
					self.mindf_part+=1
					self.mindf_time = 0
			elif self.mindf_part != 5:		
				self.mindf_time+=1
			###now
			self.mindf_time+=1
			print self.mindf_time
		self.ids.main_box.add_widget(main_txt)

	def start(self):
		self.topic="start"
		self.planupdate()
		
	def mindf(self):
		self.topic="mindf"
		self.popup1.title="mindfulness"
		self.box.add_widget(Label(text = 'For how long time do you want to exercise mindfulness?'))
		btn2=Button(text = '2 min?',on_release=(lambda btn2: self.bttn2()))
		btn4=Button(text = '4 min?',on_release=(lambda btn2: self.bttn4()))
		self.box.add_widget(btn2)
		self.box.add_widget(btn4)
		self.popup1.open()
		
	def bttn2(self):
		self.mindf_speed=4
		Clock.schedule_interval(self.planupdate, 0.2)

	def bttn4(self):
		self.mindf_speed=4
		Clock.schedule_interval(self.planupdate, 0.2)
		
	def state(self):
		self.topic="state"
		self.planupdate()

	def stast(self):
		self.topic="stast"
		self.planupdate()

	def about(self):
		box = BoxLayout(orientation='vertical')
		popup1 = Popup(title='About', content=box, size_hint=(None, None), size=(400, 400))
		self.add_widget(Label(text='Gnomie is an open source app licensed under\nthe BSD2-license. The founder and principal developer is\nRickard Verner Hultgren'))

		store_btn = Button(text='OK')
		store_btn.bind(on_release=lambda store_btn: popup1.dismiss())
		self.add_widget(store_btn)
		#popup1 = Popup(title='Add goal', content=box, auto_dismiss=True, size_hint=(None, None), size=(400, 400))
		popup1.open()

	
class emadrsApp(App):
	def build(self):
		the_screenmanager = ScreenManager()
		#the_screenmanager.transition = FadeTransition()
		mainscreen = MainScreen(name='mainscreen')
		the_screenmanager.add_widget(mainscreen)
		return the_screenmanager
		
if __name__ == '__main__':
	emadrsApp().run()
