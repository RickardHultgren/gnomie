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
from kivy.uix.scrollview import ScrollView
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
mindf_timers = JsonStore('mindf_timers.json')
temp_timers = dict(JsonStore('mindf_timers.json'))
mindf_timers_cpy = dict()
#mindf_timers.put(str(theitem), itemtype=topic, name=theitem)

for key in temp_timers:
	counting = 0
	subdict = temp_timers[key]
	thekey = str()
	thevalue = str()
	for subkey in subdict:
		if counting == 0:
			thekey = subdict[subkey]
			counting += 1
		elif counting == 1:
			thevalue = subdict[subkey]
			mindf_timers_cpy[thevalue] = thekey
			thekey=str()
			thevalue=str()
			counting = 0

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
                    text: '?'
                    font_name: 'DejaVuSerif-Bold'
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
	
	popscroll=ScrollView(size= box.size, bar_pos_x="top")

	popbox=GridLayout(
                cols=1,
                orientation='vertical',
                #height=self.minimum_height,
                #height=root.bigheight,
                #padding= (thescroll.width * 0.02, thescroll.height * 0.02),
                #spacing= (thescroll.width * 0.02, thescroll.height * 0.02),
                size_hint_y= None,
                size_hint_x= 1,
                do_scroll_x= False,
                do_scroll_y= True,
                )

	popscroll.add_widget(popbox)	
	
	popup1 = Popup(content=box, size_hint=(.75, .75))
	box.add_widget(popscroll)
	if fontheight*(len(main_choices[topic])/line_len) > fontheight :
		txt_height=0*fontheight+fontheight*(len(main_choices[topic])/line_len)
	else:
		txt_height=fontheight


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
				self.popbox.clear_widgets()
				#self.box.clear_widgets()
				self.popup1.dismiss()
			except:
				pass
			
		self.ids.main_box.height=self.main_height
		main_txt=Label(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif")#, font_size=self.fontheight)
		main_txt.bind(width=lambda s, w:
			   s.setter('text_size')(s, (self.width-.1*self.ids.main_box.width, None)))
		main_txt.bind(height=main_txt.setter('texture_size[1]'))
		main_txt.bind(height=main_txt.setter('self.minimum_height'))
		main_txt.text=str("%s"%self.main_choices[self.topic])
		
		self.ids.main_box.add_widget(main_txt)
		
		if self.topic == "start":
			start_bttn1=Button(
				text= 'mindfulness',
				size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",
				background_color=(.25, .75, 1.0, 1.0)
				)
			start_bttn2=Button(
				text= 'statements',
				size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",
				background_color=(.25, .75, 1.0, 1.0)
				)
			start_bttn3=Button(
				text= 'statistics',
				size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",
				background_color=(.25, .75, 1.0, 1.0)
				)
			start_bttn1.bind(on_release=lambda start_bttn1: self.mindf())
			start_bttn2.bind(on_release=lambda start_bttn2: self.state())
			start_bttn3.bind(on_release=lambda start_bttn3: self.stast())
			self.ids.main_box.add_widget(start_bttn1)
			self.ids.main_box.add_widget(start_bttn2)
			self.ids.main_box.add_widget(start_bttn3)
		if self.topic == "mindf":
			parts = ["Breath calm and Relax muscles","Feel muscles and organs","Feel sensations","Feel inner state","Feel inner awareness","End of mindfulness"]
			main_txt.text=parts[self.mindf_part]
			mindf_bar=ProgressBar(
				max=self.mindf_limit
				)
			mindf_bar.value=self.mindf_time
			self.ids.main_box.add_widget(mindf_bar)
			
			nxt_bttn=Button(text="next",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif")
			nxt_bttn.bind(on_release=lambda nxt_bttn: self.nxtb())
			prv_bttn=Button(text="previous",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif")
			self.ids.main_box.add_widget(nxt_bttn)
			prv_bttn.bind(on_release=lambda prv_bttn: self.prevb())
			self.ids.main_box.add_widget(prv_bttn)
			exit_bttn=Button(text="exit",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif")
			exit_bttn.bind(on_release=lambda prv_bttn: self.exitb())
			self.ids.main_box.add_widget(exit_bttn)			
			if self.mindf_time == self.mindf_limit and self.mindf_part <= 5:
				if self.mindf_part == 5:
					self.mindf_time = 0
				else:
					self.mindf_part+=1
					self.mindf_time = 0
			elif self.mindf_part != 5:		
				self.mindf_time+=1
		
	def prevb(self):
		if self.mindf_part != 0:
			self.mindf_part -= 1
		self.mindf_time = 0
		
	def nxtb(self):
		if self.mindf_part != 5:
			self.mindf_part += 1
		self.mindf_time = 0
			
	def exitb(self):
		self.mindf_part = 0
		self.mindf_time = 0
		self.topic="start"
		self.planupdate()
			
	def start(self):
		self.topic="start"
		self.planupdate()
	
	def about(self):
		try:
			self.popbox.clear_widgets()
		except:
			pass
		try:
			self.popup1.dismiss()
		except:
			pass
		self.popup1.title="about"
		about_txt=Label(text = 'Gnomie is an open source app licensed under\nthe BSD2-license. The founder and principal developer is\nRickard Verner Hultgren',size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif")
		self.popbox.add_widget(about_txt)
		
		exit_bttn=Button(text="OK",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif")
		exit_bttn.bind(on_release=lambda prv_bttn: self.popup1.dismiss())
		self.popbox.add_widget(exit_bttn)			

		self.popup1.open()
	
	def mindf(self):
		try:
			self.popbox.clear_widgets()
		except:
			pass
		try:
			self.popup1.dismiss()
		except:
			pass
		self.topic="mindf"
		self.popup1.title="mindfulness"
		self.popbox.add_widget(Label(text = 'For how long time do you want to exercise mindfulness?', font_name="DejaVuSerif"))
		new_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif")
		new_box_title = TextInput(text="", multiline=True)
		new_box_min = TextInput(text="timer name", multiline=True)
		new_box.add_widget(Label(text = 'min', size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif"))
		new_box_add=Button(text = 'add',size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif")
		new_box_add.bind(on_release=lambda new_box_add: self.add_new(new_box_title.text, new_box_min.text))
		new_box.add_widget(new_box_title)
		new_box.add_widget(new_box_min)
		new_box.add_widget(new_box_add)
		self.popbox.add_widget(new_box)
		
		###now
		for timer_item in mindf_timers_cpy: #Go through stored statements
			


			timer_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif")
			timer_box_title = Label(text=timer_item, size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif")
			#timer_box_min = Label(text="%s min"%str(timer_item[mindf_timers_cpy]), size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif")
			timer_box_min = Label(text="min", size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif")
			timer_box_add=Button(text = 'del',size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif")
			#timer_box_add.bind(on_release=lambda timer_box_add: self.add_new(timer_box_title.text, timer_box_min.text))
			timer_box.add_widget(timer_box_title)
			timer_box.add_widget(timer_box_min)
			timer_box.add_widget(timer_box_add)
			self.popbox.add_widget(timer_box)
			#mindf_timers_cpy[timer_item] = {'vis':self.viss, 'mis':self.miss, 'obj':self.objs}	
			#bind. on_release mindf_timers.put(str(status), vis=self.viss, mis=self.miss, obj=self.objs)		
		#	timer_button=Button(text = settingdata.get('title')['address'],on_release=(lambda btn2: self.bttn2()))
		#	mindf_timers.put('title', ###)
		
		self.popup1.open()

	def add_new(self,mindf_time,mindf_title):
		
		mindf_timers.put(str(mindf_title), title=mindf_title, time=mindf_time)				
		self.planupdate()
		
	def bttn2(self):
		self.mindf_speed=4
		self.mindf_limit=100
		self.popup1.dismiss()
		self.mindf_part = 0
		self.mindf_time = 0
		Clock.unschedule(self.planupdate)		
		Clock.schedule_interval(self.planupdate, 0.2)

	def bttn4(self):
		self.mindf_speed=4
		self.mindf_limit=100
		self.popup1.dismiss()
		self.mindf_part = 0
		self.mindf_time = 0
		Clock.unschedule(self.planupdate)		
		Clock.schedule_interval(self.planupdate, 0.2)
		
	def state(self):
		self.topic="state"
		self.planupdate()

	def stast(self):
		self.topic="stast"
		self.planupdate()

class emadrsApp(App):
	def build(self):
		the_screenmanager = ScreenManager()
		#the_screenmanager.transition = FadeTransition()
		mainscreen = MainScreen(name='mainscreen')
		the_screenmanager.add_widget(mainscreen)
		return the_screenmanager
		
if __name__ == '__main__':
	emadrsApp().run()
