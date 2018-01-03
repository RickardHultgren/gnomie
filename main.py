import kivy
kivy.require('1.7.2') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.storage.jsonstore import JsonStore
#from kivy.uix.gridlayout import GridLayout
#from functools import partial
#from kivy.uix.treeview import TreeView, TreeViewNode
#from kivy.uix.treeview import TreeViewLabel
#from kivy.uix.scrollview import ScrollView

#Declaration of variables:
selected = list()		
topic = str('Visions')		
#the_screenmanager = ScreenManager(transition=FadeTransition())
the_screenmanager = ScreenManager()
endtime = 0  
idata = JsonStore('itemdata.json')
idatacpy = dict(JsonStore('itemdata.json'))
newdict = dict()
for key in idatacpy:
	counting = 0
	subdict = idatacpy[key]
	thekey = str()
	thevalue = str()
	for subkey in subdict:
		if counting == 0:
			thekey = subdict[subkey]
			counting += 1
		elif counting == 1:
			thevalue = subdict[subkey]
			newdict[thevalue] = thekey
			thekey=str()
			thevalue=str()
			counting = 0

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
        on_release: root.chngIscreen()
        #on_release: app.root.current = 'itemscreen'
        text: "Item"
    PlanExe:
    Button:
        size_hint: 1, 0.10
        pos_hint: {'x': 0, 'y': 0}
        text: "Exit"
        on_release: app.root.current = 'startscreen'
<ItemScreen>:
    name: 'itemscreen'
    BoxLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        orientation: 'vertical'
        padding: 50
		BoxLayout:
		    orientation:'horizontal'
            Button:
                id: vis_button
                text:'Visions'
                on_release: root.vises()
            Button:
                id: mis_button
                text:'Missions'
                on_release: root.mises()
            Button:
                id: obj_button
                text:'Objectives'
                on_release: root.objes()
        BoxLayout:
		    id:msspinner
            size_hint:(None, None)
            size:(100, 44)
            pos_hint:{'center_x': .5, 'center_y': .5}		    
        Button:
            text:'Select and deselect to statement'
            on_release:root.slct_item(visspinner.text, root.slctid)
        Button:
            text:'Remove'
            on_release:root.rmv_vis(visspinner.text, root.slctid)
        BoxLayout:
            orientation: 'horizontal'
            TextInput:
                size_hint : 0.75, None
                text:''
                id:visinpt
            Button:
                size_hint : 0.25, None
                text:'Add item'
                on_release:root.add_vis(visspinner.text, visinpt.text)                
        Button:
            text:'Cancel'
            on_release:app.root.current = 'planscreen'    
<MultiSelectOption@ToggleButton>:
    size_hint: 1, None
    height: '48dp'
<PlanExe>:
    size_hint: 1, 0.8
    pos_hint: {'x': 0, 'y': 0.10}
    anchor_x: 'center'
    anchor_y: 'top'
    orientation: 'vertical'
    padding: 50
