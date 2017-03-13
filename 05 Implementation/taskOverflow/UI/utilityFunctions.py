import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def isMouseover(myMouse_pos,Object):
	if myMouse_pos[0]>=Object.position[0] and myMouse_pos[0]<=Object.position[0]+Object.dimension[0] and myMouse_pos[1]>=Object.position[1] and myMouse_pos[1]<=Object.position[1]+Object.dimension[1]:
		return True
	else:
		return False
def isMouseoverDropDown(myMouse_pos,Object):
	if myMouse_pos[0]>=Object.position[0] and myMouse_pos[0]<=Object.position[0]+Object.dimension[0] and myMouse_pos[1]>=Object.position[1] and myMouse_pos[1]<=Object.position[1]+(Object.numButton*Object.dimension[1]):
		return True
	else:
		return False

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key

    else:
      pass		

def getinputothers(Object,counter,event,condition):

	UnfixedWidget=Object

	buttonhh=buttonmm=None
	buttonp=None


	if id(condition)==id(UnfixedWidget[-1].isgetDuration):
		buttonhh=UnfixedWidget[-1].durationbuttonhh
		buttonmm=UnfixedWidget[-1].durationbuttonmm
	elif id(condition)==id(UnfixedWidget[-1].isgetmustart):
		buttonhh=UnfixedWidget[-1].mustarthh
		buttonmm=UnfixedWidget[-1].mustartmm
	elif id(condition)==id(UnfixedWidget[-1].isgetlowerbound):
		buttonhh=UnfixedWidget[-1].lowerboundhh
		buttonmm=UnfixedWidget[-1].lowerboundmm
	elif id(condition)==id(UnfixedWidget[-1].isgetupperbound):
		buttonhh=UnfixedWidget[-1].upperboundhh
		buttonmm=UnfixedWidget[-1].upperboundmm
	if condition==True:

		if event.type==pygame.KEYDOWN:
			x=event.key

			if x>=48 and x<=57:
				if counter<=3:
					if counter==0:
						buttonhh.edit(chr(x),0)
					elif counter==1:
						buttonhh.edit(chr(x),2)
					elif counter==2:
						buttonmm.highlight((71, 62, 63))
						buttonmm.font_col=(242,242,242)
						buttonhh.unhighlight((255,255,255))
						buttonhh.font_col=(0,0,0)
						buttonmm.edit(chr(x),0)	
					elif counter==3:
						buttonmm.edit(chr(x),2)
					counter+=1																
			elif x==K_ESCAPE or x==K_RETURN:
				UnfixedWidget[-1].isgetDuration=False
				caps=False
			elif x==K_BACKSPACE:
				if counter==0:
					buttonhh.edit('0',0)
				elif counter==1:
					buttonhh.edit('0',2)
				elif counter==2:
					buttonmm.edit('0',0)
				elif counter==3:
					buttonmm.edit('0',2)
				counter-=1

			#check is input is on range:
			if condition==UnfixedWidget[-1].isgetDuration:
				if int(buttonhh.text[0]+buttonhh.text[2])>=24:
					UnfixedWidget[-1].durationbuttonhh.text="2 3"
				if int(buttonmm.text[0]+buttonmm.text[2])>=60:
					UnfixedWidget[-1].durationbuttonmm.text="5 9"	
			elif condition==UnfixedWidget[-1].isgetmustart:
				if int(buttonhh.text[0]+buttonhh.text[2])>=24:
					UnfixedWidget[-1].mustarthh.text="2 3"
				if int(buttonmm.text[0]+buttonmm.text[2])>=60:
					UnfixedWidget[-1].mustartmm.text="5 9"
			elif condition==UnfixedWidget[-1].isgetlowerbound:
				if int(buttonhh.text[0]+buttonhh.text[2])>=24:
					UnfixedWidget[-1].lowerboundhh.text="2 3"
				if int(buttonmm.text[0]+buttonmm.text[2])>=60:
					UnfixedWidget[-1].lowerboundmm.text="5 9"
			elif condition==UnfixedWidget[-1].isgetupperbound:
				if int(buttonhh.text[0]+buttonhh.text[2])>=24:
					UnfixedWidget[-1].upperboundhh.text="2 3"
				if int(buttonmm.text[0]+buttonmm.text[2])>=60:
					UnfixedWidget[-1].upperboundmm.text="5 9"


	return UnfixedWidget,counter

def getpriority(Object,counter,event,condition):
	UnfixedWidget=Object
	buttonp=UnfixedWidget[-1].priority

	if condition==True:

		if event.type==pygame.KEYDOWN:
			x=event.key

			if x>=48 and x<=57:
				if counter<=3:
					if counter==0:
						buttonp.edit(chr(x),0)
					elif counter==1:
						buttonp.edit(chr(x),2)
					counter+=1																
			elif x==K_ESCAPE or x==K_RETURN:
				UnfixedWidget[-1].isgetDuration=False
				caps=False
			elif x==K_BACKSPACE:
				if counter==0:
					buttonp.edit('0',0)
				elif counter==1:
					buttonp.edit('0',2)
				counter-=1	
	return UnfixedWidget,counter