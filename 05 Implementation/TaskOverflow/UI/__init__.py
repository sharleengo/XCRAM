
'''
import necesarry libraries from pygame and external modules Widgets and utilitFunctions
'''
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import Widgets as Wid
import utilityFunctions as util
#import get_input

'''define constant value for windows size
'''
WIN_SIZE_X=800
WIN_SIZE_Y=600


class mainUI():

	def __init__(self):

		pygame.init() 		#initialize pygame
		AppDisplay=pygame.display.set_mode((WIN_SIZE_X,WIN_SIZE_Y)) 		#draw the window
		#AppDisplay.fill((221,247,251,100))
		bg = pygame.image.load("Resources\\background.png").convert() 		#add the background
		timetable=pygame.image.load("Resources\\timetable.png").convert() 	#add the timetable
		timetable=pygame.transform.scale(timetable,(400,1200)) 				

		bg1=pygame.transform.scale(bg,(800,30)) 							#add loweborder

		#AppDisplay.fill((216,199,255))
		AppName=pygame.display.set_caption('TaskOverFlow') 					#set appname
		myMouse=pygame.mouse 												#set mouse


		myMenuBar=Wid.MenuBar((0,0),(148,0,211),(WIN_SIZE_X,50)) 			#initialze the menubar
		addButton=Wid.Button((10,20),(148,0,211),(100,25),"+ New Task",(200,200,200),True) 		#add functional add button
		clear=Wid.Button((110,20),(148,0,211),(100,25),"x Clear",(200,200,200),True) 			#add functional clear button
		AllocationHeader=Wid.MenuBar((100,50),(229,204,255),(400,50))		#add header for timetable
		font = pygame.font.SysFont('Helvetica', 18)							#set font 

		UnfixedWidget=[]												#initialize Widget, this helps in the drawing,redrawing and undrawing of addTaskUI

		AppExit=False														#set loop exit to false
		addTask=False 														#initialize boolean addTask to False
		getTitle=False 														#initialize boolean getTtile to False
		caps=False
		getduration=False
		getdurationcounter=0
		getmustartcounter=0
		getlowerboundcounter=0
		getupperboundcounter=0
		getprioritycounter=2

		clock=pygame.time.Clock()
		move=0
		scroll_y=0

		switch=0
		ms=0
		task=Wid.Button((200,100),(184,25,255),(300,1))
		while not AppExit:
			for event in pygame.event.get():

				if event.type==pygame.QUIT: 								#this quits the app
					AppExit=True

				elif event.type==pygame.MOUSEMOTION:
					#higlight
					if util.isMouseover(myMouse.get_pos(),addButton): 		#higlights the addButton
						addButton.highlight((184,25,255))
					elif  not util.isMouseover(myMouse.get_pos(),addButton): 
						addButton.unhighlight((148,0,211))
					elif util.isMouseover(myMouse.get_pos(),clear):			#higlights the clear button
						clear.highlight((184,25,255))
					elif  not util.isMouseover(myMouse.get_pos(),clear):
						clear.unhighlight((148,0,211))

					if addTask==True:
						if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].cancel): 		#highlighst the cancel button
							UnfixedWidget[-1].cancel.highlight((234, 222, 247))
						elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].cancel): 
							UnfixedWidget[-1].cancel.unhighlight((229,204,255))

						if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].add):			#higlights the addbutton in addTASKUI
							UnfixedWidget[-1].add.highlight((205,155,255))
							UnfixedWidget[-1].add.font_col=(242,242,242)
						elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].add): 	#
							UnfixedWidget[-1].add.unhighlight((176,97,255))
							UnfixedWidget[-1].add.font_col=(0,0,0)

						if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].durationbuttonhh):			#higlights the addbutton in addTASKUI
							UnfixedWidget[-1].durationbuttonhh.highlight((205,155,255))
							UnfixedWidget[-1].durationbuttonhh.font_col=(242,242,242)
						elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].durationbuttonhh): 	#
							UnfixedWidget[-1].durationbuttonhh.unhighlight((255,255,255))
							UnfixedWidget[-1].durationbuttonhh.font_col=(0,0,0)

						if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].durationbuttonmm):			#higlights the addbutton in addTASKUI
							UnfixedWidget[-1].durationbuttonmm.highlight((205,155,255))
							UnfixedWidget[-1].durationbuttonmm.font_col=(242,242,242)
						elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].durationbuttonmm): 	#
							UnfixedWidget[-1].durationbuttonmm.unhighlight((255,255,255))
							UnfixedWidget[-1].durationbuttonmm.font_col=(0,0,0)


						if UnfixedWidget[-1].fixrbut.type=="fix":
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].mustarthh):			#higlights the addbutton in addTASKUI
								UnfixedWidget[-1].mustarthh.highlight((205,155,255))
								UnfixedWidget[-1].mustarthh.font_col=(242,242,242)
							elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].mustarthh): 	#
								UnfixedWidget[-1].mustarthh.unhighlight((255,255,255))
								UnfixedWidget[-1].mustarthh.font_col=(0,0,0)
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].mustartmm):			#higlights the addbutton in addTASKUI
								UnfixedWidget[-1].mustartmm.highlight((205,155,255))
								UnfixedWidget[-1].mustartmm.font_col=(242,242,242)
							elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].mustartmm): 	#
								UnfixedWidget[-1].mustartmm.unhighlight((255,255,255))
								UnfixedWidget[-1].mustartmm.font_col=(0,0,0)
						if UnfixedWidget[-1].fixrbut.type=="flexible":
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].lowerboundhh):			#higlights the addbutton in addTASKUI
								UnfixedWidget[-1].lowerboundhh.highlight((205,155,255))
								UnfixedWidget[-1].lowerboundhh.font_col=(242,242,242)
							elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].lowerboundhh): 	#
								UnfixedWidget[-1].lowerboundhh.unhighlight((255,255,255))
								UnfixedWidget[-1].lowerboundhh.font_col=(0,0,0)
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].lowerboundmm):			#higlights the addbutton in addTASKUI
								UnfixedWidget[-1].lowerboundmm.highlight((205,155,255))
								UnfixedWidget[-1].lowerboundmm.font_col=(242,242,242)
							elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].lowerboundmm): 	#
								UnfixedWidget[-1].lowerboundmm.unhighlight((255,255,255))
								UnfixedWidget[-1].lowerboundmm.font_col=(0,0,0)
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].upperboundhh):			#higlights the addbutton in addTASKUI
								UnfixedWidget[-1].upperboundhh.highlight((205,155,255))
								UnfixedWidget[-1].upperboundhh.font_col=(242,242,242)
							elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].upperboundhh): 	#
								UnfixedWidget[-1].upperboundhh.unhighlight((255,255,255))
								UnfixedWidget[-1].upperboundhh.font_col=(0,0,0)
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].upperboundmm):			#higlights the addbutton in addTASKUI
								UnfixedWidget[-1].upperboundmm.highlight((205,155,255))
								UnfixedWidget[-1].upperboundmm.font_col=(242,242,242)
							elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].upperboundmm): 	#
								UnfixedWidget[-1].upperboundmm.unhighlight((255,255,255))
								UnfixedWidget[-1].upperboundmm.font_col=(0,0,0)
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].priority):			#higlights the addbutton in addTASKUI
								UnfixedWidget[-1].priority.highlight((205,155,255))
								UnfixedWidget[-1].priority.font_col=(242,242,242)
							elif  not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].priority): 	#
								UnfixedWidget[-1].priority.unhighlight((255,255,255))
								UnfixedWidget[-1].priority.font_col=(0,0,0)



				elif event.type==pygame.MOUSEBUTTONDOWN:
					if myMouse.get_pressed()==(1,0,0):
						if addTask==False:
							if util.isMouseover(myMouse.get_pos(),addButton):
								myAddTaskUI=Wid.AddTaskUI((200,175),(450,350),(229,204,255))
								UnfixedWidget.append(myAddTaskUI)						
								addTask=True
							'''this block of code initializes addTASKUI if add button is clicked'''

						elif addTask==True:
							#title
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].input):
								print "getting input"
								getTitle=True
							if not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].input):
								getTitle=False								


							#duration hours
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].durationbuttonhh):
								print "gett duration"

								if UnfixedWidget[-1].isgetDuration==False:
									UnfixedWidget[-1].isgetDuration=True
								getdurationcounter=0

							if not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].durationbuttonhh):
								UnfixedWidget[-1].isgetDuration=False
								getdurationcounter=0
							#duration minute
							if util.isMouseover(myMouse.get_pos(),myAddTaskUI.durationbuttonmm):
								#myAddTaskUI.durationbuttonmm.text="0 0"
								print "get duration"
								if UnfixedWidget[-1].isgetDuration==False:
									UnfixedWidget[-1].isgetDuration=True
								getdurationcounter=2

							
							#type
							if UnfixedWidget[-1].fixrbut.gettasktype(myMouse.get_pos())=="fix":
								UnfixedWidget[-1].fixrbut.type="fix"
								UnfixedWidget[-1].lowerboundhh.text="0 0"
								UnfixedWidget[-1].lowerboundmm.text="0 0"
								UnfixedWidget[-1].upperboundhh.text="0 0"
								UnfixedWidget[-1].upperboundmm.text="0 0"
								UnfixedWidget[-1].lowerboundhh.font_col=(200,200,200)
								UnfixedWidget[-1].lowerboundmm.font_col=(200,200,200)
								UnfixedWidget[-1].upperboundhh.font_col=(200,200,200)
								UnfixedWidget[-1].upperboundmm.font_col=(200,200,200)
								UnfixedWidget[-1].priority.font_col=(200,200,200)

							if UnfixedWidget[-1].fixrbut.gettasktype(myMouse.get_pos())=="flexible":
								UnfixedWidget[-1].fixrbut.type="flexible"
								UnfixedWidget[-1].mustarthh.text="0 0"
								UnfixedWidget[-1].mustartmm.text="0 0"						
								UnfixedWidget[-1].mustarthh.font_col=(200,200,200)
								UnfixedWidget[-1].mustartmm.font_col=(200,200,200)

							if UnfixedWidget[-1].fixrbut.type=="fix":
								if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].mustarthh):
									print "gett mustart"
									if UnfixedWidget[-1].isgetmustart==False:
										UnfixedWidget[-1].isgetmustart=True
									getmustartcounter=0

								if not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].mustarthh):
									UnfixedWidget[-1].isgetmustart=False
									getmustartcounter=0
								#duration minute
								if util.isMouseover(myMouse.get_pos(),myAddTaskUI.mustartmm):
									#myAddTaskUI.durationbuttonmm.text="0 0"
									print "get mustart"
									if UnfixedWidget[-1].isgetmustart==False:
										UnfixedWidget[-1].isgetmustart=True
									getmustartcounter=2

								#turn off lowebound and uper
								UnfixedWidget[-1].isgetlowerbound=False
								UnfixedWidget[-1].isgetupperbound=False
								UnfixedWidget[-1].isgetpriority=False
								UnfixedWidget[-1].partition.value=False

							if UnfixedWidget[-1].fixrbut.type=="flexible":
								if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].lowerboundhh):
									print "gett lowebound"
									if UnfixedWidget[-1].isgetlowerbound==False:
										UnfixedWidget[-1].isgetlowerbound=True
									getlowerboundcounter=0

								if not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].lowerboundhh):
									UnfixedWidget[-1].isgetlowerbound=False
									getlowerboundcounter=0
								#duration minute
								if util.isMouseover(myMouse.get_pos(),myAddTaskUI.lowerboundmm):
									#myAddTaskUI.durationbuttonmm.text="0 0"
									print "get lowrbound"
									if UnfixedWidget[-1].isgetlowerbound==False:
										UnfixedWidget[-1].isgetlowerbound=True
									getlowerboundcounter=2


								if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].upperboundhh):
									print "gett upperbound"
									if UnfixedWidget[-1].isgetupperbound==False:
										UnfixedWidget[-1].isgetupperbound=True
									getupperboundcounter=0

								if not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].upperboundhh):
									UnfixedWidget[-1].isgetupperbound=False
									getupperboundcounter=0
								#duration minute
								if util.isMouseover(myMouse.get_pos(),myAddTaskUI.upperboundmm):
									#myAddTaskUI.durationbuttonmm.text="0 0"
									print "get upperbound"
									if UnfixedWidget[-1].isgetupperbound==False:
										UnfixedWidget[-1].isgetupperbound=True
									getupperboundcounter=2

								UnfixedWidget[-1].isgetmustart=False

								if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].priority):
									print "gett priority"
									if UnfixedWidget[-1].isgetpriority==False:
										UnfixedWidget[-1].isgetpriority=True
									getprioritycounter=2

								if not util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].priority):
									UnfixedWidget[-1].isgetpriority=False
									getprioritycounter=2				

								if UnfixedWidget[-1].partition.changeValue(myMouse.get_pos())==True:
									print "changing value to True"
									UnfixedWidget[-1].partition.value=True
								elif UnfixedWidget[-1].partition.changeValue(myMouse.get_pos())==False:
									UnfixedWidget[-1].partition.value=False
							#cancel
							if util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].cancel):
								print "cancel"
								UnfixedWidget.remove(myAddTaskUI)
								addTask=False
								getTitle=False
							elif util.isMouseover(myMouse.get_pos(),UnfixedWidget[-1].add):
								print "add"
								UnfixedWidget.remove(myAddTaskUI)
								addTask=False
								getTitle=False


					elif event.button == 4:  #scrolls up the timetable
						print "scrolling upp"
						scroll_y+=1

				elif event.type==pygame.MOUSEBUTTONUP: #scrolls down the timetable
					if event.button == 5:
						print "scrolling down"	
						scroll_y-=1

				elif event.type==pygame.KEYDOWN:
					if event.key==pygame.K_PAGEUP:
						scroll_y+=1
					elif event.key==pygame.K_PAGEDOWN:
						scroll_y-=1

				if getTitle==True:
					#x=util.get_key()
					#y=pygame.key.get_pressed()
					if event.type==pygame.KEYDOWN:
						x=event.key
						if pygame.key.get_mods() and pygame.KMOD_LSHIFT:
							#pass
							if x>=39 and x<=122:
								UnfixedWidget[-1].concatenateInputText(chr(x).title())	
						elif x==K_ESCAPE or x==K_RETURN:
							getTitle=False
							caps=False
						elif x==K_BACKSPACE:
							UnfixedWidget[-1].backspace()


						else:
							#if caps==False:
							if x<255:
								UnfixedWidget[-1].concatenateInputText(chr(x))
							#else:
								#caps=False		

				if addTask==True:		
					UnfixedWidget,getdurationcounter=util.getinputothers(UnfixedWidget,getdurationcounter,event,UnfixedWidget[-1].isgetDuration)
					if UnfixedWidget[-1].fixrbut.type=="fix":
						UnfixedWidget,getmustartcounter=util.getinputothers(UnfixedWidget,getmustartcounter,event,UnfixedWidget[-1].isgetmustart)
					elif UnfixedWidget[-1].fixrbut.type=="flexible":
						UnfixedWidget,getlowerboundcounter=util.getinputothers(UnfixedWidget,getlowerboundcounter,event,UnfixedWidget[-1].isgetlowerbound)
						UnfixedWidget,getupperboundcounter=util.getinputothers(UnfixedWidget,getupperboundcounter,event,UnfixedWidget[-1].isgetupperbound)
						UnfixedWidget,getprioritycounter=util.getinputothers(UnfixedWidget,getprioritycounter,event,UnfixedWidget[-1].isgetpriority)

			ms+=1
			#print ms
			#print clock.get_time()
			#drawingz
			keys=pygame.key.get_pressed()
			if keys[pygame.K_PAGEUP]:
				scroll_y+=10
			elif keys[pygame.K_PAGEDOWN]:
				scroll_y-=10
			elif keys[K_BACKSPACE]:
				if addTask==True:
					if getTitle==True:
						UnfixedWidget[-1].backspace()

			#check for hold keys

			AppDisplay.blit(bg,(0,0))
			
			pygame.draw.rect(AppDisplay,(200,200,200),(98,50,404,550))


			if(scroll_y<-450):
				scroll_y=-450
			if(scroll_y>250):
				scroll_y=250
			AppDisplay.blit(timetable,(100,-200+scroll_y))

			myMenuBar.draw(AppDisplay)
			addButton.draw(AppDisplay)
			clear.draw(AppDisplay)



			if addTask==True and getTitle==True:
				if ms%20==0:
					if switch==0:
						#l=list(UnfixedWidget[-1].input.text)
						#l[-1]="|"	
						#UnfixedWidget[-1].input.text=''.join(l)
						UnfixedWidget[-1].input.text+="|"
						switch=1
			
			'''test dynamics'''
			if move<=1:
				move+=.05
				pos=200*move
				task.dimension=(task.dimension[0],pos)
			pygame.draw.rect(AppDisplay,task.color,(task.position,task.dimension))


			for i in UnfixedWidget:
				i.draw(AppDisplay)



			AppDisplay.blit(bg1,(0,570))
			AllocationHeader.draw(AppDisplay)
			AppDisplay.blit(font.render("Time", True, (20,20,20)), (110,80))	
			AppDisplay.blit(font.render("Tasks", True, (20,20,20)), (250,80))	
				

			if addTask==True and getTitle==True:
				if ms%20==0:
					if switch==1:
						l=list(UnfixedWidget[-1].input.text)
						l=l[:-1]	
						UnfixedWidget[-1].input.text=''.join(l)
						switch=0

			pygame.display.update()	

			

			clock.tick(500)
			#pygame.draw.rect(AppDisplay,task.color,(task.position,task.dimension))

		pygame.quit()
		quit()


if __name__=="__main__":
	main=mainUI()
