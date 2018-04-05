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
if platform == 'android':
#try:
	from jnius import autoclass

	PythonActivity = autoclass('org.renpy.android.PythonActivity')

	PythonActivity = autoclass('org.renpy.android.PythonActivity')
	Intent = autoclass('android.content.Intent')
	#Calendar = autoclass('java.util.Calendar')
	
	intent = Intent()
	#calendar = Calendar.getInstance()
	
	#calendar.setTimeInMillis(1480103863835)
	#Logger.info(calendar.getTimeInMillis()) //  -1659853285
	#intent.setType("vnd.android.cursor.item/event");
	#intent.putExtra("beginTime", cal.getTimeInMillis());
	#intent.putExtra("allDay", false);
	#intent.putExtra("rrule", "FREQ=DAILY");
	#intent.putExtra("endTime", cal.getTimeInMillis()+60*60*1000);
	intent.putExtra("title", "A Test Event from android app");

	intent.setAction(Intent.ACTION_VIEW)
	PythonActivity.mActivity.startActivity(intent)

	#currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
	#currentActivity.startActivity(intent)

	#cal_intent = autoclass('android.content.Intent')


	#cal_intent.setType("vnd.android.cursor.item/event");
	#cal_intent.putExtra("beginTime", cal.getTimeInMillis());
	#cal_intent.putExtra("allDay", false);
	#cal_intent.putExtra("rrule", "FREQ=DAILY");
	#cal_intent.putExtra("endTime", cal.getTimeInMillis()+60*60*1000);
	#cal_intent.putExtra("title", "A Test Event from android app");
	#cal_intent = Intent(Intent.ACTION_VIEW)
	#PythonActivity.mActivity.startActivity(cal_intent)

#PythonActivity = autoclass('org.renpy.android.PythonActivity')
#Intent = autoclass('android.content.Intent')
#Uri = autoclass('android.net.Uri')
#cal_intent.setType("vnd.android.cursor.item/event");
#cal_intent.putExtra("beginTime", cal.getTimeInMillis());
#cal_intent.putExtra("allDay", false);
#cal_intent.putExtra("rrule", "FREQ=DAILY");
#cal_intent.putExtra("endTime", cal.getTimeInMillis()+60*60*1000);
#cal_intent.putExtra("title", "A Test Event from android app");
#cal_intent = Intent(Intent.ACTION_VIEW)
#PythonActivity.mActivity.startActivity(cal_intent)
	
#	PythonActivity = autoclass('org.renpy.android.PythonActivity') #request the activity instance
#	Intent = autoclass('android.content.Intent') # get the Android Intend class
#	Calendar = autoclass('java.util.Calendar')
#
#	PythonActivity = autoclass('org.renpy.android.PythonActivity')
#	cal_intent = autoclass('android.content.Intent')
#	cal_intent.setType("vnd.android.cursor.item/event");
#	cal_intent.putExtra("beginTime", cal.getTimeInMillis());
#	cal_intent.putExtra("allDay", false);
#	cal_intent.putExtra("rrule", "FREQ=DAILY");
#	cal_intent.putExtra("endTime", cal.getTimeInMillis()+60*60*1000);
#	cal_intent.putExtra("title", "A Test Event from android app");
#	cal_intent = Intent(Intent.ACTION_VIEW)
#	PythonActivity.mActivity.startActivity(cal_intent)
#except:
#	pass

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

