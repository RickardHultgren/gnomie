import kivy
#from datetime import datetime, timedelta

kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
#from kivy.uix.gridlayout import GridLayout
#from functools import partial
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
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

from kivy.storage.jsonstore import JsonStore

idata = JsonStore('itemdata.json')

#idata.put('item', Visions='')
#idata.put('Missions', item='')
#idata.put('Objectives', item='')
		#inpt=TextInput(text=settingdata.get('email')['address'], multiline=False)
		#store_btn.bind(on_release=(lambda store_btn: self.change_mail(inpt.text, popup1)))
	#def change_mail(self, theaddress, popup1):
		#the_screenmanager.current = 'planscreen'
		#settingdata.put('email', address=theaddress)

selected = list()		
		
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
                on_release: root.About()
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
            #on_release: root.Plan()
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
    Button:
        size_hint: 1, 0.10
        pos_hint: {'x': 0, 'y': 0.90}
        text: "Item"
        on_release: app.root.current = 'visitems'
    PlanExe:
    Button:
        size_hint: 1, 0.10
        pos_hint: {'x': 0, 'y': 0}
        text: "Exit"
        on_release: root.Exit()
<PlanExe>
    size_hint: 1, 0.8
    pos_hint: {'x': 0, 'y': 0.10}
    anchor_x: 'center'
    anchor_y: 'top'
    orientation: 'vertical'
    padding: 50
    TabbedPanelItem:
        text: 'first tab'
        Label:
            text: 'First tab content area'    
<VisItems>:
    name:'visitems'
    BoxLayout:
        #visspinner:visspinner
        anchor_x: 'center'
        anchor_y: 'top'
        orientation: 'vertical'
        padding: 50
        Spinner:
            id:visspinner
            # default value shown
            text:'Visions'
            # available values
            values:('Visions', 'Missions', 'Objectives')
            # just for positioning in our example
            size_hint:None, None
            size:100, 44
            #pos_hint:'center_x': .5, 'center_y': .5
            
            on_release: root.select_screen()
        
        MultiSelectSpinner:
            id:visslctid
            size_hint:(None, None)
            size:(100, 44)
            pos_hint:{'center_x': .5, 'center_y': .5}
            values : root.newitems
        Button:
            text:'Select and deselect to statement'
            on_release:root.slct_item(visspinner.text, visslctid)
        Button:
            text:'Remove'
            on_release:root.rmv_vis(visspinner.text, visslctid)
        Button:
            text:'Add item'
            on_release:root.add_vis(visspinner.text, visinpt.text)
        TextInput:
            text:''
            id:visinpt
        Button:
            text:'Cancel'
            on_release:app.root.current = 'planscreen'
<MisItems>:
    name:'misitems'
    BoxLayout:
        #misspinner:misspinner
        anchor_x: 'center'
        anchor_y: 'top'
        orientation: 'vertical'
        padding: 50
        Spinner:
            id:misspinner
            # default value shown
            text:'Missions'
            # available values
            values:('Visions', 'Missions', 'Objectives')
            # just for positioning in our example
            size_hint:None, None
            size:100, 44
            #pos_hint:'center_x': .5, 'center_y': .5
            
            on_release: root.select_screen()
            
        MultiSelectSpinner:
            id:misslctid
            size_hint:(None, None)
            size:(100, 44)
            #pos_hint:{'center_x': .5, 'center_y': .5}
            values : root.newitems            
        Button:
            text:'Select and deselect to statement'
            on_release:root.slct_item(misspinner.text, misslctid)
        Button:
            text:'Remove'
            on_release:root.rmv_mis(misspinner.text, misslctid)
        Button:
            text:'Add item'
            on_release:root.add_mis(misspinner.text, misinpt.text)
        TextInput:
            text:''
            id:misinpt
        Button:
            text:'Cancel'
            on_release:app.root.current = 'planscreen'
<ObjItems>:
    name:'objitems'
    BoxLayout:
        #objspinner:objspinner
        anchor_x: 'center'
        anchor_y: 'top'
        orientation: 'vertical'
        padding: 50
        Spinner:
            id:objspinner
            # default value shown
            text:'Objectives'
            # available values
            values:('Visions', 'Missions', 'Objectives')
            # just for positioning in our example
            size_hint:None, None
            size:100, 44
            #pos_hint:'center_x': .5, 'center_y': .5
            
            on_release: root.select_screen()
            
        MultiSelectSpinner:
            id:objslctid
            size_hint:None, None
            size:100, 44
            pos_hint:{'center_x': .5, 'center_y': .5}
            values : root.newitems            
        Button:
            text:'Select and deselect to statement'
            on_release:root.slct_item(objspinner.text, objslctid)
        Button:
            text:'Remove'
            on_release:root.rmv_obj(objspinner.text, objslctid)
        Button:
            text:'Add item'
            on_release:root.add_obj(objspinner.text, objinpt.text)
        TextInput:
            text:''
            id:objinpt
        Button:
            text:'Cancel'
            on_release:app.root.current = 'planscreen'
    
