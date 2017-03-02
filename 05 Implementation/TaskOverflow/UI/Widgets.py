import pygame 
#import inputbox

class Button(pygame.Rect):
	def __init__(self,position,color,dimension,text=None,font_col=(200,200,200),bold=False):
		self.position=position
		self.color=color
		self.dimension=dimension
		self.rect = pygame.Rect(position, dimension)
		self.text=text
		self.font_col=font_col
		self.bold=bold		

	def draw(self,surface):
		#pygame.draw.rect(surface,(0,0,0),(self.dimension[0]+2,self.dimension[1]+2,self.position[0]-1,self.position[1]-1))

		pygame.draw.rect(surface,self.color,self.rect)
		self.font = pygame.font.SysFont('Helvetica', 18)
		self.font.set_bold(self.bold)
		if self.text!=None:	
			surface.blit(self.font.render(self.text, True, self.font_col), (self.position[0]+5,self.position[1]+5))	

	def highlight(self,color):
		#self.color=(184,25,255)
		self.color=color
	def unhighlight(self,color):
		#self.color=(148,0,211)
		self.color=color

	def isclicked(self):
		print "do some UI stuffs and call addFunction"
		
	def edit(self,char,index):
		l=list(self.text)
		l[index]=char
		self.text=''.join(l)

class MenuBar(pygame.Rect):
	def __init__(self,position,color,dimension,text=None):
		self.position=position
		self.color=color
		self.dimension=dimension
		self.rect = pygame.Rect(position, dimension)

	def draw(self,surface):
		pygame.draw.rect(surface,(200,200,200),((self.position[0],self.position[1]+2),self.dimension))		
		pygame.draw.rect(surface,self.color,self.rect)



class Input(pygame.sprite.Sprite):
	def __init__(self,position,dimension,text=None):
		image="Resources\inputimg2.png"
		self.image=pygame.image.load(image).convert()
		self.image.set_alpha(75)
		self.position=position
		self.dimension=dimension
		self.text=text
		self.image=pygame.transform.scale(self.image,self.dimension)


	def draw(self,surface):
		surface.blit(self.image,self.position)	
		self.font = pygame.font.SysFont('Helvetica', 18)
		if self.text!=None:	
			surface.blit(self.font.render(self.text, True, (0,0,0)), (self.position[0]+5,self.position[1]+5))	


class RadioButton(pygame.sprite.Sprite):
	def __init__(self,position,color,radius,_type=None):
		self.position=position
		self.color=color
		self.radius=radius
		self.type=_type
		#self.cir = pygame.Rect(position, dimension)	
	def draw(self,surface):
		pygame.draw.circle(surface,(200,200,200),self.position,self.radius+2)
		pygame.draw.circle(surface,(200,200,200),(self.position[0]+150,self.position[1]),self.radius+2)
		self.font = pygame.font.SysFont('Helvetica', 18)
		surface.blit(self.font.render("fix", True, (0,0,0)), (self.position[0]+20,self.position[1]-13))
		surface.blit(self.font.render("flexible", True, (0,0,0)), (self.position[0]+170,self.position[1]-13))

		if self.type=="fix":
			pygame.draw.circle(surface,self.color,self.position,self.radius)
			pygame.draw.circle(surface,(255,255,255),(self.position[0]+150,self.position[1]),self.radius)
		else:
			pygame.draw.circle(surface,(255,255,255),self.position,self.radius)
			pygame.draw.circle(surface,self.color,(self.position[0]+150,self.position[1]),self.radius)			
		#elif self.
	def gettasktype(self,mouse_pos):
		if mouse_pos[0]>self.position[0]-self.radius and mouse_pos[0]<self.position[0]+self.radius and mouse_pos[1]>self.position[1]-self.radius and mouse_pos[1]<self.position[1]+self.radius:
			return "fix"
		elif mouse_pos[0]>self.position[0]+150-self.radius and mouse_pos[0]<self.position[0]+150+self.radius and mouse_pos[1]>self.position[1]-self.radius and mouse_pos[1]<self.position[1]+self.radius:
			return "flexible"

class boolButton(pygame.sprite.Sprite):
	def __init__(self,position,color,radius,value=False):
		self.position=position
		self.color=color
		self.radius=radius
		self.value=value
	def draw(self,surface):
		pygame.draw.circle(surface,(200,200,200),self.position,self.radius+2)
		self.font = pygame.font.SysFont('Helvetica', 18)
		print self.value
		if self.value==True:

			pygame.draw.circle(surface,self.color,self.position,self.radius)
		elif self.value==False:
			print "drawing"
			pygame.draw.circle(surface,(255,255,255),self.position,self.radius)
	def changeValue(self,mouse_pos):
		if mouse_pos[0]>self.position[0]-self.radius and mouse_pos[0]<self.position[0]+self.radius and mouse_pos[1]>self.position[1]-self.radius and mouse_pos[1]<self.position[1]+self.radius:
			return not self.value
