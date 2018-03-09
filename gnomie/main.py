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

#https://www.snip2code.com/Snippet/344451/Kivy--Android-keep-screen-on
#https://gist.github.com/kived/4b3c1a78b0104e52b2a1
#try:
#	from jnius import autoclass
#	PythonActivity = autoclass('org.kivy.android.PythonActivity')
#	View = autoclass('android.view.View')
#	Params = autoclass('android.view.WindowManager$LayoutParams')
#	from android.runnable import run_on_ui_thread
#except:
#	pass

#Declaration of global variables:
#mindf_things = JsonStore('app/mindf_things.json')
#state_things = JsonStore('app/state_things.json')
#think_things = JsonStore('app/think_things.json')
#temp_timers = dict(JsonStore('app/mindf_things.json'))
#temp_claims = dict(JsonStore('app/state_things.json'))
#temp_think = dict(JsonStore('app/think_things.json'))
mindf_things = JsonStore('mindf_things.json')
state_things = JsonStore('state_things.json')
think_things = JsonStore('think_things.json')
temp_timers = dict(JsonStore('mindf_things.json'))
temp_claims = dict(JsonStore('state_things.json'))
temp_think = dict(JsonStore('think_things.json'))
mindf_things_cpy = dict()
state_things_cpy = dict()
think_things_cpy = dict()
#mindf_things.put(str(theitem), itemtype=topic, name=theitem)

#the_screenmanager = ScreenManager()

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
    
        row_default_height:root.height / 8
		cols:1
        orientation: 'vertical'
        ActionBar:

            height:root.height / 8
            width:root.width
            background_color:255,0,0,.5
            pos_hint: {'top':1}            
            padding: '2ssp'
            canvas:
                Color:
                    rgba: self.background_color
                BorderImage:
                    pos: self.pos
                    size: self.size
                    source: "gnomie.png"
                    
            ActionView:
                use_separator: True
                ActionPrevious:
                    #title: 'gnomie'
                    #title: ''
                    app_icon: 'gnomie.png'
                    with_previous: False
                    #on_release: root.start()
                    #on_press: root.start()
                    #background_normal: ''
                    #background_color: 1, .3, .4, .85
                ActionGroup:
                    #orientation: 'horizontal'
                    mode: 'spinner'
                    background_normal: './menu.png'
                    background_down: './menu.png'
                    background_disabled_normal: './menu.png'
                    border: 30, 30, 3, 3                    
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

                    
        ScrollView:
            size: self.size
            GridLayout:
                cols:1
                orientation:'vertical'
                height:self.minimum_height
                #height:root.main_height
                #padding: root.width * 0.02, root.height * 0.02
                #spacing: root.width * 0.02, root.height * 0.02            
                size_hint_y: None
                size_hint_x: 1            
                do_scroll_x: False
                do_scroll_y: True
                id: main_box

