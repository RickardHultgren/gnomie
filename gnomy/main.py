# coding:utf-8
import kivy
kivy.require('1.7.2') # replace with your current kivy version !
import kivy.garden
#from kivy.garden.graph import Graph, MeshLinePlot
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
#from kivy.graphics import BorderImage

from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton
from kivy.utils import platform

try:
	from plyer import tts
except:
	pass

try:
	from plyer import vibrator
except:
	pass

####
#if platform == 'android':
#	from jnius import autoclass

#	PythonActivity = autoclass('org.renpy.android.PythonActivity')
#	Intent = autoclass('android.content.Intent')
	
#	intent = Intent()
#	intent.setType("vnd.android.cursor.item/event")
#	intent.setAction(Intent.ACTION_VIEW)
#	PythonActivity.mActivity.startActivity(intent)
####

from kivy.core.window import Window
	
from kivy.core.text import LabelBase  
KIVY_FONTS = [
    {"name":"DejaVuSerif",  
                   "fn_regular":"DejaVuSerif.ttf",
                   "fn_bold":"DejaVuSerif-Bold.ttf",
                   "fn_italic":"DejaVuSerif-Italic.ttf",
                   "fn_bolditalic":"DejaVuSerif-BoldItalic.ttf"
                   }
                   ]
for font in KIVY_FONTS:
    LabelBase.register(**font)

if platform == 'android':
	from jnius import autoclass
	PythonActivity = autoclass('org.renpy.android.PythonActivity')
	
	Environment = autoclass('android.os.Environment')
	FileClass = autoclass("java.io.File")
	fG = FileClass('/storage/emulated/0/gnomie/')
	
	if not fG.exists():
		fG.mkdir()
	
	try:
		mindf_things = JsonStore('/storage/emulated/0/gnomie/mindf_things.json')
		temp_timers = dict(JsonStore('/storage/emulated/0/gnomie/mindf_things.json'))
	except:
		pass
	try:
		state_things = JsonStore('/storage/emulated/0/gnomie/state_things.json')
		temp_claims = dict(JsonStore('/storage/emulated/0/gnomie/state_things.json'))
	except:
		pass
	try:
		think_things = JsonStore('/storage/emulated/0/gnomie/think_things.json')
		temp_think = dict(JsonStore('/storage/emulated/0/gnomie/think_things.json'))
	except:
		pass
	try:
		setting_things = JsonStore('/storage/emulated/0/gnomie/settings.json')
		temp_set = dict(JsonStore('/storage/emulated/0/gnomie/settings.json'))	
	except:
		pass

else:
	try:
		mindf_things = JsonStore('mindf_things.json')
		temp_timers = dict(JsonStore('mindf_things.json'))
	except:
		pass
	try:
		state_things = JsonStore('state_things.json')
		temp_claims = dict(JsonStore('state_things.json'))
	except:
		pass
	try:
		think_things = JsonStore('think_things.json')
		temp_think = dict(JsonStore('think_things.json'))
	except:
		pass
	try:
		setting_things = JsonStore('settings.json')
		temp_set = dict(JsonStore('settings.json'))
	except:
		pass

mindf_things_cpy = dict()
state_things_cpy = dict()
think_things_cpy = dict()
temp_set_cpy = dict()

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
			mindf_things_cpy[thevalue] = thekey
			thekey=str()
			thevalue=str()
			counting = 0

for key in temp_claims:
	counting = 0
	subdict = temp_claims[key]
	thekey = str()
	thevalue = str()
	for subkey in subdict:
		if counting == 0:
			thekey = subdict[subkey]
			counting += 1
		elif counting == 1:
			thevalue = subdict[subkey]
			state_things_cpy[thevalue] = thekey
			thekey=str()
			thevalue=str()
			counting = 0

for key in temp_set:
	counting = 0
	subdict = temp_set[key]
	thekey = str()
	thevalue = str()
	for subkey in subdict:
		thekey = subkey
		thevalue = subdict[subkey]
		temp_set_cpy[thekey] = thevalue
		thekey=str()
		thevalue=str()
		counting = 0

thekey = str()
thevalue = str()
for akey in temp_think :
	think_things_cpy[str(akey)] = temp_think[akey]

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
    
        #row_default_height:root.height / 8
        row_default_height:"32sp"
		cols:1
        orientation: 'vertical'
        ActionBar:
            #height:root.height / 8
            height:"64sp"
            #height:"32pt"
            width:root.width
            background_color:255,0,0,.5
            pos_hint: {'top':1}    
            padding: '2ssp'
            canvas:
                Color:
                    rgba: self.background_color
                #BorderImage:
                    #pos: self.pos
                    #size: self.size
                    #source: "bg1.png"
                    
            ActionView:
                
                
                ActionPrevious:
                    #title: 'gnomy'
                    #title: ''
                    app_icon: 'gnomy.png'
                    with_previous: False
                    on_release: root.mindf()
                    #on_press: root.start()
                    #background_normal: ''
                    #background_color: 1, .3, .4, .85
                ActionGroup:
                
					text: "|||"
					#icon: './menu.png'
                
                    #font_size:"48sp"
                    font_size:"16sp"
                    #orientation: 'horizontal'
                    mode: 'spinner'
                    background_color:255,0,0,.5
                    background_down: ''
                    background_disabled_normal: ''
                    #border: 60, 60, 60, 3      
                    text_width:'48ssp'              
                    canvas.before:
                        PushMatrix
                        Rotate:
                            angle: 90
                            origin: self.center
                    canvas.after:
                        PopMatrix
                    ActionButton:
                        text: 'about'
                        font_name: 'DejaVuSerif'
                        on_release: root.about()
                        background_color:255,0,0,1
                    ActionButton:
                        text: 'settings'
                        font_name: 'DejaVuSerif'
                        on_release: root.settings()
                        background_color:255,0,0,1                    

                   
        GridLayout:
            cols:1
            id: megabox