<MultiSelectOption@ToggleButton>:
    size_hint: 1, None
    height: '48dp'
<PlanExe>:
''')
the_screenmanager = ScreenManager()
endtime = 0    

class MultiSelectSpinner(Button):
	"""Widget allowing to select multiple text options."""

	dropdown = ObjectProperty(None)
	"""(internal) DropDown used with MultiSelectSpinner."""

	values = ListProperty([])
	"""Values to choose from."""

	selected_values = ListProperty([])
	"""List of values selected by the user."""

	def __init__(self, **kwargs):
		self.bind(dropdown=self.update_dropdown)
		self.bind(values=self.update_dropdown)
		super(MultiSelectSpinner, self).__init__(**kwargs)
		self.bind(on_release=self.toggle_dropdown)

	def toggle_dropdown(self, *args):
		if self.dropdown.parent:
			self.dropdown.dismiss()
		else:
			self.dropdown.open(self)

	def update_dropdown(self, *args):
		if not self.dropdown:
			self.dropdown = DropDown()
		values = self.values
		if values:
			if self.dropdown.children:
				self.dropdown.clear_widgets()
			for value in values:
				b = Factory.MultiSelectOption(text=value)
				b.bind(state=self.select_value)
				self.dropdown.add_widget(b)

	def select_value(self, instance, value):
		if value == 'down':
			if instance.text not in self.selected_values:
				self.selected_values.append(instance.text)
		else:
			if instance.text in self.selected_values:
				self.selected_values.remove(instance.text)

	def on_selected_values(self, instance, value):
		if value:
			self.text = ', '.join(value)
		else:
			self.text = ''

class PlanScreen(Screen):
	global selected
	#global idata
	global the_screenmanager
	global mngr	
	def __init__ (self,**kwargs):
		super (PlanScreen, self).__init__(**kwargs)
		PlanExe=TabbedPanel(
			size_hint= (1, 0.8),
			pos_hint_x= {'x': 0, 'y': 0.125},
			anchor_x= 'center',
			anchor_y= 'top',
			orientation= 'vertical',
			padding= 50
		)
		self.add_widget(PlanExe)	
		
class VisItems(Screen):
	global selected
	#global idata
	global the_screenmanager
	global mngr

	newitems=ListProperty()

	def __init__(self, **kwargs):
		global selected
		#global idata
		global the_screenmanager
		global mngr

		super (VisItems, self).__init__(**kwargs)
		for anitem, atype in idata.find(itemtype=str(self.ids.visspinner.text)):
			self.newitems.append(anitem)

	def slct_item(self,varitemtype,slctid):
		global selected
		del selected[:]
		selected.append(varitemtype)
		selected.extend(slctid.text.split(", "))
		the_screenmanager.current = 'visitems'
		
	def rmv_vis(self,varitemtype,slctid):
		global selected
		del selected[:]
		selected=slctid.text.split(", ")
		for i in selected:
			idata.delete(str(i))
		the_screenmanager.current = 'visitems'		

	def add_vis(self, varitemtype, theitem):
		idata.put(str(theitem), itemtype=varitemtype, name=theitem)
		the_screenmanager.current = 'visitems'

	def Exit(self):
		global the_screenmanager
		global mngr
		self.nowpart = 0
		self.nowtime=0						
		mngr = 'start'
		the_screenmanager.current = 'planscreen'

	#def select_screen(self, spinner, thetext):
	def select_screen(self):
		self.show(self.ids.visspinner.text)

	#def show(self, name, popup1):
	def show(self, name):
		global the_screenmanager
		if name=='Visions':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current='visitems'
		if name=='Missions':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current='misitems'
		if name=='Objectives':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current='objitems'			
			
class MisItems(Screen):
	global selected
	#global idata
	global the_screenmanager
	global mngr

	newitems=ListProperty()
	def __init__(self, **kwargs):
		global selected
		#global idata
		global the_screenmanager

		global mngr

		super (MisItems, self).__init__(**kwargs)
		for anitem, atype in idata.find(itemtype=str(self.ids.misspinner.text)):
			self.newitems.append(anitem)
		#now
		#https://stackoverflow.com/questions/27809703/kivy-sending-text-from-spinner-to-another-function#27810290				

	def slct_item(self,varitemtype,slctid):
		global selected
		del selected[:]
		selected.append(varitemtype)
		selected.extend(slctid.text.split(", "))
		the_screenmanager.current = 'misitems'
		
	def add_mis(self,varitemtype,slctid):
		global selected
		del selected[:]
		selected=slctid.text.split(", ")
		for i in selected:
			idata.delete(str(i))
		the_screenmanager.current = 'misitems'

	def add_mis(self, varitemtype, theitem):
		idata.put(str(theitem), itemtype=varitemtype, name=theitem)
		the_screenmanager.current = 'misitems'

	def Exit(self):
		global the_screenmanager
		global mngr
		self.nowpart = 0
		self.nowtime=0						
		mngr = 'start'
		the_screenmanager.current = 'planscreen'

	#def select_screen(self, spinner, thetext):
	def select_screen(self):
		self.show(self.ids.misspinner.text)

	#def show(self, name, popup1):
	def show(self, name):
		global the_screenmanager
		if name=='Visions':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current = 'visitems'
		if name=='Missions':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current = 'misitems'
		if name=='Objectives':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current = 'objitems'			
			
class ObjItems(Screen):
	global selected
	#global idata
	global the_screenmanager
	global mngr
	newitems=ListProperty()

	def __init__(self, **kwargs):
		global selected
		#global idata
		global the_screenmanager
		global mngr

		super (ObjItems, self).__init__(**kwargs)
		for anitem, atype in idata.find(itemtype=str(self.ids.objspinner.text)):
			self.newitems.append(anitem)

	def slct_item(self,varitemtype,slctid):
		global selected
		del selected[:]
		selected.append(varitemtype)
		selected.extend(slctid.text.split(", "))
		the_screenmanager.current = 'objitems'
		
	def rmv_obj(self,varitemtype,slctid):
		global selected
		del selected[:]
		selected=slctid.text.split(", ")
		for i in selected:
			idata.delete(str(i))
		the_screenmanager.current = 'objitems'

	def add_obj(self, varitemtype, theitem):
		the_screenmanager.current = 'planscreen'
		idata.put(str(theitem), itemtype=varitemtype, name=theitem)
		the_screenmanager.current = 'objitems'

	def Exit(self):
		global the_screenmanager
		global mngr
		self.nowpart = 0
		self.nowtime=0						
		mngr = 'start'
		the_screenmanager.current = 'planscreen'

	#def select_screen(self, spinner, thetext):
	def select_screen(self):
		self.show(self.ids.objspinner.text)

	#def show(self, name, popup1):
	def show(self, name):
		global the_screenmanager
		if name=='Visions':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current='visitems'
		if name=='Missions':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current='misitems'
		if name=='Objectives':
			the_screenmanager.current = 'planscreen'
			the_screenmanager.current='objitems'			
			
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

class PlanExe(TabbedPanel):
#now:
	global mngr
	global the_screenmanager
	global endtime
	global selected
	objs = str('')
	miss = str('')
	viss = str('')
	#inpt=TextInput(text=settingdata.get('email')['address'], multiline=False)
	def __init__ (self,**kwargs):
		super (PlanExe, self).__init__(**kwargs)
		Clock.schedule_interval(self.update, 0.2)
		
	def update(self, dt):
		global mngr

		if len(selected) > 1:
			if selected[0] == "Objectives":
				self.objs = ', '.join(list(selected[1:]))
			if selected[0] == "Missions":
				self.miss = ', '.join(list(selected[1:]))
			if selected[0] == "Visions":
				self.viss = ', '.join(list(selected[1:]))
		
		self.default_tab_text = "New"
		box = BoxLayout(orientation='vertical')
		self.add_widget(Label(text='if'))
		self.add_widget(Label(text=self.objs))
		self.add_widget(Label(text='then'))
		self.add_widget(Label(text=self.miss))
		self.add_widget(Label(text='so that'))
		self.add_widget(Label(text=self.viss))
		add_btn = Button(text='Add')
		#selected
		#add_btn.bind(on_release=(lambda store_btn: self.add_sm()))
		self.add_widget(add_btn)
		self.default_tab_content = box

	def add_sm(self):
		global selected
		selectedstr = ', '.join(selected)
		idata.put(str(selectedstr), itemtype='Statements', name=selectedstr)		
			
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
	def About(self):
		box = BoxLayout(orientation='vertical')
		popup1 = Popup(title='About', content=box, size_hint=(None, None), size=(400, 400))
		self.add_widget(Label(text='Gnomie is an open source app licensed under\nthe BSD2-license. The founder and principal developer is\nRickard Verner Hultgren'))

		store_btn = Button(text='OK')
		store_btn.bind(on_release=lambda store_btn: popup1.dismiss())
		self.add_widget(store_btn)
		#popup1 = Popup(title='Add goal', content=box, auto_dismiss=True, size_hint=(None, None), size=(400, 400))
		popup1.open()

	def Plan(self):
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
		visitems = VisItems(name='visitems')
		misitems = MisItems(name='misitems')
		objitems = ObjItems(name='objitems')
		
		#if mngr=='start':
		the_screenmanager.add_widget(startscreen)
		the_screenmanager.add_widget(reviewscreen)
		the_screenmanager.add_widget(mfscreen)
		the_screenmanager.add_widget(exescreen)
		the_screenmanager.add_widget(planscreen)
		the_screenmanager.add_widget(visitems)
		the_screenmanager.add_widget(misitems)
		the_screenmanager.add_widget(objitems)
		return the_screenmanager
		
if __name__ == '__main__':
	GnomieApp().run()
