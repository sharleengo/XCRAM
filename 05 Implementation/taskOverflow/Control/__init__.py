'''
MIT License

Copyright (c) 2017 Gerry P. Agluba Jr.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


This is a course requirement for CS192 Software Engineering II
under the supervision of Asst. Prof. Ma.Rowena C. Solamo 
of the Department of Computer Science, College of Engineering,
University of the Philippines, Diliman for the AY 2016-2017

Gerry Agluba Jr.
last updated on January 31,2017
Initial Software for Control Classes , its structures and methods.

File created on January 29,2017.
Developed by TaskOverflow group.

This software serves as the primary Control Classes  of our 
Software Project (Task OverFlow).

'''

import sys
import os
import math 

import Data.__init__ as Dat
import UI.__init__ as UI

'''
For all Classes, no files or database tables had been used.
module from Data.__init__ and UI__init__ had been impoted.
Python module, and system model was also imported
'''

'''This class is a ControlClass for Adding Task.
Atributes:None
Methods involve is addTask
'''
class AddTask():
	def __init__(self):
		pass

	'''method addTask
		created January 29,2017	

		This method is responsible for checking the parameters for a specific Task.
		It checks if each attributes of the task is valid. And this methods decide if 
		the task entered is valid.
		The method returns False if it does not passed the necessary condition for Allocation.
		Formal parameters of this method is task and AllocationSpace of type Task and AllocationSpace respectively
		AllocationSpace is an instance off the class Allocation in which we will allocate task.
	'''
	def addTask(self,task,AllocationSpace):
		'''check parameters of task'''

		if isinstance(task,Dat.FixTask):

			print (task.mustart,task.mustend,task.duration)
			if(task.mustart%100 > 59 or task.mustend%100>59 or task.duration%100>59):
				print ("invalid time input")
				return False
			task.duration=task.duration-(task.duration%100)+((task.duration%100)*(100.0/60))
			task.mustart=task.mustart-(task.mustart%100)+(task.mustart%100)*(100.0/60)
			task.mustend=task.mustend-(task.mustend%100)+((task.mustend%100)*(100.0/60))

			print task.duration,task.mustart,task.mustend			
			if(task.title==""):
				print ("error you entered a task with no title") 
				return False
			if(task.duration==None):
				print ("error you entered a task with no duration") 
				return False
			if(task.duration<=0):
				print ("error duration must be greater than 0") 
				return False				
			if(task.mustart<0 or task.mustart>=2400 ):
				print ('error your mustart must lie from 0 to not higher than 2400') 
				return False
			if(task.mustend<=0 or task.mustend>2400 ):
				print ('error your mustend must be greater than 0 but not higher than 2400') 
				return False
			if(task.mustend<=task.mustart ):
				print ('error your mustend must be greater muststart') 
				return False
			if(task.duration !=task.mustend-task.mustart ):
				print ('error your mustend must be greater muststart') 
				return False	



			AllocationSpace.AllocateTimeFix(task)	#a method call to AllocateTimeFix
	
		elif isinstance(task,Dat.FlexibleTask):
			if(task.lowerbound%100 > 100 or task.upperbound%100>100 or task.duration%100>100):
				print ("invalid time input")				

			task.duration=task.duration-(task.duration%100)+((task.duration%100)*(100.0/60))
			task.lowerbound=task.lowerbound-(task.lowerbound%100)+((task.lowerbound%100)*(100.0/60))
			task.upperbound=task.upperbound-(task.upperbound%100)+(task.upperbound%100)*(100.0/60)


			if(task.title==""):
				print ("error you entered a task with no title")
				return False
			if(task.duration==None):
				print ("error you entered a task with no duration") 
				return False
			if(task.duration<=0):
				print ("error duration must be greater than 0") 
				return False								

			if(task.priority==None):
				print ("error user must enter priority") 
				return False												

			if(task.lowerbound<0 or task.lowerbound>=2400 ):
				print ('error your lowerbound must lie from 0 to not higher than 2400') 
				return False
			if(task.upperbound<=0 or task.upperbound>2400 ):
				print ('error your upperbound must be greater than 0 but not higher than 2400') 
				return False
			if(task.lowerbound>=task.upperbound ):
				print ('error your upperbound must be greater lowerbound') 
				return False
			if(task.priority<0):
				print ('error entered number is not allowed') 
				return False


			AllocationSpace.AllocateTime(task)#a method call to AllocateTimeFix

		AllocationSpace.GetData() 
		#the code below performs the rescheduling of recently kicked tasks
		for i in AllocationSpace.priorityQueue:
			if(AllocationSpace.AllocateTime(i[1])==True):
				print ("true")
				AllocationSpace.priorityQueue.pop()


'''This class is a ControlClass for prompting user inputs.
Primary attributes is Allocator which an instance of AddTask class.
Methods is ActiveState
'''
class Menu():
	def __init__(self):
		self.Allocator=AddTask() #this is an initialized addTask class


	'''method ActiveState
		created January 29,2017	

		This method is the does the interface between the use and the software itself.
		It provides prompt which the user have to respond to inorder to perform the Allocation.
		The method does not return anything.
		Formal parameters of this method is AllocationSpace of type AllocationSpace.
	'''	
	def ActiveState(self,AllocationSpace):
		while(True):
			#os.system('cls')
			AllocationSpace.GetData()		
			print ("[A].Add task\n")
			event=raw_input("") #this keeps tracks of the actions specified the user
			if(event=="A"):
				newT=None #this is a temporary variablee for the possible task to be created
				title=raw_input("enter task title\n") #this variable takes note of the entered title
				ttype=0
				try:

					duration=int(raw_input("enter duration\n")) #this variable takes note of the entered duration
					ttype=int(raw_input("enter task type\n[1].Fix Task \t[2].Flexible Task\n"))			
				except ValueError as V:
					print (V)
				if(ttype==1):
					try:
						mustart=int(raw_input("enter start time\n")) #this variable takes note of the entered mustart
						mustend=int(raw_input("enter end time\n")) #this variable takes note of the entered mustend
					except ValueError as V:
					    print(V)
					else:
						newT=Dat.FixTask(title,duration,mustart,mustend)
						newT=self.Allocator.addTask(newT,AllocationSpace)


				elif(ttype==2):
					try:
						priority=int(raw_input("enter priority")) #this variable takes note of the entered priority
						lowerbound=int(raw_input("inter lowerbound\n")) #this variable takes note of the entered lowerbound
						upperbound=int(raw_input("inter upperbound\n")) #this variable takes note of the entered upperbound
					except ValueError as V:
					    print(V)
					else:
						newT=Dat.FlexibleTask(title,duration,priority,lowerbound,upperbound)
						newT=self.Allocator.addTask(newT,AllocationSpace)