''')  

class MainScreen(Screen):
	#global the_screenmanager
	global mindf_things_cpy
	global state_things_cpy
	global think_things_cpy
	nownr=0
	main_height=NumericProperty()
	fontheight=15
	line_len=30
	main_headline = {
	'settings' : "Settings",
	'start' : "\n\n\n\nWelcome to my little home!\nI'm Gnomie the gnome.\n\n\n\n",
	'mindf' : '\n\n',
	'state' : '\n\n',
	'stati' : '\n\n'}
	pop_choices = {
	'settings' : '\n\n',
	'start' : '\n\n',
	'mindf' : [mindf_things_cpy],
	'state' : [state_things_cpy, think_things_cpy],
	'stati' : '\n\n'}
	main_buttons = {
	'settings' : [],
	#'start' : ["mindfulness", "statements", "statistics"],
	'start' : [],
	'mindf' : ["<<",">>","||","cycle ON"],
	'state' : [],
	'stati' : '\n\n'}
	topic='start'
	state_topic='obj'
	state_sub_topic='plan'
	mindf_time=NumericProperty(0)
	mindf_part=0
	paused = False
	going = True
	mindf_limit=0
	mindf_speed=0
	state_claim=""
	cycle = True

	box = BoxLayout(orientation='vertical')
	popscroll=ScrollView(size= box.size, bar_pos_x="top")
	poptop=BoxLayout(orientation='vertical',size_hint_y=.4, size_hint_x=1)
	popbox=GridLayout(
                cols=1,
                orientation='vertical',
                #height=self.minimum_height,
                #height=root.bigheight,
                padding = (popscroll.width * 0.02, popscroll.height * 0.02),
                spacing = (popscroll.width * 0.02, popscroll.height * 0.02),
                size_hint_y= None,
                size_hint_x= 1,
                do_scroll_x= False,
                do_scroll_y= True
                )
	popscroll.add_widget(popbox)
	#87.5% of the screen in X and Y:
	popup1 = Popup(content=box, size_hint=(.875, .875))
	box.add_widget(poptop)
	box.add_widget(popscroll)
	
	txt_height = 0
	pop_rubric = ""
	pop_unit = ""
	pop_action = ""
	pop_unit_name = ""
	pop_title_name = ""

	delbox = BoxLayout(orientation='vertical')
	main_x_scroll=ScrollView(size=delbox.size, bar_pos_x="top")
	main_x_box=GridLayout(
                cols=1,
                orientation='vertical',
                #height=self.minimum_height,
                #height=root.bigheight,
                padding = (main_x_scroll.width * 0.02, main_x_scroll.height * 0.02),
                spacing = (main_x_scroll.width * 0.02, main_x_scroll.height * 0.02),
                size_hint_y = None,
                size_hint_x = 1,
                do_scroll_x = False,
                do_scroll_y = True
                )
	main_x_scroll.add_widget(main_x_box)
	popup2 = Popup(content=delbox, size_hint = (.875, .875))
	delbox.add_widget(main_x_scroll)

	pop_bubble= Bubble(orientation = 'vertical',size_hint=(None, None),size=(600, 100),pos=(200,0))
	
	parts = ["Relax and breathe calmly","breathe in and out","Feel the muscles of the head and neck","of the the arms","of the chest and abdomen","of the legs","Feel the organs of the pelvis and abdomen","Feel the organs of the chest","Feel the sensations of light","smell","taste","sound","touch","Feel inner state and mood","Try to name the mood you feel","Try to feel all the feelings all at once","End of mindfulness"]
	#parts = ["Breath calm and Relax muscles","Feel muscles and organs","Feel sensations","Feel inner state","Feel inner awareness","End of mindfulness"]

	def prevb(self, *args):
		if self.mindf_part != 0:
			self.mindf_part -= 1
		self.mindf_time = 0

	def nxtb(self, *args):
		if self.mindf_part != len(self.parts)-1:
			self.mindf_part += 1
		else:
			self.mindf_part = 0
		self.mindf_time = 0

	def pausing(self, *args):
		if self.paused == False:
			self.paused = True
			Clock.unschedule(self.planupdate)
			self.planupdate()
		else:
			self.paused = False
			Clock.schedule_interval(self.planupdate, 0.2)

	def cycling(self, *args):
		if self.cycle == False:
			self.cycle = True
		else:
			self.cycle = False
				
	def exitb(self, *args):
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
			self.poptop.clear_widgets()
		except:
			pass
		try:
			self.popup1.dismiss()
		except:
			pass
		about_box = BoxLayout(orientation='vertical')
		self.popup1.title="about"
		about_txt=Label(text = 'Gnomie is an open source app licensed under the BSD2-license. The founder and principal developer is Rickard Verner Hultgren',size_hint_y=None, width=self.ids.megabox.width, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		about_txt.bind(width=lambda s, w:
				s.setter('text_size')(s, (self.width, None)))
		about_txt.bind(height=about_txt.setter('texture_size[1]'))
		about_txt.bind(height=about_txt.setter('self.minimum_height'))
		about_box.add_widget(about_txt)
		
		self.popbox.add_widget(about_box)
		self.popbox.height += about_txt.height
		
		exit_bttn=Button(text="OK",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		exit_bttn.bind(on_release=lambda prv_bttn: self.popup1.dismiss())
		self.popbox.add_widget(exit_bttn)			
		self.popbox.height += exit_bttn.height

		self.popup1.open()

	def settings(self):
		self.topic="settings"
		self.planupdate()
	
	def act_tts(self, checkbox, value):
		if value:
			#self.act_ttsvar = True
			
			#set_things_cpy.pop("tts", None)
			#set_things.delete("tts")
			temp_set_cpy['tts'] = "True"
			setting_things.put("tts", tts="True")
		else:
			#self.act_ttsvar = False
			temp_set_cpy['tts'] = "False"
			setting_things.put("tts", tts="False")

	def act_vibr(self, checkbox, value):
		if value:
			#self.act_vibrvar = True
			
			#set_things_cpy.pop("vibr", None)
			#set_things.delete("vibr")
			temp_set_cpy['vibr'] = "True"
			setting_things.put("vibr", vibr="True")
		else:
			#self.act_vibrvar = False
			temp_set_cpy['vibr'] = "False"
			setting_things.put("vibr", vibr="False")
			
	def chng_setname(self, name_inpt, *args):
		temp_set_cpy['setname'] = name_inpt.text
		setting_things.put("setname", setname=name_inpt.text)


	def __init__ (self,**kwargs):
		super (MainScreen, self).__init__(**kwargs)
		self.planupdate()


	def planupdate(self,*args):
		zcroller=ScrollView(size=self.size, bar_pos_x = "top")
		main_box=GridLayout(
		   cols=1,
		   orientation='vertical',
		   #height=self.minimum_height,
		   #height=root.bigheight,
		   #padding= (thescroll.width * 0.02, thescroll.height * 0.02),
		   #spacing= (thescroll.width * 0.02, thescroll.height * 0.02),
		   size_hint_y= None,
		   size_hint_x= 1,
		   do_scroll_x= False,
		   do_scroll_y= True
		   )


		#global the_screenmanager
		self.main_height=0
		try:
			self.ids.megabox.clear_widgets()
		except:
			pass
		if self.topic != "mindf" :
			try:
				self.main_x_box.clear_widgets()
			except:
				pass
			try:
				self.popup1.dismiss()
			except:
				pass
			try:
				self.popup2.dismiss()
			except:
				pass
			try:
				Clock.unschedule(self.planupdate)
				self.popbox.clear_widgets()
				self.poptop.clear_widgets()
				#self.box.clear_widgets()
				self.popup1.dismiss()
			except:
				pass
		if self.fontheight*(len(self.main_headline[self.topic])/self.line_len) > self.fontheight :
			self.txt_height=0*self.fontheight+self.fontheight*(len(self.main_headline[topic])/self.line_len)
		else:
			self.txt_height=self.fontheight		
		
		self.popbox.spacing = .75*self.txt_height
		main_box.height = 2*self.main_height
		main_txt = Label(align="left", valign="middle", size_hint_y=None, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))#, font_size=self.fontheight)
		main_txt.bind(width=lambda s, w:
			   s.setter('text_size')(s, (self.width, None)))
		main_txt.bind(height=main_txt.setter('texture_size[1]'))
		main_txt.bind(height=main_txt.setter('self.minimum_height'))
		main_txt.text=str("%s"%self.main_headline[self.topic])
		
		main_box.add_widget(main_txt)
		main_box.height += main_txt.height

		if self.topic == "settings":
			smallbar1=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			chk1=CheckBox()
			try:
				if temp_set_cpy['tts'] == "True":
					chk1.active=True
				else:
					chk1.active=False
			except:
				chk1.active=True
				temp_set_cpy['tts'] = "True"
				setting_things.put("tts", tts="True")
			chk1.bind(active=self.act_tts)
			#chk1.bind(passive=self.act_tts)
			smallbar1.add_widget(chk1)
			smallbar1.add_widget(Label(text="text2voice"))
			main_box.add_widget(smallbar1)

			smallbar2=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))			
			chk2=CheckBox()
			try:
				if temp_set_cpy['vibr'] == "True":
					chk2.active=True
				else:
					chk2.active=False
			except:
				chk2.active=True
				temp_set_cpy['vibr'] = "True"
				setting_things.put("vibr", vibr="True")
			chk2.bind(active=self.act_vibr)
			#chk2.bind(passive=self.act_vibr)
			smallbar2.add_widget(chk2)
			smallbar2.add_widget(Label(text="vibration"))
			main_box.add_widget(smallbar2)
			
			smallbar3=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.3, self.txt_height * 0.3))
			name_bttn=Button(text="Change name", size_hint_y=None, size_hint_x=None, size=(.31*self.ids.megabox.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.3, self.txt_height * 0.3))
			try:
				name_inpt = TextInput(text=temp_set_cpy['setname'], multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.3, self.txt_height * 0.3))
			except:
				name_inpt = TextInput(text="", multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.3, self.txt_height * 0.3))
			name_bttn.bind(on_release=partial(self.chng_setname, name_inpt))
###
			smallbar3.add_widget(name_inpt)
			smallbar3.add_widget(name_bttn)
			main_box.add_widget(smallbar3)


		if self.topic == "mindf":
			if self.going == True:
				if temp_set_cpy['vibr'] == "True":
					try:
						vibrator.vibrate(0.125)
						#vibrator.cancel()
					except:
						pass
				if temp_set_cpy['tts'] == "True":
					#print "tts: " + temp_set_cpy['tts']
				#if self.act_ttsvar == True:	
					try:
						tts.speak(self.parts[self.mindf_part])
					except:
					#except NotImplementedError:
						#popup = ErrorPopup()
						#popup.open()
						pass

				self.going=False
			
			main_txt.text=self.parts[self.mindf_part]
			mindf_bar=ProgressBar(
				max=self.mindf_limit
				)
			mindf_bar.value=self.mindf_time
			main_box.add_widget(mindf_bar)
			main_box.height += mindf_bar.height
			if self.mindf_time >= self.mindf_limit and self.mindf_part <= len(self.parts)-1:
				self.mindf_part+=1
				self.mindf_time = 0
				self.going=True
			elif self.mindf_part != len(self.parts)-1:		
				self.mindf_time += self.mindf_speed
				if not (self.mindf_time/self.mindf_speed)%60 :
					self.going=True
			elif self.cycle==True and self.mindf_part == len(self.parts)-1:
					self.mindf_part = 0
			
		if self.topic == "state":

			main_txt.text="title: %s\ncategory:%s %s"%(self.state_claim, str(self.pop_choices[self.topic][0][self.state_claim]),self.pop_unit_name)
			
			edit_box = BoxLayout(orientation="horizontal", size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 2, self.txt_height * 2))
			res_lbl=Button(text="edit", size_hint_y=None, size_hint_x=None, size=(.31*self.ids.megabox.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_lbl.bind(on_release = partial(self.menu, self.state_claim))
			
			edit_box.add_widget(res_lbl)

			main_box.add_widget(edit_box)
			main_box.height += edit_box.height
			
			rubric_box=BoxLayout(orientation="horizontal", size_hint_y=None, size_hint_x=1, spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			obj_btn=Button(text="Objectives", size_hint_y=None, size_hint_x=None, size=(self.ids.megabox.width/4, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2),background_color= (.25, .75, 1.0, 1.0))
			obj_btn.bind(on_release=lambda obj_btn: self.chng_obj())
			mis_btn=Button(text="Missions", size_hint_y=None, size_hint_x=None, size=(self.ids.megabox.width/4, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2),background_color= (.25, .75, 1.0, 1.0))
			mis_btn.bind(on_release=lambda mis_btn: self.chng_mis())
			vis_btn=Button(text="Visions", size_hint_y=None, size_hint_x=None, size=(self.ids.megabox.width/4, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2),background_color= (.25, .75, 1.0, 1.0))
			vis_btn.bind(on_release=lambda vis_btn: self.chng_vis())
			val_btn=Button(text="Value", size_hint_y=None, size_hint_x=None, size=(self.ids.megabox.width/4, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2),background_color= (.25, .75, 1.0, 1.0))
			val_btn.bind(on_release=lambda val_btn: self.chng_val())

			eval("%s_btn"%self.state_topic).background_color= (.75, .25, 0, 1.0)
			temp_list=["obj","mis","vis","val"]
			for temp_word in temp_list:
				rubric_box.add_widget(eval("%s_btn"%temp_word))
			temp_list = None
			main_box.add_widget(rubric_box)

			res_box=GridLayout(cols=1,size_hint_y=None, size_hint_x=1, size=(0.8*self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_box.add_widget(Label(text="name"))
			if self.state_topic=="obj" and self.state_sub_topic=="plan":
				res_inpt = TextInput(text=("%s " % temp_set_cpy['setname']),multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			elif self.state_topic=="val" and self.state_sub_topic=="plan":
					res_inpt = TextInput(text=("I care about "),multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))				
			else:
				res_inpt = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			#res_inpt = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_box.add_widget(res_inpt)
			bttn_box=BoxLayout(orientation="vertical",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_bttn = Button(text="add", size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_bttn.padding = (self.ids.megabox.width * 0.2, main_box.height * 0.2)
			bttn_box.add_widget(res_bttn)

			res_box.height= "%ssp"%str(8*self.txt_height)
			res_bttn.bind(on_release=partial(self.add_nomen, self.state_topic, res_inpt))
			main_box.add_widget(res_box)
			main_box.add_widget(bttn_box)
			
			for preNomen in ["obj","mis","vis","val"]:
				if preNomen == "obj":
					obj_lbl=Label(text="",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
					main_box.add_widget(obj_lbl)
					main_box.height += obj_lbl.height
				if preNomen == "mis":
					mis_lbl=Label(text="",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
					main_box.add_widget(mis_lbl)
					main_box.height += mis_lbl.height
				if preNomen == "vis":
					vis_lbl=Label(text="",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))					
					main_box.add_widget(vis_lbl)
					main_box.height += vis_lbl.height
				if preNomen == "val":
					val_lbl=Label(text="",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))					
					main_box.add_widget(val_lbl)
					main_box.height += val_lbl.height					
				for pop_item in self.pop_choices[self.topic][1]:
					if self.pop_choices[self.topic][1][pop_item]["state"] == self.state_claim:
						if self.pop_choices[self.topic][1][pop_item]["nomen"] == preNomen and self.state_topic==preNomen:
							res_box = BoxLayout(orientation="vertical",size_hint_y=None, size_hint_x=1, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
							res = self.pop_choices[self.topic][1][pop_item]["title"]
							res_lbl=Label(halign="left", valign="middle", text=res, size_hint_y=None, size_hint_x=.75, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
							res_lbl.bind(width=lambda s, w:
								   s.setter('text_size')(s, (.50*self.width, None)))
							res_lbl.bind(height=res_lbl.setter('texture_size[1]'))
							res_lbl.bind(height=res_lbl.setter('self.minimum_height'))
							res_box.add_widget(res_lbl)
							res_box.height += res_lbl.height
							
							res_del=Button(text="del", size_hint_y=None, size_hint_x=None, size=(0.25*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
							res_del.bind(on_release = partial(self.del_func, pop_item))
							res_box.add_widget(res_del)
							res_box.height += res_del.height
							
							if self.state_topic == "obj":
#								res_rev=Button(text="review", size_hint_y=None, size_hint_x=None, size=(0.25*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
#								res_rev.bind(on_release = partial(self.review, pop_item))
#								res_box.add_widget(res_rev)
#								res_box.height += res_rev.height
								
								res_edit=Button(text="edit", size_hint_y=None, size_hint_x=None, size=(0.25*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
								res_edit.bind(on_release = partial(self.edit_post, pop_item))
								res_box.add_widget(res_edit)
								res_box.height += res_edit.height
								#res_del.bind(on_release = partial(self.del_nomen, pop_item))
							main_box.add_widget(res_box)
							main_box.height += res_box.height
				#res_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				#res_inpt = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				#res_bttn = Button(text="add", size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				#res_bttn.bind(on_release=partial(self.add_nomen, preNomen, res_inpt))
				#res_box.add_widget(res_inpt)
				#res_box.add_widget(res_bttn)
				#main_box.add_widget(res_box)
				main_box.height += res_box.height
				main_box.height += 1*self.txt_height

		try:
			data.clear()
		except:
			data=dict()
		#timer_list=[self.main_buttons[self.topic].index(x) for x in self.main_buttons[self.topic].values()]
		for b_nr in range(len(self.main_buttons[self.topic])):
		#for main_button in self.main_buttons[self.topic]:
			main_button = self.main_buttons[self.topic][b_nr]
			if self.fontheight*(len(main_button)/self.line_len) > self.fontheight :
				self.txt_height=0*self.fontheight+self.fontheight*(len(main_button)/self.line_len)
			else:
				self.txt_height=self.fontheight

			bttn = Button(text="%s"%(main_button), size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)), font_name="DejaVuSerif")
			funcy = self.main_funcs[self.topic][b_nr].__name__
			bttn.bind(on_release = partial((eval("self.%s"%(funcy)))))

			if self.topic=="mindf":
				#if self.mindf_part == 0 and b_nr==0:
					#bttn.color=(1,1,1,.5)
				if self.mindf_part == len(self.parts)-1 and b_nr==1:
					bttn.text = "again?"
					#bttn.color=(1,1,1,.5)
				if b_nr==2:
					if self.paused == True:
						bttn.text = ">"
					if self.mindf_part == len(self.parts)-1:
						#bttn.text = "again?"
						bttn.color=(1,1,1,.5)
				if b_nr==3 and self.cycle==False:
					bttn.text = "cycle OFF"
					#bttn.color=(1,1,1,.5)

			main_box.add_widget(bttn)
			main_box.height += bttn.height
			
		#zcroller.clear_widgets()
		zcroller.add_widget(main_box)
		self.ids.megabox.add_widget(zcroller)

		#main_box.height += 1*self.txt_height + Window.keyboard_height
		#main_box.height += 1*self.txt_height + Window.height

	def popping(self):
		
		poplbl=Label(halign="center", valign="top", text = self.pop_rubric, size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		poplbl.bind(width=lambda s, w:
		       s.setter('text_size')(s, (.66*self.width, None)))
		poplbl.bind(height=poplbl.setter('texture_size[1]'))
		poplbl.bind(height=poplbl.setter('self.minimum_height'))
							
		#self.popbox.add_widget(poplbl)
		self.poptop.add_widget(poplbl)
		#self.popbox.height += poplbl.height
		self.poptop.height += poplbl.height
		
		### size_hint_x=1 prevents boxes from squeezing together
		box1 = BoxLayout(orientation='horizontal', size_hint_y=None, width=.8*self.popbox.width, size_hint_x=1, size=(self.popbox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		box2 = BoxLayout(orientation='horizontal', size_hint_y=None, width=.8*self.popbox.width, size_hint_x=1, size=(self.popbox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box_title = TextInput(text=self.pop_title_name, multiline=False, size_hint_x=1, size=(.5*box1.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box_unit = TextInput(text=self.pop_unit_name, multiline=False, size_hint_x=1, size=(.5*box1.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		
		if self.topic=="mindf":
			new_box_unit.input_type='number'
		box1.add_widget(Label(text = self.pop_title, size_hint_y=None, size_hint_x=1, size=(.5*box1.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		box1.add_widget(Label(text = self.pop_unit, size_hint_y=None, size_hint_x=1, size=(.5*box1.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		
		box1.add_widget(Label(text = "", size_hint_y=None, size_hint_x=None, size=("%ssp"%str(10*self.txt_height), "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		new_box_add=Button(text = self.pop_action, size_hint_y=None, size_hint_x=1, size=("%ssp"%str(10*self.txt_height), "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))

		new_box_add.bind(on_release=lambda new_box_add: self.add_new(new_box_title.text, new_box_unit.text))
		
		new_box.add_widget(new_box_title)
#		with new_box_title.canvas.before:
#			BorderImage(
#				size=(new_box_title.width + 100, new_box_title.height + 100),
#				pos=(new_box_title.x - 50, new_box_title.y - 50),
#				border=(10, 10, 10, 10),
#				source='left.png')

		new_box.add_widget(new_box_unit)
		new_box.add_widget(new_box_add)
		#self.popbox.add_widget(box1)
		#self.popbox.add_widget(new_box)
		#self.popbox.add_widget(box2)
		#self.popbox.height += box1.height
		#self.popbox.height += box2.height
			
		self.poptop.add_widget(box1)
		self.poptop.add_widget(new_box)
		self.poptop.add_widget(box2)
		self.poptop.height += box1.height
		self.poptop.height += box2.height
	
		for pop_item in self.pop_choices[self.topic][0]: #Go through stored statements
			popping_box=BoxLayout(size=(1*self.popbox.width, "%ssp"%str(2*self.txt_height)), orientation="horizontal", size_hint_y=None, size_hint_x=1, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))

			if self.fontheight*(len(str(pop_item))/self.line_len) > 3*self.fontheight :
				bttnheight=2*self.fontheight+self.fontheight*(len(str(pop_item))/self.line_len)
			else:
				bttnheight=3*self.fontheight
			popping_box_title = Button(size=("%ssp"%str(10*self.txt_height), "%ssp"%str(2*self.txt_height)), height="%ssp"%str(bttnheight), text=str(pop_item), size_hint_y=None, size_hint_x=None, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			popping_box_title.bind(width=lambda s, w:
				s.setter('text_size')(s, (33*self.width, None)))
			popping_box_title.bind(height=popping_box_title.setter('texture_size[1]'))
			popping_box_title.bind(height=popping_box_title.setter('self.minimum_height'))

			predict = self.pop_funcs[self.topic].__name__
			popping_box_title.bind(on_release = partial(eval("self.%s"%(predict)),pop_item))
		
			if self.fontheight*(len(str("%s %s"%(str(self.pop_choices[self.topic][0][pop_item]),self.pop_unit_name)))/self.line_len) > 3*self.fontheight :
				bttnheight=2*self.fontheight+self.fontheight*(len(str("%s %s"%(str(self.pop_choices[self.topic][0][pop_item]),self.pop_unit_name)))/self.line_len)
			else:
				bttnheight=3*self.fontheight
			popping_box_min = Button(size=("%ssp"%str(10*self.txt_height), "%ssp"%str(2*self.txt_height)), text="%s %s"%(str(self.pop_choices[self.topic][0][pop_item]),self.pop_unit_name), size_hint_y=None, size_hint_x=None, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			popping_box_min.bind(width=lambda s, w:
				s.setter('text_size')(s, (self.width, None)))
			popping_box_min.bind(height=popping_box_min.setter('texture_size[1]'))
			popping_box_min.bind(height=popping_box_min.setter('self.minimum_height'))
			popping_box_min.bind(on_release = partial(eval("self.%s"%(predict)),pop_item))

			popping_box_del=Button(size_hint_y=1, size_hint_x=1, size=("%ssp"%str(5*self.txt_height), "%ssp"%str(2*self.txt_height)), text = '...', font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			
			popping_box_del.bind(on_release = partial(self.menu, pop_item))
			if popping_box_min.height>popping_box_title.height:
				#popping_box.height=self.txt_height * 0.2
				popping_box.height=2*popping_box_min.height
				popping_box_del.height=2*popping_box_min.height
			else:
				popping_box.height=self.txt_height * 0.2
				popping_box.height=2*popping_box_title.height
				popping_box_del.height=2*popping_box_title.height
			#popping_box.minimum_height="2ssp"
			#popping_box.width=self.ids.megabox.width
			popping_box.size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height))
			#popping_box.size = Window.size
			
			popping_box.add_widget(popping_box_title)
			popping_box.add_widget(popping_box_min)
			
			popping_box.add_widget(popping_box_del)
			self.popbox.add_widget(popping_box)
			self.popbox.height += popping_box.height
		self.popup1.open()


	def menu(self, pop_item, *args):
		
		
		try:
			self.popbox.clear_widgets()
			self.poptop.clear_widgets()
		except:
			pass
		try:
			self.main_x_box.clear_widgets()
		except:
			pass			
		try:
			self.popup2.dismiss()
		except:
			pass
		try:
			self.popup1.dismiss()
		except:
			pass			


		self.popup2.title=pop_item

		self.pop_bubble.background_color =(20, 0, 0, .5) 
		self.pop_bubble.border = [50, 50, 50, 10]
		#self.pop_bubble.size = (150, 50)
		self.pop_bubble.arrow_pos= 'top_mid'
		my_bub_lbl=Label(text="Edit %s"%pop_item)
		my_bub_title=TextInput(text="%s"%pop_item, multiline=False, size_hint_x=1, size_hint_y=None, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		my_bub_cat=TextInput(text="%s"%str(self.pop_choices[self.topic][0][pop_item]), multiline=False, size_hint_x=1, size_hint_y=None, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		my_bub_bttn=BubbleButton(text="change", size_hint_x=1, size_hint_y=None, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)))
		my_bub_bttn.bind(on_release=partial(self.chng_edit, pop_item, my_bub_title, my_bub_cat))
		my_bub_btnN=BubbleButton(text="cancel", size_hint_x=1, size_hint_y=None, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)))
		my_bub_btnN.bind(on_release=partial(eval("self.%s"%(self.topic) )))
			
		self.main_x_box.add_widget(my_bub_lbl)
		self.main_x_box.add_widget(my_bub_title)
		self.main_x_box.add_widget(my_bub_cat)
		self.main_x_box.add_widget(my_bub_bttn)
		self.main_x_box.add_widget(my_bub_btnN)


		popping_box_del=Button(halign="left", valign="middle", text="del", size_hint_y=None, size_hint_x=None, font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		popping_box_del.width=.5*self.width
		popping_box_del.bind(on_release = partial(self.del_pop, pop_item))
		popping_box_slct=Button(text = 'select',size_hint_y=None, size_hint_x=None, size=("%ssp"%str(5*self.txt_height), "%ssp"%str(2*self.txt_height)), font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		predict = self.pop_funcs[self.topic].__name__
		popping_box_slct.bind(on_release = partial(eval("self.%s"%(predict)),pop_item))

		self.main_x_box.add_widget(popping_box_slct)
		self.main_x_box.add_widget(popping_box_del)
		#self.main_x_box.height += popping_box.height
		self.popup2.open()
		
	def mindf(self, *args):
		try:
			self.popbox.clear_widgets()
			self.poptop.clear_widgets()
		except:
			pass
		self.topic="mindf"
		self.popup1.title="mindfulness"
		#if self.fontheight*(len(self.main_headline[self.topic])/self.line_len) > self.fontheight :
		#	self.txt_height=0*self.fontheight+self.fontheight*(len(self.main_headline[topic])/self.line_len)
		#else:
		#	self.txt_height=self.fontheight		
		self.pop_rubric = 'For how long time do you want to exercise mindfulness?'
		self.pop_unit= "min"
		self.pop_action = "add"
		self.pop_title = "title"
		self.pop_title_name = ""
		self.pop_unit_name = ""
		self.popping()



	def start_timer(self, pop_item, *args):
		timer_item_value=self.pop_choices[self.topic][0][pop_item]
		#Timer_item is the number of minutes the mindfulness should take.
		self.mindf_limit=200
		try:
			self.popup1.dismiss()
		except:
			pass
		self.mindf_part = 0
		self.mindf_time = 0
		#print int(timer_item_value)
		#300 * int(timer_item_value) [0.2 sec] / len(self.parts)[items] = 200 [points] / 1 [items]
		#(300 * int(timer_item_value)) / (len(self.parts)) = 200[points]/[0.2 sec]
		#(300 * int(timer_item_value))[0.2 sec] / (200*len(self.parts))[points] = 1
		#(200*len(self.parts))[points] / (300 * int(timer_item_value))[0.2 sec] = 1
		self.mindf_speed = (self.mindf_limit * len(self.parts)) / (float(timer_item_value) * 300)
		Clock.unschedule(self.planupdate)		
		Clock.schedule_interval(self.planupdate, 0.2)

	def add_new(self,mindf_title,mindf_time):
		checking=1
		for pop_item in self.pop_choices[self.topic][0]:
			if self.pop_choices[self.topic][0][pop_item] == mindf_title:
				checking = 0
		if checking == 1:
			eval("%s_things"%self.topic).put(str(mindf_title), category=mindf_time, title=mindf_title)
			self.pop_choices[self.topic][0][mindf_title] = mindf_time
		eval("self.%s()"%self.topic)

		
	def chng_edit(self, res, new_res, cat, *args):
		cat=cat.text
		new_res=new_res.text
		times_matched = 0
		length = int(len(think_things_cpy)+1)
		nowlen = 1
		keylist=list(think_things_cpy.keys())


		for key in sorted(keylist):

				title_var = ""
				state_var = ""
				nomen_var = ""
				for j in ["title","state","nomen"] :
					if j == "title" :
						title_var = str(think_things_cpy[key][j])
					if j == "state" :
						state_var = str(think_things_cpy[key][j])
					if j == "nomen" :
						nomen_var = str(think_things_cpy[key][j])
				think_things.delete(key)
				think_things_cpy.pop(key, None)
				think_things.put("%s"%(nowlen), title=title_var, state=state_var, nomen=nomen_var)
				think_things_cpy["%s"%(nowlen)] = {"title":title_var, "state":state_var, "nomen":new_res}
				nowlen+=1

		eval("%s_things"%self.topic).delete(res)
		eval("%s_things_cpy"%self.topic).pop(res, None)
		eval("%s_things"%self.topic).put(str(res), category=cat, title=res)
		self.pop_choices[self.topic][0][res] = cat
		
		eval("self.%s()"%self.topic)
				

	def del_pop(self, pop_item, *args):
		try:
			self.popbox.clear_widgets()
			self.poptop.clear_widgets()
		except:
			pass
		try:
			self.main_x_box.clear_widgets()
		except:
			pass			
		try:
			self.popup2.dismiss()
		except:
			pass
		try:
			self.popup1.dismiss()
		except:
			pass			
		
		self.pop_bubble.background_color =(20, 0, 0, .5) 
		self.pop_bubble.border = [50, 50, 50, 10]
		#self.pop_bubble.size = (150, 50)
		self.pop_bubble.arrow_pos= 'top_mid'
		my_bub_lbl=Label(text="Are you sure you want to delete this item?")
		my_bub_btnY= BubbleButton(text='Yes')
		my_bub_btnN= BubbleButton(text='No')
		#my_bub_btn1.bind(on_release=lambda my_bub_btn1: self.Update(1, self.pop_bubble, my_bub_btn1))
		my_bub_btnY.bind(on_release=lambda my_bub_btnY: self.del_popping(pop_item))
		#my_bub_btnN.bind(on_release=lambda my_bub_btnN: eval("self.%s()"%self.topic))
		my_bub_btnN.bind(on_release=lambda my_bub_btnN: self.del_pop_N())
		#self.pop_bubble.add_widget(my_bub_btnY)
		#self.pop_bubble.add_widget(my_bub_btnN)
		#self.add_widget(self.pop_bubble)
		#self.popbox.add_widget(self.pop_bubble)
		#self.main_x_box.add_widget(my_bub_lbl)
		#self.main_x_box.add_widget(my_bub_btnY)
		#self.main_x_box.add_widget(my_bub_btnN)
		#self.popup2.open()
		self.popbox.add_widget(my_bub_lbl)
		self.popbox.add_widget(my_bub_btnY)
		self.popbox.add_widget(my_bub_btnN)
		self.popup1.open()

			
	def del_popping(self, pop_item, *args):

		try:
			self.popbox.clear_widgets()
			self.poptop.clear_widgets()			
		except:
			pass
		try:
			self.main_x_box.clear_widgets()
		except:
			pass			
		try:
			self.popup2.dismiss()
		except:
			pass
		try:
			self.popup1.dismiss()
		except:
			pass			

		eval("%s_things"%self.topic).delete(str("%s"%pop_item))
		self.pop_choices[self.topic][0].pop(pop_item, None)
		eval("self.%s()"%self.topic)

	main_funcs = {
	'settings': [],
	'start': [],
	#'start': [mindf, state, stati],
	'mindf': [prevb, nxtb, pausing, cycling],
	#'state': [],
	#'stati': '\n\n'
	}		

	pop_funcs = {
	'mindf' : start_timer,
	#'state' : show_claim,
	#'stati' : show_ojbs
	}

class gnomieApp(App):
	#global the_screenmanager
	def build(self):
		#global the_screenmanager
		the_screenmanager = ScreenManager()
		#the_screenmanager.transition = FadeTransition()
		mainscreen = MainScreen(name='mainscreen')
		the_screenmanager.add_widget(mainscreen)
		return the_screenmanager

	def on_pause(self):
		return True

	def on_resume(self):
		the_screenmanager = ScreenManager()
		#the_screenmanager.transition = FadeTransition()
		mainscreen = MainScreen(name='mainscreen')
		the_screenmanager.add_widget(mainscreen)
		return the_screenmanager
		
	def on_start(self):
		the_screenmanager = ScreenManager()
		#the_screenmanager.transition = FadeTransition()
		mainscreen = MainScreen(name='mainscreen')
		the_screenmanager.add_widget(mainscreen)
		return the_screenmanager

	def on_stop(self):
		pass
		
if __name__ == '__main__':
	gnomieApp().run()