''')  

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
	global the_screenmanager
	
	def __init__ (self,**kwargs):
		super (PlanScreen, self).__init__(**kwargs)
	def chngIscreen(self):
		global the_screenmanager
		the_screenmanager.current = 'itemscreen'
		
class ItemScreen(Screen):
	global selected
	global the_screenmanager
	global newdict
	global topic
	
	newitems = ListProperty()
	slctid = MultiSelectSpinner(
		id="slctid",
		#now
		#values = newitems
	)

	def __init__(self, **kwargs):
		
		super (ItemScreen, self).__init__(**kwargs)
		self.vises()
		
	def vises(self):
		self.ids.vis_button.background_color= (1.0, 0.0, 0.0, 1.0)
		self.ids.mis_button.background_color= (1.0, 1.0, 1.0, 1.0)
		self.ids.obj_button.background_color= (1.0, 1.0, 1.0, 1.0)
		global topic
		global the_screenmanager
		global newdict
		#super (Items, self).__init__(**kwargs)
		for thename in newdict:
			if str(newdict[thename])==str(topic):
			#if str(newdict[name])==str(self.ids.visspinner.text):
				self.newitems.append(thename)
		self.slctid.values = self.newitems
		#try:
		#	self.ids.msspinner.add_widget(self.slctid)
		#except:
		#	pass

	def mises(self):
		self.ids.mis_button.background_color= (1.0, 0.0, 0.0, 1.0)
		self.ids.vis_button.background_color= (1.0, 1.0, 1.0, 1.0)
		self.ids.obj_button.background_color= (1.0, 1.0, 1.0, 1.0)		
		global topic
		global the_screenmanager
		global newdict
		#super (Items, self).__init__(**kwargs)
		for thename in newdict:
			if str(newdict[thename])==str(topic):
			#if str(newdict[name])==str(self.ids.visspinner.text):
				self.newitems.append(thename)
		self.slctid.values = self.newitems
		#try:
		#	self.ids.msspinner.add_widget(self.slctid)
		#except:
		#	pass

	def objes(self):
		self.ids.obj_button.background_color= (1.0, 0.0, 0.0, 1.0)
		self.ids.mis_button.background_color= (1.0, 1.0, 1.0, 1.0)
		self.ids.vis_button.background_color= (1.0, 1.0, 1.0, 1.0)		
		global topic
		global the_screenmanager
		global newdict
		#super (Items, self).__init__(**kwargs)
		for thename in newdict:
			if str(newdict[thename])==str(topic):
			#if str(newdict[name])==str(self.ids.visspinner.text):
				self.newitems.append(thename)
		self.slctid.values = self.newitems
		#try:
		#	self.ids.msspinner.add_widget(self.slctid)
		#except:
		#	pass

	def slct_item(self,varitemtype,slctid):
		global selected
		del selected[:]
		selected.append(varitemtype)
		selected.extend(slctid.text.split(", "))

		
		#print 'rmv_item %s'%selected
		#the_screenmanager.current = 'visitems'
		the_screenmanager.current = 'planscreen'
		
	def rmv_vis(self,varitemtype,slctid):
		global selected
		global newdict
		del selected[:]
		selected=slctid.text.split(", ")
		for i in selected:
			#now
			idata.delete(str(i))
			for name in newdict:
				#https://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-dictionary#11277439
				if newdict[name]==str(i):
					my_dict.pop(str(i), None)
					#self.newitems.remove(str(i))

		self.ids.msspinner.remove_widget(self.slctid)		
		self.slctid.values = self.newitems
		self.ids.msspinner.add_widget(self.slctid)		
		App.get_running_app().stop()
		GnomieApp().run()
		the_screenmanager.current = 'itemscreen'

	def add_vis(self, varitemtype, theitem):
		global newdict
		global the_screenmanager
		idata.put(str(theitem), itemtype=varitemtype, name=theitem)
		newdict[theitem] = varitemtype

		self.ids.msspinner.remove_widget(self.slctid)		
		self.slctid.values = self.newitems
		self.ids.msspinner.add_widget(self.slctid)		
		App.get_running_app().stop()
		GnomieApp().run()
		the_screenmanager.current = 'itemscreen'

	def Exit(self):
		global the_screenmanager
		
		self.nowpart = 0
		self.nowtime=0						
		the_screenmanager.current = 'planscreen'

	#def select_screen(self, spinner, thetext):
	def select_screen(self):
		self.show(self.ids.visspinner.text)

	#def show(self, name, popup1):
	def show(self, name):
		#global the_screenmanager
		global topic
		if name=='Visions':
			#the_screenmanager.current = 'planscreen'
			topic='Visions'
		if name=='Missions':
			#the_screenmanager.current = 'planscreen'
			#the_screenmanager.current='misitems'
			topic='Missions'
		if name=='Objectives':
			#the_screenmanager.current = 'planscreen'
			#the_screenmanager.current='objitems'			
			topic='Objectives'
			
class MFScreen(Screen):
	global endtime
	global the_screenmanager
	
	def __init__ (self,**kwargs):
		global endtime
		super (MFScreen, self).__init__(**kwargs)
	def two(self):
		global the_screenmanager
		global endtime
		
		endtime=120
		the_screenmanager.current = 'exescreen'

	def four(self):
		global the_screenmanager
		global endtime
		
		endtime=240
		the_screenmanager.current = 'exescreen'

class ExeScreen(Screen):
	pass		

class PlanExe(TabbedPanel):
	
	global the_screenmanager
	global endtime
	global selected
	
	objs = StringProperty('')
	miss = StringProperty('')
	viss = StringProperty('')
	box = BoxLayout(orientation='vertical')
	#inpt=TextInput(text=settingdata.get('email')['address'], multiline=False)

	def __init__ (self,**kwargs):
		global selected
		super (PlanExe, self).__init__(**kwargs)
		self.default_tab_content = self.box
		#for anitem, atype in newdict.find(itemtype=str('Statements')):
		#for idata.put(str(selectedstr), itemtype='Statements', name=selectedstr)
			#self.add_widget(TabbedPanelItem(text="tab1"))
			#TabbedPanelItem:
			#text: 'tab3'
			#RstDocument:
			#text:
				
				#'\\n'.join(("Hello world", "-----------",
				#"You are in the third tab."))

		Clock.schedule_interval(self.planupdate, 0.2)

	def planupdate(self, dt):
		
		global selected
		#print selected
		self.box.clear_widgets()
		if len(selected) > 0:
			if selected[0] == "Objectives":
				self.objs = ', '.join(list(selected[1:]))
			if selected[0] == "Missions":
				self.miss = ', '.join(list(selected[1:]))
			if selected[0] == "Visions":
				self.viss = ', '.join(list(selected[1:]))
		
		self.default_tab_text = "New"
		#self.box = self.boxLayout(orientation='vertical')
		self.box.add_widget(Label(text='if'))
		self.box.add_widget(Label(text=self.objs))
		self.box.add_widget(Label(text='then'))
		self.box.add_widget(Label(text=self.miss))
		self.box.add_widget(Label(text='so that'))
		self.box.add_widget(Label(text=self.viss))
		add_btn = Button(text='Add')


		self.box.add_widget(add_btn)
		self.default_tab_content = self.box


	def add_sm(self):
		global selected
		selectedstr = ', '.join(selected)
		idata.put(str(selectedstr), itemtype='Statements', name=selectedstr)		
		newdict['Statements'] = 'selectedstr'		
			
class MFExe(BoxLayout):
	
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
		global the_screenmanager
		self.limit=endtime
		#https://github.com/kivy/kivy/issues/2801		
		if the_screenmanager.current is 'exescreen':
		#if mngr == "exescreen":
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
		
		self.nowpart = 0
		self.nowtime=0						
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
	global the_screenmanager
	def build(self):
		global the_screenmanager
		#the_screenmanager = ScreenManager()
		startscreen = StartScreen(name='startscreen')
		reviewscreen = ReviewScreen(name='reviewscreen')
		mfscreen = MFScreen(name='mfscreen')
		exescreen = ExeScreen(name='exescreen')
		planscreen = PlanScreen(name='planscreen')
		itemscreen = ItemScreen(name='itemscreen')
		
		the_screenmanager.add_widget(startscreen)
		the_screenmanager.add_widget(reviewscreen)
		the_screenmanager.add_widget(mfscreen)
		the_screenmanager.add_widget(exescreen)
		the_screenmanager.add_widget(planscreen)
		the_screenmanager.add_widget(itemscreen)
		return the_screenmanager
		
if __name__ == '__main__':
	GnomieApp().run()