mindf_things = JsonStore('mindf_things.json')
state_things = JsonStore('state_things.json')
think_things = JsonStore('think_things.json')
setting_things = JsonStore('settings.json')
temp_timers = dict(JsonStore('mindf_things.json'))
temp_claims = dict(JsonStore('state_things.json'))
temp_think = dict(JsonStore('think_things.json'))
temp_set = dict(JsonStore('settings.json'))
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
                #BorderImage:
                    #pos: self.pos
                    #size: self.size
                    #source: "bg1.png"
                    
            ActionView:
                
                
                ActionPrevious:
                    #title: 'gnomie'
                    #title: ''
                    app_icon: 'gnomie.png'
                    with_previous: False
                    on_release: root.start()
                    #on_press: root.start()
                    #background_normal: ''
                    #background_color: 1, .3, .4, .85
                ActionGroup:
                
					text: "|||"
					#icon: './menu.png'
                
                    font_size:"48sp"
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

        ActionBar:

            height:root.height / 8
            width:root.width
            background_color:0,50,50,.2
            pos_hint: {'top':1}            
            padding: '2ssp'
            canvas:
                Color:
                    rgba: self.background_color
                BorderImage:
                    pos: self.pos
                    size: self.size
                    source: "bg1.png"
                    
            ActionView:
                use_separator: True
                ActionPrevious:
                    #title: 'gnomie'
                    #title: ''
                    app_icon: 'bg1.png'
                    with_previous: False
                    #on_release: root.start()
                    #on_press: root.start()
                    #background_normal: ''
                    #background_color: 1, .3, .4, .85
                ActionButton:
                    on_release: root.mindf()
                    text: ''
                    icon: './brain.png'
                ActionButton:
                    text: ''
                    on_release: root.state()
                    icon:'./goal.png'
                ActionButton:
                    text: ''
                    on_release: root.stati()
                    icon: './stat.png'
                   
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
	'mindf' : ["<<",">>","||"],
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
			smallbar=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
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
			smallbar.add_widget(chk1)
			smallbar.add_widget(Label(text="text2voice"))
			main_box.add_widget(smallbar)

		if self.topic == "mindf":
			if self.going == True:
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
				if self.mindf_part == len(self.parts)-1:
					self.mindf_time = 0
				else:
					self.mindf_part+=1
					self.mindf_time = 0
					self.going=True
			elif self.mindf_part != len(self.parts)-1:		
				self.mindf_time += self.mindf_speed
			
		if self.topic == "state":

			main_txt.text="title: %s\ncategory:%s %s"%(self.state_claim, str(self.pop_choices[self.topic][0][self.state_claim]),self.pop_unit_name)
			
			edit_box = BoxLayout(orientation="horizontal", size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 2, self.txt_height * 2))
			res_lbl=Button(text="edit", size_hint_y=None, size_hint_x=None, size=(.31*self.ids.megabox.width, "%ssp"%str(self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_lbl.bind(on_release = partial(self.menu, self.state_claim))
			
			edit_box.add_widget(res_lbl)

			main_box.add_widget(edit_box)
			main_box.height += edit_box.height
			
			rubric_box=BoxLayout(orientation="horizontal", size_hint_y=None, size_hint_x=1, spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			obj_btn=Button(text="Objectives", size_hint_y=None, size_hint_x=None, size=(0.33*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2),background_color= (.25, .75, 1.0, 1.0))
			obj_btn.bind(on_release=lambda obj_btn: self.chng_obj())
			mis_btn=Button(text="Missions", size_hint_y=None, size_hint_x=None, size=(0.33*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2),background_color= (.25, .75, 1.0, 1.0))
			mis_btn.bind(on_release=lambda mis_btn: self.chng_mis())
			vis_btn=Button(text="Visions", size_hint_y=None, size_hint_x=None, size=(0.33*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2),background_color= (.25, .75, 1.0, 1.0))
			vis_btn.bind(on_release=lambda vis_btn: self.chng_vis())

			eval("%s_btn"%self.state_topic).background_color= (.75, .25, 0, 1.0)
			temp_list=["obj","vis","mis"]
			for temp_word in temp_list:
				rubric_box.add_widget(eval("%s_btn"%temp_word))
			temp_list = None
			main_box.add_widget(rubric_box)

			res_box=GridLayout(cols=2,size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_box.add_widget(Label(text="name"))
			res_inpt = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_box.add_widget(res_inpt)
			bttn_box=BoxLayout(orientation="vertical",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_bttn = Button(text="add", size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
			res_bttn.padding = (self.ids.megabox.width * 0.2, main_box.height * 0.2)
			bttn_box.add_widget(res_bttn)

			if self.state_topic=="obj" and self.state_sub_topic=="plan":
				data_begin = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				data_end = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
				res_box.add_widget(Label(text="begin date, time"))
				res_box.add_widget(data_begin)
				res_box.add_widget(Label(text="end date, time"))
				res_box.add_widget(data_end)
				res_box.height= "%ssp"%str(8*self.txt_height)
				res_bttn.bind(on_release=partial(self.add_nomen, self.state_topic, res_inpt, data_begin, data_end))
			else:
				res_bttn.bind(on_release=partial(self.add_nomen, self.state_topic, res_inpt))
			main_box.add_widget(res_box)
			main_box.add_widget(bttn_box)
			
			for preNomen in ["obj","mis","vis"]:
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
								res_rev=Button(text="review", size_hint_y=None, size_hint_x=None, size=(0.25*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
								res_rev.bind(on_release = partial(self.review, pop_item))
								res_box.add_widget(res_rev)
								res_box.height += res_rev.height
								
								res_edit=Button(text="edit", size_hint_y=None, size_hint_x=None, size=(0.25*self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
								res_edit.bind(on_release = partial(self.edit_post, pop_item))
								res_box.add_widget(res_edit)
								res_box.height += res_edit.height
								#res_del.bind(on_release = partial(self.del_nomen, pop_item))
								try:
									begin_box = BoxLayout(orientation="horizontal",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									beginning = self.pop_choices[self.topic][1][pop_item]["begin"]
									begin_lbl=Label(text="begin: %s"%beginning, size_hint_y=None, size_hint_x=None, size=(0.75*self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									#if self.pop_choices[self.topic][1][pop_item]["begin"] != "add" or self.pop_choices[self.topic][1][pop_item]["begin"] != "" :
									#	begin_box.add_widget(begin_lbl)
									#	main_box.add_widget(begin_box)
								except:
									pass
								try:
									end_box = BoxLayout(orientation="horizontal",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									ending = self.pop_choices[self.topic][1][pop_item]["end"]
									end_lbl=Label(text="end: %s"%ending, size_hint_y=None, size_hint_x=None, size=(0.75*self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									#if self.pop_choices[self.topic][1][pop_item]["end"] != "add" or self.pop_choices[self.topic][1][pop_item]["end"] != "" :
									#	end_box.add_widget(end_lbl)
									#	main_box.add_widget(end_box)
								except:
									pass
								try:
									mood_box = BoxLayout(orientation="horizontal",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									moodning = self.pop_choices[self.topic][1][pop_item]["mood"]
									mood_lbl=Label(text="mood: %s"%moodning, size_hint_y=None, size_hint_x=None, size=(0.75*self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									if self.pop_choices[self.topic][1][pop_item]["mood"] != "":
										mood_box.add_widget(mood_lbl)
										main_box.add_widget(mood_box)
								except:
									pass
								try:
									about_box = BoxLayout(orientation="horizontal",size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									abouting = self.pop_choices[self.topic][1][pop_item]["about"]
									about_lbl=Label(text="about: %s"%abouting, size_hint_y=None, size_hint_x=None, size=(0.75*self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
									if self.pop_choices[self.topic][1][pop_item]["about"] != "":
										about_box.add_widget(about_lbl)
										main_box.add_widget(about_box)
								except:
									pass
							
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

			main_box.add_widget(bttn)
			main_box.height += bttn.height
			
		#zcroller.clear_widgets()
		zcroller.add_widget(main_box)
		self.ids.megabox.add_widget(zcroller)

		#main_box.height += 1*self.txt_height + Window.keyboard_height
		#main_box.height += 1*self.txt_height + Window.height

	def edit_post(self, pop_item, *args):
		res= think_things[pop_item]['title']
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
		my_bub_lbl=Label(text="Edit %s"%res)

		data_end = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_box=GridLayout(cols=2,size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_box.add_widget(Label(text=res))
		res_inpt = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_box.add_widget(res_inpt)
		
		data_begin = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_box.add_widget(Label(text="begin date, time"))
		res_box.add_widget(data_begin)
		res_box.add_widget(Label(text="end date, time"))
		res_box.add_widget(data_end)
		res_box.height= "%ssp"%str(8*self.txt_height)
		
		bttn_box=GridLayout(cols=1,size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_bttn=BubbleButton(text="change")
		res_bttn.bind(on_release=partial(self.edit_nomen, pop_item, res_inpt, data_begin, data_end))

		my_bub_btnN=BubbleButton(text="cancel")
		my_bub_btnN.bind(on_release=lambda my_bub_btnN: self.planupdate())
			
		self.main_x_box.add_widget(my_bub_lbl)
		self.main_x_box.add_widget(res_box)
		#self.main_x_box.add_widget(res_bttn)
		#self.main_x_box.add_widget(my_bub_btnN)
		bttn_box.add_widget(res_bttn)
		bttn_box.add_widget(my_bub_btnN)		
		self.main_x_box.add_widget(bttn_box)
		
		self.popup2.open()

	def edit_nomen(self, pop_item, res, begin, end, *args):
		preNomen=self.state_topic
		res = res.text
		begin2var = begin.text
		end2var = end.text

		try:
			mood2var = think_things[pop_item]['mood']
		except:
			pass
		try:
			about2var = think_things[pop_item]['about']
		except:
			pass
		
		think_things.delete(pop_item)
		think_things_cpy.pop(pop_item, None)
		think_things.put("%s"%pop_item, title=res, state=self.state_claim, nomen=preNomen, begin=begin2var, end=end2var, mood=mood2var, about=about2var)
		think_things_cpy["%s"%pop_item]={"title":res, "state":self.state_claim, "nomen":preNomen, "begin":begin2var, "end":end2var, "mood":mood2var, "about":about2var}
		self.planupdate()
		
	def review(self, pop_item, *args):
		res= think_things[pop_item]['title']
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
		my_bub_lbl=Label(text="Edit %s"%res)

		data_end = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_box=GridLayout(cols=2,size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_box.add_widget(Label(text="%s"%res))
		#res_inpt = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		#res_box.add_widget(res_inpt)
		
		data_mood = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		data_about = TextInput(multiline=False, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_box.add_widget(Label(text="mood"))
		res_box.add_widget(data_mood)
		res_box.add_widget(Label(text="about"))
		res_box.add_widget(data_about)
		res_box.height= "%ssp"%str(8*self.txt_height)
		
		
		

		bttn_box=GridLayout(cols=1,size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(4*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		res_bttn=BubbleButton(text="Save")
		res_bttn.bind(on_release=partial(self.add_review, pop_item, data_mood, data_about))

		my_bub_btnN=BubbleButton(text="cancel")
		my_bub_btnN.bind(on_release=lambda my_bub_btnN: self.planupdate())
			
		bttn_box.add_widget(res_bttn)
		bttn_box.add_widget(my_bub_btnN)
		
		
		
		self.main_x_box.add_widget(my_bub_lbl)
		self.main_x_box.add_widget(res_box)
		self.main_x_box.add_widget(bttn_box)
		
		self.popup2.open()

	def add_review(self, pop_item, mood, about, *args):
		res = think_things[pop_item]['title']
		preNomen=self.state_topic

		try:
			begin2var = think_things[pop_item]['begin']
		except:
			pass
		try:
			end2var = think_things[pop_item]['end']
		except:
			pass			

		mood2var = mood.text
		about2var = about.text
		
		think_things.delete(pop_item)
		think_things_cpy.pop(pop_item, None)
		think_things.put("%s"%pop_item, title=res, state=self.state_claim, nomen=preNomen, begin=begin2var, end=end2var, mood=mood2var, about=about2var)
		think_things_cpy["%s"%pop_item]={"title":res, "state":self.state_claim, "nomen":preNomen, "begin":begin2var, "end":end2var, "mood":mood2var, "about":about2var}
		self.planupdate()

	def chng_obj(self):

		self.state_topic="obj"
		self.planupdate()

	def chng_state_obj(self):

		if self.state_sub_topic=="plan":
			self.state_sub_topic="review"
		else:
			self.state_sub_topic="plan"
		self.planupdate()
		
	def chng_mis(self):

		self.state_topic="mis"
		self.planupdate()
		
	def chng_vis(self):

		self.state_topic="vis"
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
			
	def add_nomen(self, preNomen, res, *args):
		res = res.text
		times_matched = 0
		length = int(len(think_things_cpy)+1)
		
		for h in range(1,length) :
			keylist=list(think_things_cpy.keys())
			#print sorted(keylist)
			for key in sorted(keylist):
				#print "\nh:%s\nkey: %s ; h: %s ; times_matched: %s"%("abc", key, h, times_matched)
				if times_matched < h and int(key) > h:
					title_var = ""
					state_var = ""
					nomen_var = ""
					begin_var = ""
					end_var = ""
					mood_var = ""
					about_var = ""
					for j in ["title","state","nomen","begin","end","mood","about"] :
						if j == "title" :
							title_var = str(think_things_cpy[key][j])
						if j == "state" :
							state_var = str(think_things_cpy[key][j])
						if j == "nomen" :
							nomen_var = str(think_things_cpy[key][j])
						if j == "begin" :
							try:
								begin_var = str(think_things_cpy[key][j])
							except:
								pass
						if j == "end" :
							try:
								end_var = str(think_things_cpy[key][j])
							except:
								pass
						if j == "mood" :
							try:
								mood_var = str(think_things_cpy[key][j])
							except:
								pass
						if j == "about" :
							try:
								about_var = str(think_things_cpy[key][j])
							except:
								pass
					think_things.delete(key)
					think_things_cpy.pop(key, None)
					think_things.put("%s"%(h), title=title_var, state=state_var, nomen=nomen_var, begin=begin_var, end=end_var, mood=mood_var, about=about_var)
					think_things_cpy["%s"%(h)] = {"title":title_var, "state":state_var, "nomen":nomen_var, "begin":begin_var, "end":end_var, "mood":mood_var, "about":about_var}
					times_matched += 1
					#print "REPAIR key: %s ; h: %s ; times_matched: %s"%(key, h, times_matched)
				else:
					times_matched += 1
		maxed=length+1
		
		begin2var=""
		end2var=""
		mood2var=""
		about2var=""
		
		if len(args)>2:
			begin2var=str(args[0].text)
			end2var=str(args[1].text)
	
		think_things.put("%s"%maxed, title=res, state=self.state_claim, nomen=preNomen, begin=begin2var, end=end2var, mood=mood2var, about=about2var)
		think_things_cpy["%s"%maxed]={"title":res, "state":self.state_claim, "nomen":preNomen, "begin":begin2var, "end":end2var}
		self.planupdate()
		index_nr = 0

	def del_func(self, pop_item, *args):
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
		my_bub_btnY=Button(text='Yes')
		my_bub_btnN=Button(text='No')
		##my_bub_btn1.bind(on_release=lambda my_bub_btn1: self.Update(1, self.main_x_box, my_bub_btn1))
		self.main_x_box.add_widget(my_bub_lbl)
		#self.popbox.add_widget(box2)
		my_bub_btnY.bind(on_release=lambda my_bub_btnY: self.del_nomen(pop_item))
		my_bub_btnN.bind(on_release=lambda my_bub_btnN: self.planupdate())
		self.popbox.add_widget(my_bub_btnY)
		self.popbox.add_widget(my_bub_btnN)
		self.popup1.open()

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
		
		box1 = BoxLayout(orientation='horizontal', size_hint_y=None, width=.8*self.ids.megabox.width, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		box2 = BoxLayout(orientation='horizontal', size_hint_y=None, width=.8*self.ids.megabox.width, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(1*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box=BoxLayout(size_hint_y=None, size_hint_x=1, size=(self.ids.megabox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box_title = TextInput(text=self.pop_title_name, multiline=False, size_hint_x=1, size=(.31*self.popbox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		new_box_unit = TextInput(text=self.pop_unit_name, multiline=False, size_hint_x=1, size=(.31*self.popbox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		if self.topic=="mindf":
			new_box_unit.input_type='number'
		box1.add_widget(Label(text = self.pop_title, size_hint_y=None, size_hint_x=None, size=(.31*self.popbox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		box1.add_widget(Label(text = self.pop_unit, size_hint_y=None, size_hint_x=None, size=(.31*self.popbox.width, "%ssp"%str(2*self.txt_height)),font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2)))
		
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
		###three dot menu on select button
		popping_box_slct=Button(text = 'select',size_hint_y=None, size_hint_x=None, size=("%ssp"%str(5*self.txt_height), "%ssp"%str(2*self.txt_height)), font_name="DejaVuSerif",spacing=(self.txt_height * 0.2, self.txt_height * 0.2))
		predict = self.pop_funcs[self.topic].__name__
		popping_box_slct.bind(on_release = partial(eval("self.%s"%(predict)),pop_item))

		self.main_x_box.add_widget(popping_box_slct)
		self.main_x_box.add_widget(popping_box_del)
		#self.main_x_box.height += popping_box.height
		self.popup2.open()


### check similarities in add_nomen
	def chng_edit(self, res, new_res, cat, *args):
		cat=cat.text
		new_res=new_res.text
		times_matched = 0
		length = int(len(think_things_cpy)+1)

		keylist=list(think_things_cpy.keys())


		for key in sorted(keylist):

				title_var = ""
				state_var = ""
				nomen_var = ""
				begin_var = ""
				end_var = ""
				mood_var = ""
				about_var = ""
				for j in ["title","state","nomen","begin","end","mood","about"] :
					if j == "title" :
						title_var = str(think_things_cpy[key][j])
					if j == "state" :
						state_var = str(think_things_cpy[key][j])
					if j == "nomen" :
						nomen_var = str(think_things_cpy[key][j])
					if j == "begin" :
						try:
							begin_var = str(think_things_cpy[key][j])
						except:
							pass
					if j == "end" :
						try:
							end_var = str(think_things_cpy[key][j])
						except:
							pass
					if j == "mood" :
						try:
							mood_var = str(think_things_cpy[key][j])
						except:
							pass
					if j == "about" :
						try:
							about_var = str(think_things_cpy[key][j])
						except:
							pass
					think_things.delete(key)
					think_things_cpy.pop(key, None)
					if begin_var == "" and end_var == "":
						think_things.put("%s"%(key), title=title_var, state=state_var, nomen=new_res)
						think_things_cpy["%s"%(key)] = {"title":title_var, "state":state_var, "nomen":new_res}
					else:
						think_things.put("%s"%(key), title=title_var, state=state_var, nomen=new_res, begin=begin_var, end=end_var)
						think_things_cpy["%s"%(key)] = {"title":title_var, "state":state_var, "nomen":new_res, "begin":begin_var, "end":end_var}
					#think_things.put("%s"%(key), title=title_var, state=state_var, nomen=new_res, begin=begin_var, end=end_var)
					#think_things_cpy["%s"%(key)] = {"title":title_var, "state":state_var, "nomen":new_res, "begin":begin_var, "end":end_var}


		eval("%s_things"%self.topic).delete(res)
		eval("%s_things_cpy"%self.topic).pop(res, None)
		eval("%s_things"%self.topic).put(str(res), category=cat, title=res)
		self.pop_choices[self.topic][0][res] = cat
		
		eval("self.%s()"%self.topic)



		
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
		
	def state(self, *args):
		try:
			self.pop_bubble.clear_widgets()
		except:
			pass		
		try:
			self.popbox.clear_widgets()
			self.poptop.clear_widgets()
		except:
			pass
		try:
			Clock.unschedule(self.planupdate)
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

	def stati(self, *args):
		self.topic="stati"
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
		#print int(timer_item_value)
		#300 * int(timer_item_value) [0.2 sec] / len(self.parts)[items] = 200 [points] / 1 [items]
		#(300 * int(timer_item_value)) / (len(self.parts)) = 200[points]/[0.2 sec]
		#(300 * int(timer_item_value))[0.2 sec] / (200*len(self.parts))[points] = 1
		#(200*len(self.parts))[points] / (300 * int(timer_item_value))[0.2 sec] = 1
		self.mindf_speed = (self.mindf_limit * len(self.parts)) / (float(timer_item_value) * 300)
		Clock.unschedule(self.planupdate)		
		Clock.schedule_interval(self.planupdate, 0.2)

	def show_claim(self, pop_item, *args):
		self.state_claim=pop_item
		self.planupdate()

	main_funcs = {
	'settings': [],
	'start': [],
	#'start': [mindf, state, stati],
	'mindf': [prevb, nxtb, pausing],
	'state': [],
	'stati': '\n\n'}		

	pop_funcs = {
	'mindf' : start_timer,
	'state' : show_claim
	}

class emadrsApp(App):
	#global the_screenmanager
	def build(self):
		#global the_screenmanager
		the_screenmanager = ScreenManager()
		#the_screenmanager.transition = FadeTransition()
		mainscreen = MainScreen(name='mainscreen')
		the_screenmanager.add_widget(mainscreen)
		return the_screenmanager

	def on_pause(self):
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
