
'''
import necesarry libraries from pygame and external modules Widgets and utilitFunctions
'''
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import Widgets as Wid
import utilityFunctions as util
from Control.__init__ import *
from Data.functions import *
#from TaskOverflow.Data.__init__ import*

#import get_input

'''define constant value for windows size
	and background color
'''
WIN_SIZE_X=700
WIN_SIZE_Y=600
BACGROUND_COLOR=(33, 140, 141)

class mainUI():

	def __init__(self):

		pygame.init()
		self.AppDisplay=pygame.display.set_mode((WIN_SIZE_X,WIN_SIZE_Y)) 	
		self.myMouse=pygame.mouse 
		self.myMouse.set_cursor(*pygame.cursors. arrow)	

		#initialize primary widgets
		self.taskPaneHeader=Wid.TaskPaneHeader((100,50),(71, 62, 63),(500,50),"Time")
		self.taskPane=Wid.TaskPane((100,50),(239, 113, 38),(500,500))
		self.addButton=Wid.Button2("UI/res/icons/addButton.png",(625,50),(50,50))
		self.clearButton=Wid.Button2("UI/res/icons/clearButton.png",(625,110),(50,50))
		self.UnfixedWidget=[]

		#add Allocation instance
		self.TaskAllocator = Scheduler()

		self.AllocationSpaceUI=[]

		self.TB=self.TaskAllocator.CS.sched
		self.positionreferencecounter=0
		while self.TB!=None:
			self.AllocationSpaceUI.append(Wid.TimeBlockUI((205,105+(49*self.positionreferencecounter)),(255,222,0),(390,50),self.TB))
			self.positionreferencecounter+=1
			self.TB=self.TB.next

		self.positionreferencecounter=0
		#States
		AppExit=False
		self.addTask=False
		self.getTask=False
		self.getDuration=False

		self.blinkSwitch=0		
		self.clearTask=False

		#counter-> this variables is for getting input
		self.getdurationcounter=0
		self.getmustartcounter=0
		self.getlowerboundcounter=0
		self.getupperboundcounter=0
		self.getprioritycounter=2

		#this variable determines what input is being done
		self.addState=None

		clock=pygame.time.Clock()

		while not AppExit:
			for event in pygame.event.get():
				if event.type==pygame.QUIT: 
					self.TaskAllocator.saveSched()		# Save before exiting
					#exit when exit button si clicked						
					AppExit=True
				elif event.type==pygame.MOUSEMOTION:
					#change mouse pointer when over a addButton
					#if util.isMouseover(self.myMouse.get_pos(),self.addButton): 
					#	self.myMouse.set_cursor(*pygame.cursors.broken_x)	
					#if not util.isMouseover(self.myMouse.get_pos(),self.addButton): 
					#	self.myMouse.set_cursor(*pygame.cursors.arrow)
					pass

				elif event.type==pygame.MOUSEBUTTONDOWN:
					if self.myMouse.get_pressed()==(1,0,0):
						self.ClickAddButton()	#check if addBUtton is clicked, display addTaskUI if such event happens
						self.ClickClearButton()	#check if ClearButton is Cliked, display a query message if user wants to delete all tasks
						if self.addTask==True:
							self.getTask=self.ClickGetTask()	#respomsibe for getting the title
							self.ClickGetType() 				#reponsible for getting the type

							if self.ClickGetTime(self.UnfixedWidget[-1].durationbuttonhh,self.UnfixedWidget[-1].durationbuttonmm)==True:
								self.addState=1					#update addState to 1->getting duration
							elif self.UnfixedWidget[-1].fixrbut.type=="fix":
								if self.ClickGetTime(self.UnfixedWidget[-1].mustarthh,self.UnfixedWidget[-1].mustartmm)==True:
									self.addState=2				#update 
							elif self.UnfixedWidget[-1].fixrbut.type=="flexible":
								if self.ClickGetTime(self.UnfixedWidget[-1].lowerboundhh,self.UnfixedWidget[-1].lowerboundmm)==True:
									self.addState=3
								elif self.ClickGetTime(self.UnfixedWidget[-1].upperboundhh,self.UnfixedWidget[-1].upperboundmm)==True:
									self.addState=4	
								elif self.clickGetPriority():
									print "getting priority"
									self.addState=5
								self.clickGetPartition()
								#if self.ClickGetTime(self.UnfixedWidget[-1].lowerboundhh,self.UnfixedWidget[-1].lowerboundmm)==True:
								#	self.addState=3							
								#if self.ClickGetTime(self.UnfixedWidget[-1].lowerboundhh,self.UnfixedWidget[-1].lowerboundmm)==True:
								#	self.addState=3							
							else:
								self.addState=None

							self.cancelAdd()
							self.confirmAdd()

						if self.clearTask==True:
							self.confirmedClear()
							self.cancelClear()

						if self.addTask==False or self.clearTask==False:
							for i in self.AllocationSpaceUI:
								if util.isMouseover(self.myMouse.get_pos(),i):
									if i.status!=None:
										print i.status.tid,"is pressed"


					elif event.button == 4:  #scrolls up the timetable
						print "scrolling upp"
						self.positionreferencecounter+=.5

				elif event.type==pygame.MOUSEBUTTONUP: #scrolls down the timetable
					if event.button == 5:
						print "scrolling down"	
						self.positionreferencecounter-=.5


				#display the taskUI if addTask is True
				if self.addTask==True:
					if self.getTask==True:
						self.GetTaskTitle(event)

					elif self.addState==1:
						self.UnfixedWidget,self.getdurationcounter=util.getinputothers(self.UnfixedWidget,self.getdurationcounter,event,self.UnfixedWidget[-1].isgetDuration)
					if self.addState==2:
						self.UnfixedWidget,self.getmustartcounter=util.getinputothers(self.UnfixedWidget,self.getmustartcounter,event,self.UnfixedWidget[-1].isgetmustart)
					if self.addState==3:
						self.UnfixedWidget,self.getlowerboundcounter=util.getinputothers(self.UnfixedWidget,self.getlowerboundcounter,event,self.UnfixedWidget[-1].isgetlowerbound)
					if self.addState==4:
						self.UnfixedWidget,self.getupperboundcounter=util.getinputothers(self.UnfixedWidget,self.getupperboundcounter,event,self.UnfixedWidget[-1].isgetupperbound)
					if self.addState==5:
						self.UnfixedWidget,self.getprioritycounter=util.getpriority(self.UnfixedWidget,self.getprioritycounter,event,self.UnfixedWidget[-1].isgetpriority)
						#self.UnfixedWidget,self.getupperboundcounter=util.getinputothers(self.UnfixedWidget,self.getupperboundcounter,event,self.UnfixedWidget[-1].isgetupperbound)
					#elif self.UnfixedWidget[-1].fixrbut.type=="flexible":

					#	self.UnfixedWidget,self.getlowerboundcounter=util.getinputothers(self.UnfixedWidget,self.getlowerboundcounter,event,self.UnfixedWidget[-1].isgetlowerbound)
					#	self.UnfixedWidget,self.getupperboundcounter=util.getinputothers(self.UnfixedWidget,self.getupperboundcounter,event,self.UnfixedWidget[-1].isgetupperbound)
					#	self.UnfixedWidget,self.getprioritycounter=util.getinputothers(self.UnfixedWidget,self.getprioritycounter,event,self.UnfixedWidget[-1].isgetpriority)


			#for i in self.AllocationSpaceUI:
			#	i.position=(i.position[0],i.position[1]+1)
			#	print i.position
			#self.positionreferencecounter+=0.01

			if(len(self.AllocationSpaceUI))>9:
				keys=pygame.key.get_pressed()
				if keys[pygame.K_PAGEUP]:
					self.positionreferencecounter+=.5
				elif keys[pygame.K_PAGEDOWN]:
					self.positionreferencecounter-=.5

				if self.positionreferencecounter<9-len(self.AllocationSpaceUI):
					self.positionreferencecounter=9-len(self.AllocationSpaceUI)
				elif self.positionreferencecounter>0:
					self.positionreferencecounter=0



			self.drawUI(self.positionreferencecounter)

			pygame.display.update()	
			clock.tick(300)
		pygame.quit()
		quit()

	def ClickAddButton(self):
		if self.addTask==False and self.clearTask==False:
			if util.isMouseover(self.myMouse.get_pos(),self.addButton):	
				self.addButton=Wid.Button2("UI/res/icons/addButtonClicked.png",(625,50),(50,50))		
				myAddTaskUI=Wid.AddTaskUI((WIN_SIZE_X/2-225,WIN_SIZE_Y/2-175),(450,350),(108,206,203))
				self.UnfixedWidget.append(myAddTaskUI)	
				self.addTask=True
				#reinitialize all addTask states to False
		elif self.addTask==True:
			if util.isMouseover(self.myMouse.get_pos(),self.addButton):	
				self.addButton=Wid.Button2("UI/res/icons/addButton.png",(625,50),(50,50))		
				self.UnfixedWidget.remove(self.UnfixedWidget[-1])
				self.addTask=False
				#reinitialize all addTask states to False
	def ClickClearButton(self):
		if self.clearTask==False and self.addTask==False:
			if util.isMouseover(self.myMouse.get_pos(),self.clearButton):	
				self.clearButton=Wid.Button2("UI/res/icons/clearButtonClicked.png",(625,110),(50,50))		
				self.clearTask=True
				myMessageUI=Wid.MessageDialog((WIN_SIZE_X/2-150,WIN_SIZE_Y/2-175),(108,206,203),(300,150),"Would you like to Clear all Task?")
				self.UnfixedWidget.append(myMessageUI)
		elif self.clearTask==True:
			if util.isMouseover(self.myMouse.get_pos(),self.clearButton):	
				self.clearButton=Wid.Button2("UI/res/icons/clearButton.png",(625,110),(50,50))		
				self.UnfixedWidget.remove(self.UnfixedWidget[-1])
				self.clearTask=False
				

	def ClickGetTask(self):
		if util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].input):
			return True
		if not util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].input):
			return False
	def ClickGetType(self):
		if self.UnfixedWidget[-1].fixrbut.gettasktype(self.myMouse.get_pos())=="fix":
			self.UnfixedWidget[-1].fixrbut.type="fix"
			self.UnfixedWidget[-1].lowerboundhh.text="0 0"
			self.UnfixedWidget[-1].lowerboundmm.text="0 0"
			self.UnfixedWidget[-1].upperboundhh.text="0 0"
			self.UnfixedWidget[-1].upperboundmm.text="0 0"
			self.UnfixedWidget[-1].lowerboundhh.font_col=(200,200,200)
			self.UnfixedWidget[-1].lowerboundmm.font_col=(200,200,200)
			self.UnfixedWidget[-1].upperboundhh.font_col=(200,200,200)
			self.UnfixedWidget[-1].upperboundmm.font_col=(200,200,200)
			self.UnfixedWidget[-1].priority.font_col=(200,200,200)
			self.UnfixedWidget[-1].lowerboundhh.color=(255,255,255)
			self.UnfixedWidget[-1].lowerboundmm.color=(255,255,255)
			self.UnfixedWidget[-1].upperboundhh.color=(255,255,255)
			self.UnfixedWidget[-1].upperboundmm.color=(255,255,255)
			self.UnfixedWidget[-1].priority.color=(255,255,255)

		if self.UnfixedWidget[-1].fixrbut.gettasktype(self.myMouse.get_pos())=="flexible":
			self.UnfixedWidget[-1].fixrbut.type="flexible"
			self.UnfixedWidget[-1].mustarthh.text="0 0"
			self.UnfixedWidget[-1].mustartmm.text="0 0"	
			self.UnfixedWidget[-1].mustarthh.font_col=(200,200,200)
			self.UnfixedWidget[-1].mustartmm.font_col=(200,200,200)	
			self.UnfixedWidget[-1].mustarthh.color=(255,255,255)
			self.UnfixedWidget[-1].mustartmm.color=(255,255,255)	
	def ClickGetTime(self,buttonhh,buttonmm):

		if util.isMouseover(self.myMouse.get_pos(),buttonhh):			
			buttonhh.highlight((71, 62, 63))
			buttonhh.font_col=(242,242,242)
		elif  not util.isMouseover(self.myMouse.get_pos(),buttonhh): 	
			buttonhh.unhighlight((255,255,255))
			buttonhh.font_col=(0,0,0)
		if util.isMouseover(self.myMouse.get_pos(),buttonmm):
			buttonmm.highlight((71, 62, 63))
			buttonmm.font_col=(242,242,242)
		elif  not util.isMouseover(self.myMouse.get_pos(),buttonmm): 
			buttonmm.unhighlight((255,255,255))
			buttonmm.font_col=(0,0,0)


		if util.isMouseover(self.myMouse.get_pos(),buttonhh):
			if id(buttonhh)==id(self.UnfixedWidget[-1].durationbuttonhh):
				print "getting duration hh"
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetDuration=True
				self.getdurationcounter=0
				return True
		elif util.isMouseover(self.myMouse.get_pos(),buttonmm):
			if id(buttonmm)==id(self.UnfixedWidget[-1].durationbuttonmm):
				print "getting duration mm"
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetDuration=True
				self.getdurationcounter=2
				return True
		if util.isMouseover(self.myMouse.get_pos(),buttonhh):
			if id(buttonhh)==id(self.UnfixedWidget[-1].mustarthh):
				print "getting mustart"
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetmustart=True
				self.getmustartcounter=0
				return True
		elif util.isMouseover(self.myMouse.get_pos(),buttonmm):
			if id(buttonmm)==id(self.UnfixedWidget[-1].mustartmm):
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetmustart=True
				self.getmustartcounter=2
				return True

		if util.isMouseover(self.myMouse.get_pos(),buttonhh):
			if id(buttonhh)==id(self.UnfixedWidget[-1].lowerboundhh):
				print "getting mustart"
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetlowerbound=True
				self.getlowerboundcounter=0
				return True
		elif util.isMouseover(self.myMouse.get_pos(),buttonmm):
			if id(buttonmm)==id(self.UnfixedWidget[-1].lowerboundmm):
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetlowerbound=True
				self.getlowerboundcounter=2
				return True
		if util.isMouseover(self.myMouse.get_pos(),buttonhh):
			if id(buttonhh)==id(self.UnfixedWidget[-1].upperboundhh):
				print "getting mustart"
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetupperbound=True
				self.getupperboundcounter=0
				return True
		elif util.isMouseover(self.myMouse.get_pos(),buttonmm):
			if id(buttonmm)==id(self.UnfixedWidget[-1].upperboundmm):
				self.setAllAddConditionFalse()
				self.UnfixedWidget[-1].isgetupperbound=True
				self.getupperboundcounter=2
				return True
		else:
			return False

	def clickGetPriority(self):
		if util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].priority):			
			self.UnfixedWidget[-1].priority.highlight((71, 62, 63))
			self.UnfixedWidget[-1].priority.font_col=(242,242,242)
		elif  not util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].priority): 	
			self.UnfixedWidget[-1].priority.unhighlight((255,255,255))
			self.UnfixedWidget[-1].priority.font_col=(0,0,0)

		if util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].priority):
			print "getting priority"
			self.setAllAddConditionFalse()
			self.UnfixedWidget[-1].isgetpriority=True
			self.getprioritycounter=0
			return True

	def clickGetPartition(self):
		if self.UnfixedWidget[-1].partition.getpartition(self.myMouse.get_pos()):
			print "getting partition"
			self.setAllAddConditionFalse()
			if self.UnfixedWidget[-1].partition.value==False:
				self.UnfixedWidget[-1].partition.value=True
			elif self.UnfixedWidget[-1].partition.value==True:
				self.UnfixedWidget[-1].partition.value=False

	def setAllAddConditionFalse(self):
		self.UnfixedWidget[-1].isgetDuration=False
		self.UnfixedWidget[-1].isgetmustart=False
		self.UnfixedWidget[-1].isgetlowerbound=False
		self.UnfixedWidget[-1].isgetupperbound=False
		self.UnfixedWidget[-1].isgetpriority=False


	#def updateTime(self,condition)
	def cancelAdd(self):
		#cancel
		if self.addTask==True:
			if util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].cancel):
				print "cancel"
				self.UnfixedWidget=[]
				self.addTask=False
				getTask=False
				self.addButton=Wid.Button2("UI/res/icons/addButton.png",(625,50),(50,50))

	def cancelClear(self):
		if self.clearTask==True:
			if util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].cancel):
				print "cancel"
				self.UnfixedWidget=[]
				self.clearTask=False
				self.clearButton=Wid.Button2("UI/res/icons/clearButton.png",(625,110),(50,50))
	def confirmAdd(self):
		#add
		if self.addTask==True:
			if util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].add):
				print "confirm add"
				# Integration of Add Task
				NT = Task()
				NT=self.extractData(NT)
				self.TaskAllocator.addTask(NT)

				self.UnfixedWidget=[]
				self.addTask=False
				getTask=False			
				self.addButton=Wid.Button2("UI/res/icons/addButton.png",(625,50),(50,50))
				
	def confirmedClear(self):
		if self.clearTask==True:
			if util.isMouseover(self.myMouse.get_pos(),self.UnfixedWidget[-1].clear):
				print "confirm clear"
				# Integration of Clear Task
				self.TaskAllocator.clearSched()
				self.UnfixedWidget=[]
				self.clearTask=False
				self.clearButton=Wid.Button2("UI/res/icons/clearButton.png",(625,110),(50,50))
				

	def extractData(self,NT):
		taskname=self.UnfixedWidget[-1].input.text
		NT.title=taskname[10:]
		NT.duration=int(self.UnfixedWidget[-1].durationbuttonhh.text[0]+self.UnfixedWidget[-1].durationbuttonhh.text[2])*100+int(self.UnfixedWidget[-1].durationbuttonmm.text[0]+self.UnfixedWidget[-1].durationbuttonmm.text[2])
		NT.tType=0

		if (self.UnfixedWidget[-1].fixrbut.type=="flexible"):
			NT.tType=1
			NT.mStart=int(self.UnfixedWidget[-1].lowerboundhh.text[0]+self.UnfixedWidget[-1].lowerboundhh.text[2])*100+int(self.UnfixedWidget[-1].lowerboundmm.text[0]+self.UnfixedWidget[-1].lowerboundmm.text[2])
			NT.mEnd=int(self.UnfixedWidget[-1].upperboundhh.text[0]+self.UnfixedWidget[-1].upperboundhh.text[2])*100+int(self.UnfixedWidget[-1].upperboundmm.text[0]+self.UnfixedWidget[-1].upperboundmm.text[2])
			NT.priority=int(self.UnfixedWidget[-1].priority.text[0]+self.UnfixedWidget[-1].priority.text[2])
			NT.partition= 1 if(self.UnfixedWidget[-1].partition.value) else 0
			print "task:\t",NT.title,"\tduration:\t",NT.duration,"\ttype:\t",NT.tType,"\tlowerbound\t",NT.mStart,"\tupperbound",NT.mEnd,"\tpriority\t",NT.priority,"\tpartition\t",NT.partition
			return NT
	
		NT.mStart=int(self.UnfixedWidget[-1].mustarthh.text[0]+self.UnfixedWidget[-1].mustarthh.text[2])*100+int(self.UnfixedWidget[-1].mustartmm.text[0]+self.UnfixedWidget[-1].mustartmm.text[2])
		NT.mEnd = addTime(NT.mStart,NT.duration)
		print "task:\t",NT.title,"\tduration:\t",NT.duration,"\ttype:\t",NT.tType,"\tmustart\t",NT.mStart
		return NT

	def GetTaskTitle(self,event):
		if event.type==pygame.KEYDOWN:
			x=event.key
			if pygame.key.get_mods() and pygame.KMOD_LSHIFT:
				#pass
				if x>=39 and x<=122:
					self.UnfixedWidget[-1].concatenateInputText(chr(x).title())	
			elif x==K_ESCAPE or x==K_RETURN:
				getTitle=False
				caps=False
			elif x==K_BACKSPACE:
				self.UnfixedWidget[-1].backspace()


			else:
				#if caps==False:
				if x<255:
					self.UnfixedWidget[-1].concatenateInputText(chr(x))	


	def drawUI(self,positionreferencecounter):
		self.AppDisplay.fill((108,206,203))
		#pygame.draw.rect(self.AppDisplay,BACGROUND_COLOR,(650,0,WIN_SIZE_X,WIN_SIZE_Y))
		self.taskPane.draw(self.AppDisplay)
		self.addButton.draw(self.AppDisplay)
		self.clearButton.draw(self.AppDisplay)

		#draw task
		self.AllocationSpaceUI=[]
		#positionreferencecounter=0
		X=self.TaskAllocator.CS.sched
		while X!=None:
			TBUI=Wid.TimeBlockUI((205,105+(49*positionreferencecounter)),(255,222,0),(390,50),X)
			if TBUI.status==None:
				TBUI.color=(239, 113, 38)
			elif TBUI.status.tType==1:
				TBUI.color=(255,245,171)
			self.AllocationSpaceUI.append(TBUI)
			positionreferencecounter+=1
			X=X.next


		for i in self.AllocationSpaceUI:
			i.draw(self.AppDisplay)

		for i in self.UnfixedWidget:
			i.draw(self.AppDisplay)

		pygame.draw.rect(self.AppDisplay,(108,206,203),((0,550),(800,50)))	
		pygame.draw.rect(self.AppDisplay,(108,206,203),((0,0),(800,50)))
		self.taskPaneHeader.draw(self.AppDisplay)
		self.taskPaneHeader.addText("Task",(250,15),self.AppDisplay)