class dropdown(pygame.Rect):
	def __init__(self,position,color,dimension,numButton):
		self.position=position
		self.color=color
		self.dimension=dimension
		self.drbuttons=[]
		self.numButton=numButton
		for i in range(0,self.numButton):
			self.drbuttons.append(Button((self.position[0],self.position[1]+(i*self.dimension[1])),self.color,self.dimension,str(i)))

	def draw(self,surface):
		for i in self.drbuttons:
			i.draw(surface)

class AddTaskUI(pygame.Rect):
	def __init__(self,position,dimension,color):
		self.isgetDuration=False
		self.isgetmustart=False
		self.isgetlowerbound=False
		self.isgetupperbound=False
		self.isgetpriority=False

		self.position=position
		self.dimension=dimension
		self.color=color
		self.rect = pygame.Rect(self.position, self.dimension)
		self.input=Input((self.position[0]+20,self.position[1]+20),(410,30),"title:  ")

		self.durationbuttonhh=Button((self.position[0]+90,self.position[1]+60),(255,255,255),(35,30),"0 0")
		self.durationbuttonmm=Button((self.position[0]+130,self.position[1]+60),(255,255,255),(35,30),"0 0")
		self.cancel=Button((self.position[0]+300,self.position[1]+300),(229,204,255),(75,25)," Cancel")
		self.add=Button((self.position[0]+75,self.position[1]+300),(176,97,255),(75,25),"   Add",(20,20,20))		

		self.fixrbut=RadioButton((self.position[0]+110,self.position[1]+120),(148,0,211),10,"fix")

		self.mustarthh=Button((self.position[0]+100,self.position[1]+150),(255,255,255),(35,30),"0 0")
		self.mustartmm=Button((self.position[0]+140,self.position[1]+150),(255,255,255),(35,30),"0 0")
		self.lowerboundhh=Button((self.position[0]+360,self.position[1]+150),(255,255,255),(35,30),"0 0")
		self.lowerboundmm=Button((self.position[0]+400,self.position[1]+150),(255,255,255),(35,30),"0 0")
		self.upperboundhh=Button((self.position[0]+360,self.position[1]+190),(255,255,255),(35,30),"0 0")
		self.upperboundmm=Button((self.position[0]+400,self.position[1]+190),(255,255,255),(35,30),"0 0")
		self.priority=Button((self.position[0]+400,self.position[1]+230),(255,255,255),(35,30),"0 0")
		self.partition=boolButton((self.position[0]+420,self.position[1]+275),(148,0,211),10,False)


	def concatenateInputText(self,char):
		self.input.text=self.input.text+char
		#print self.input.text


	def backspace(self):
		if len(self.input.text)>6:
			self.input.text = self.input.text[:-1]

	def draw(self,surface):
		#self.rect = pygame.Rect(self.position, self.dimension)
		pygame.draw.rect(surface,self.color,self.rect)
		self.cancel.draw(surface)
		self.add.draw(surface)
		#answer=inputbox.ask(surface, "Name") + " was entered"
		self.input.draw(surface)
		self.durationbuttonhh.draw(surface)
		self.durationbuttonmm.draw(surface)
		self.fixrbut.draw(surface)
		self.mustarthh.draw(surface)
		self.mustartmm.draw(surface)
		self.lowerboundhh.draw(surface)
		self.lowerboundmm.draw(surface)
		self.upperboundhh.draw(surface)
		self.upperboundmm.draw(surface)
		self.priority.draw(surface)
		self.partition.draw(surface)

		#
		self.font = pygame.font.SysFont('Helvetica', 16)
		surface.blit(self.font.render("duration", True, (0,0,0)), (self.position[0]+20,self.position[1]+65))
		surface.blit(self.font.render("type", True, (0,0,0)), (self.position[0]+20,self.position[1]+110))
		surface.blit(self.font.render("must start at: ", True, (0,0,0)), (self.position[0]+20,self.position[1]+155))
		surface.blit(self.font.render("must start as early as: ", True, (0,0,0)), (self.position[0]+225,self.position[1]+155))
		surface.blit(self.font.render("must end as late as: ", True, (0,0,0)), (self.position[0]+225,self.position[1]+195))
		surface.blit(self.font.render("priority: ", True, (0,0,0)), (self.position[0]+225,self.position[1]+235))
		surface.blit(self.font.render("partition: ", True, (0,0,0)), (self.position[0]+225,self.position[1]+265))

		'''if self.isgetDuration==True:
			self.mydr.draw(surface)
			self.mydr2.draw(surface)
			self.mydr3.draw(surface)
			self.mydr4.draw(surface)
		'''