''')  

paused=True

class MainScreen(Screen):
	#global the_screenmanager
	global paused
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
	'stast' : '\n\n'}
	pop_choices = {
	'settings' : '\n\n',
	'start' : '\n\n',
	'mindf' : [mindf_things_cpy],
	'state' : [state_things_cpy, think_things_cpy],
	'stast' : '\n\n'}
	main_buttons = {
	'settings' : ["exit"],
	'start' : ["mindfulness", "statements", "statistics"],
	'mindf' : ["next","previous","exit"],
	'state' : ["statements","exit"],
	'stast' : '\n\n'}
	topic='start'
	mindf_time=NumericProperty(0)
	mindf_part=0
	mindf_limit=0
	mindf_speed=0
	state_claim=""
	act_ttsvar = False
	box = BoxLayout(orientation='vertical')
	popscroll=ScrollView(size= box.size, bar_pos_x="top")
###now
	poptop=BoxLayout(orientation='horizontal')
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
	popup1 = Popup(content=box, size_hint=(.875, .875))
	box.add_widget(poptop)
	box.add_widget(popscroll)
	
	txt_height = 0
	pop_rubric = ""
	pop_unit = ""
	pop_action = ""
	pop_unit_name = ""
	pop_title_name = ""

	###now
	#main_x_scroll= Bubble(orientation = 'vertical',size_hint=(None, None),size=(600, 100),pos=(200,0))
	delbox = BoxLayout(orientation='vertical')
	main_x_scroll=ScrollView(size= delbox.size, bar_pos_x="top")
	main_x_box=GridLayout(
                cols=1,
                orientation='vertical',
                #height=self.minimum_height,
                #height=root.bigheight,
                padding = (main_x_scroll.width * 0.02, main_x_scroll.height * 0.02),
                spacing = (main_x_scroll.width * 0.02, main_x_scroll.height * 0.02),
                size_hint_y= None,
                size_hint_x= 1,
                do_scroll_x= False,
                do_scroll_y= True
                )
	main_x_scroll.add_widget(main_x_box)
	popup2 = Popup(content=delbox, size_hint=(.875, .875))
	delbox.add_widget(main_x_scroll)

	pop_bubble= Bubble(orientation = 'vertical',size_hint=(None, None),size=(600, 100),pos=(200,0))
	
	parts = ["Relax and breathe calmly","breathe in and out","Feel the muscles of the head and neck","of the the arms","of the chest and abdomen","of the legs","Feel the organs of the pelvis and abdomen","Feel the organs of the chest","Feel the sensations of light","smell","taste","sound","touch","Feel inner state and mood","Try to name the mood you feel","Try to feel all the feelings all at once","End of mindfulness"]
	#parts = ["Breath calm and Relax muscles","Feel muscles and organs","Feel sensations","Feel inner state","Feel inner awareness","End of mindfulness"]
	
	def __init__ (self,**kwargs):
		super (MainScreen, self).__init__(**kwargs)
		self.planupdate()
	
	def planupdate(self,*args):
		#global the_screenmanager
		global paused
		self.main_height=0
		try:
			self.ids.main_box.clear_widgets()
		except:
			pass

		if self.topic != "mindf" :
			paused = True
			try:
				the_screenmanager.on_pause=False
			except:
				pass
			#try:
			#	PythonActivity.mActivity.getWindow().clearFlags(Params.FLAG_KEEP_SCREEN_ON)
			#except:
			#	pass
			try:
				self.main_x_box.clear_widgets()
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
		self.ids.main_box.padding=.25*self.txt_height
		self.ids.main_box.spacing=.25*self.txt_height
		
		self.popbox.spacing = .75*self.txt_height
		self.ids.main_box.height=self.main_height
		main_txt=Label(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))#, font_size=self.fontheight)
		main_txt.bind(width=lambda s, w:
			   s.setter('text_size')(s, (self.width-.1*self.ids.main_box.width, None)))
		main_txt.bind(height=main_txt.setter('texture_size[1]'))
		main_txt.bind(height=main_txt.setter('self.minimum_height'))
		main_txt.text=str("%s"%self.main_headline[self.topic])
		
		self.ids.main_box.add_widget(main_txt)
		self.ids.main_box.height += main_txt.height

		if self.topic == "settings":
			#main_txt.text="settings settings"
			#self.ids.main_box.add_widget(Label(text="Settings:"))
			#if platform == 'android':
			#	if paused==True:
			smallbar=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			chk1=CheckBox()
			chk1.bind(active=self.act_tts)
			#chk1.bind(passive=self.act_tts)
			smallbar.add_widget(chk1)
			smallbar.add_widget(Label(text="text2voice"))
			self.ids.main_box.add_widget(smallbar)

		
		if self.topic == "mindf":
			#if platform == 'android':
			#	if paused==True:
			if paused==True:
					try:
						vibrator.vibrate(0.125)
						#vibrator.cancel()
					except:
						pass
					if self.act_ttsvar == True:	
						try:
							tts.speak(self.parts[self.mindf_part])
						except NotImplementedError:
							popup = ErrorPopup()
							popup.open()									
					paused=False
					try:
						the_screenmanager.on_pause=False
					except:
						pass
				
			#try:
			#	PythonActivity.mActivity.getWindow().addFlags(Params.FLAG_KEEP_SCREEN_ON)
			#except:
			#	pass
			#self.parts = ["Breath calm and Relax muscles","Feel muscles and organs","Feel sensations","Feel inner state","Feel inner awareness","End of mindfulness"]
			main_txt.text=self.parts[self.mindf_part]
			mindf_bar=ProgressBar(
				max=self.mindf_limit
				)
			mindf_bar.value=self.mindf_time
			self.ids.main_box.add_widget(mindf_bar)
			self.ids.main_box.height += mindf_bar.height
			if self.mindf_time >= self.mindf_limit and self.mindf_part <= len(self.parts)-1:
				if self.mindf_part == len(self.parts)-1:
					self.mindf_time = 0
				else:
					self.mindf_part+=1
					self.mindf_time = 0
					paused=True
			elif self.mindf_part != len(self.parts)-1:		
				self.mindf_time += self.mindf_speed

		if self.topic == "state":

			main_txt.text=self.state_claim
			for preNomen in ["obj","mis","vis"]:
				if preNomen == "obj":
					obj_lbl=Label(text="If:",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
					self.ids.main_box.add_widget(obj_lbl)
					self.ids.main_box.height += obj_lbl.height
				if preNomen == "mis":
					mis_lbl=Label(text="Then:",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
					self.ids.main_box.add_widget(mis_lbl)
					self.ids.main_box.height += mis_lbl.height
				if preNomen == "vis":
					vis_lbl=Label(text="So that:",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
					self.ids.main_box.add_widget(vis_lbl)
					self.ids.main_box.height += vis_lbl.height
				for pop_item in self.pop_choices[self.topic][1]:
					if self.pop_choices[self.topic][1][pop_item]["state"] == self.state_claim:
						if self.pop_choices[self.topic][1][pop_item]["nomen"] == preNomen :
							
							res = self.pop_choices[self.topic][1][pop_item]["title"]
							res_box = BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
							
							res_lbl=Label(text=res, size_hint_y=None, size_hint_x=None, size=(0.75*self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
							res_box.add_widget(res_lbl)
							res_box.height += res_lbl.height
							res_del=Button(text="del", size_hint_y=None, size_hint_x=None, size=(0.25*self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
							
							res_del.bind(on_release = partial(self.del_func, pop_item))
							#res_del.bind(on_release = partial(self.del_nomen, pop_item))
							res_box.add_widget(res_del)
							res_box.height += res_del.height
							
							self.ids.main_box.add_widget(res_box)
							self.ids.main_box.height += res_box.height
				res_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				res_inpt = TextInput(multiline=False, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				res_bttn = Button(text="add", size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				res_bttn.bind(on_release=partial(self.add_nomen, preNomen, res_inpt))
				res_box.add_widget(res_inpt)
				res_box.add_widget(res_bttn)
				self.ids.main_box.add_widget(res_box)
				self.ids.main_box.height += res_box.height
				self.ids.main_box.height += 1*self.txt_height

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

			bttn = Button(text="%s"%(main_button), size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)), font_name="DejaVuSerif")
			funcy = self.main_funcs[self.topic][b_nr].__name__
			bttn.bind(on_release = partial((eval("self.%s"%(funcy)))))
			self.ids.main_box.add_widget(bttn)
			self.ids.main_box.height += bttn.height
		#self.ids.main_box.height += 1*self.txt_height + Window.keyboard_height
		#self.ids.main_box.height += 1*self.txt_height + Window.height

	def act_tts(self, checkbox, value):
		if value:
			self.act_ttsvar = True
		else:
			self.act_ttsvar = False

	def add_nomen(self, preNomen, res, *args):
		res = res.text
		times_matched = 0
		length = int(len(think_things_cpy)+1)
		#fixed length:
		for h in range(1,length) :
			keylist=list(think_things_cpy.keys())
			print sorted(keylist)
			for key in sorted(keylist):
				#print "key: %s ; h: %s ; times_matched: %s"%(key, h, times_matched)
				if int(key) == h:
					times_matched += 1
					#break
				elif times_matched < h and int(key) > h:
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
					#print "key to delete: %s" % key
					think_things.delete(key)
					think_things_cpy.pop(key, None)
					#times_matched += 1
					think_things.put("%s"%(h), title=title_var, state=state_var, nomen=nomen_var)
					think_things_cpy["%s"%(h)] = {"title":title_var, "state":state_var, "nomen":nomen_var}
					#think_things.put("%s"%(times_matched), title=title_var, state=state_var, nomen=nomen_var)
					#think_things["%s"%(times_matched)] = {"title":title_var, "state":state_var, "nomen":nomen_var}
					times_matched += 1

					
					#print "REPAIR key: %s ; h: %s ; times_matched: %s"%(key, h, times_matched)
					
					#break
					#continue
		maxed=0
		maxing = []
		for n in think_things_cpy:
			maxing.append(int(n))
		try:
			maxed = max(maxing)+1
		except:
			pass
		think_things.put("%s"%maxed, title=res, state=self.state_claim, nomen=preNomen)
		think_things_cpy["%s"%maxed]={"title":res, "state":self.state_claim, "nomen":preNomen}
		self.planupdate()
		index_nr = 0




	def del_func(self, pop_item, *args):
		###now
		#Are you sure you want to delete this item?:
		#bubble or popup?

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
		self.popup2.title="delete?"
		my_bub_lbl=Label(text="Are you sure you want to delete this item?")
		my_bub_btnY=Button(text='Yes')
		my_bub_btnN=Button(text='No')
		##my_bub_btn1.bind(on_release=lambda my_bub_btn1: self.Update(1, self.main_x_box, my_bub_btn1))
		###now
		self.main_x_box.add_widget(my_bub_lbl)
		#self.popbox.add_widget(box2)
		my_bub_btnY.bind(on_release=lambda my_bub_btnY: self.del_nomen(pop_item))
		my_bub_btnN.bind(on_release=lambda my_bub_btnN: self.planupdate())
		self.main_x_box.add_widget(my_bub_btnY)
		self.main_x_box.add_widget(my_bub_btnN)
		self.popup2.open()

	def del_nomen(self, pop_item, *args):
		if self.topic=='state':
			think_things.delete(str("%s"%pop_item))
		self.pop_choices[self.topic][1].pop(pop_item, None)
		self.planupdate()
				
	def prevb(self, *args):
		if self.mindf_part != 0:
			self.mindf_part -= 1
		self.mindf_time = 0

	def nxtb(self, *args):
		if self.mindf_part != 5:
			self.mindf_part += 1
		self.mindf_time = 0
			
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
		self.popup1.title="about"
		about_txt=Label(text = 'Gnomie is an open source app licensed under\nthe BSD2-license. The founder and principal developer is\nRickard Verner Hultgren',size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(3*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		self.popbox.add_widget(about_txt)
		self.popbox.height += about_txt.height
		
		exit_bttn=Button(text="OK",size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		exit_bttn.bind(on_release=lambda prv_bttn: self.popup1.dismiss())
		self.popbox.add_widget(exit_bttn)			
		self.popbox.height += exit_bttn.height

		self.popup1.open()

	def settings(self):
		self.topic="settings"
		self.planupdate()
	
	def popping(self):
		poplbl=Label(text = self.pop_rubric, size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		#self.popbox.add_widget(poplbl)
		self.poptop.add_widget(poplbl)
		#self.popbox.height += poplbl.height
		self.poptop.height += poplbl.height
		box1 = BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		box2 = BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box_title = TextInput(text=self.pop_title_name, multiline=False, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box_unit = TextInput(text=self.pop_unit_name, multiline=False, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		box1.add_widget(Label(text = self.pop_title, size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		box1.add_widget(Label(text = self.pop_unit, size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		
		box1.add_widget(Label(text = "", size_hint_y=None, size_hint_x=None, size=("%ssp"%str(10*self.txt_height), "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		new_box_add=Button(text = self.pop_action, size_hint_y=None, size_hint_x=None, size=("%ssp"%str(10*self.txt_height), "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box_add.bind(on_release=lambda new_box_add: self.add_new(new_box_title.text, new_box_unit.text))
		
		new_box.add_widget(new_box_title)
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
			#pop_item is the key/title of the timer
			popping_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			
			popping_box_title = Label(text=str(pop_item), size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			popping_box_min = Label(text="%s %s"%(str(self.pop_choices[self.topic][0][pop_item]),self.pop_unit_name), size_hint_y=None, size_hint_x=1, size=(self.ids.main_box.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			popping_box_del=Button(text = 'del',size_hint_y=None, size_hint_x=None, size=("%ssp"%str(5*self.txt_height), "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			
			popping_box_del.bind(on_release = partial(self.del_pop, pop_item))
			popping_box_slct=Button(text = 'select',size_hint_y=None, size_hint_x=None, size=("%ssp"%str(5*self.txt_height), "%ssp"%str(2*self.txt_height)), font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			predict = self.pop_funcs[self.topic].__name__
			popping_box_slct.bind(on_release = partial(eval("self.%s"%(predict)),pop_item))
			
			popping_box.add_widget(popping_box_title)
			popping_box.add_widget(popping_box_min)
			popping_box.add_widget(popping_box_del)
			popping_box.add_widget(popping_box_slct)
			self.popbox.add_widget(popping_box)
			self.popbox.height += popping_box.height
		self.popup1.open()

		
	def mindf(self, *args):
		try:
			self.popbox.clear_widgets()
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
		
	def state(self, *args):
		try:
			self.pop_bubble.clear_widgets()
		except:
			pass		
		try:
			self.popbox.clear_widgets()
		except:
			pass
		self.topic = "state"
		self.popup1.title = "claims"
		#if self.fontheight*(len(self.main_headline[self.topic])/self.line_len) > self.fontheight :
		#	self.txt_height=0*self.fontheight+self.fontheight*(len(self.main_headline[topic])/self.line_len)
		#else:
		#	self.txt_height=self.fontheight		
		self.pop_rubric = 'Claims'
		self.pop_unit = "category"
		self.pop_action = "add"
		self.pop_title = "title"
		self.pop_title_name = ""
		self.pop_unit_name = ""
		self.popping()

	def stast(self, *args):
		self.topic="stast"
		pass

	def add_claim(self,state_obj_inpt, state_mis_inpt, state_vis_inpt):
		pass
		
	def add_new(self,mindf_title,mindf_time):
		checking=1
		for pop_item in self.pop_choices[self.topic][0]:
			if self.pop_choices[self.topic][0][pop_item] == mindf_title:
				checking = 0
		if checking == 1:
			eval("%s_things"%self.topic).put(str(mindf_title), category=mindf_time, title=mindf_title)
			self.pop_choices[self.topic][0][mindf_title] = mindf_time
		eval("self.%s()"%self.topic)
				
	def del_popping(self, pop_item, *args):

		try:
			self.popbox.clear_widgets()
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

	def del_pop(self, pop_item, *args):
		###now
		#Are you sure you want to delete this item?:
		#bubble or popup?

		try:
			self.popbox.clear_widgets()
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
		self.main_x_box.add_widget(my_bub_lbl)
		self.main_x_box.add_widget(my_bub_btnY)
		self.main_x_box.add_widget(my_bub_btnN)
		self.popup2.open()

	def del_pop_N(self):
		self.popup2.dismiss()
		eval("self.%s()"%self.topic)
		#self.popup1.open()


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
		print int(timer_item_value)
		#300 * int(timer_item_value) [0.2 sec] / len(self.parts)[items] = 200 [points] / 1 [items]
		#(300 * int(timer_item_value)) / (len(self.parts)) = 200[points]/[0.2 sec]
		#(300 * int(timer_item_value))[0.2 sec] / (200*len(self.parts))[points] = 1
		#(200*len(self.parts))[points] / (300 * int(timer_item_value))[0.2 sec] = 1
		self.mindf_speed = (self.mindf_limit * len(self.parts)) / (int(timer_item_value) * 300)
		Clock.unschedule(self.planupdate)		
		Clock.schedule_interval(self.planupdate, 0.2)

	def show_claim(self, pop_item, *args):
		self.state_claim=pop_item
		self.planupdate()

	main_funcs = {
	'settings': [exitb],
	'start': [mindf, state, stast],
	'mindf': [nxtb, prevb, exitb],
	'state': [state, exitb],
	'stast': '\n\n'}		

	pop_funcs = {
	'mindf' : start_timer,
	'state' : show_claim
	}

class emadrsApp(App):
	global paused
	#global the_screenmanager
	def build(self):
		#global the_screenmanager
		the_screenmanager = ScreenManager()
		#the_screenmanager.transition = FadeTransition()
		mainscreen = MainScreen(name='mainscreen')
		the_screenmanager.add_widget(mainscreen)
		return the_screenmanager

	def on_pause(self):
		global paused
		if paused == True:
			# Here you can save data if needed
			return True
		else:
			return False

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
		
if __name__ == '__main__':
	emadrsApp().run()
