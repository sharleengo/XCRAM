'''
MIT License

Copyright (c) 2017 Gerry P. Agluba Jr,Robelle Silverio.

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

Robelle Silverio
last updated on February 8, 2017
Clear and Delete Method

File created on January 29,2017.
Developed by TaskOverflow group.

This software serves as the primary Control Classes  of our 
Software Project (Task OverFlow).

'''

import sys
import os
import math 

import Data.__init__ as Dat
#import UI.__init__ as UI

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
	'''	method  __init__
		created January 29,2017

		This method initializes an object of class AddTask.
		__init__ methods return None.
		This method has no parameters
	'''
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
	def addTask(self,task,AllocationSpace,Partition=False):
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
			if(int(task.duration) !=int(task.mustend-task.mustart) ):
				print (task.mustend-task.mustart,'error your mustend must be greater muststart') 
				return False	



			AllocationSpace.AllocateTime(task,Partition)	#a method call to AllocateTimeFix
	
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


			AllocationSpace.AllocateTime(task,Partition)#a method call to AllocateTimeFix

		#the code below performs the rescheduling of recently kicked tasks
		for i in AllocationSpace.priorityQueue:
			if(AllocationSpace.AllocateTime(i[1])==True):
				print ("true")
				AllocationSpace.priorityQueue.pop()

		print ("saving...")
		AllocationSpace.Save("Data\DataFiles\myData.in")

		AllocationSpace.GetData() 

'''This class is a ControlClass for prompting user inputs.
Primary attributes is Allocator which an instance of AddTask class.
Methods is ActiveState
'''
class Menu():

	def __init__(self):
		self.Allocator=AddTask() #this is an initialized addTask class



	def ActiveState(self,AllocationSpace):
		while(True):
			#os.system('cls')
			AllocationSpace.GetData()		
			print ("[A].Add task\t[C].Clear_Schedule\t[D].Delete\t[Q].Quit\n")
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
						mustend=mustart+duration
						print (mustend)
						if(mustend%100>59):
							mustend=mustend+40
						print (mustend)
					except ValueError as V:
					    print(V)
					else:
						newT=Dat.FixTask(title,duration,mustart,mustend)
						newT=self.Allocator.addTask(newT,AllocationSpace)


				elif(ttype==2):
					try:
						priority=int(raw_input("enter priority"))#this variable takes note of the entered priority
						lowerbound=int(raw_input("inter lowerbound\n")) #this variable takes note of the entered lowerbound
						upperbound=int(raw_input("inter upperbound\n")) #this variable takes note of the entered upperbound
						Partition=bool(input("do you want to partition?\n[1]Yes\t\t[0]NO\n"))
					except ValueError as V:
					    print(V)
					else:
						print (Partition)
						newT=Dat.FlexibleTask(title,duration,priority,lowerbound,upperbound)
						newT=self.Allocator.addTask(newT,AllocationSpace,Partition)

			elif(event=="C"):
				AllocationSpace.Clear() #clears the timeblock (in its initial state: 0000 2400)
			elif(event=="D"):
				tasky=raw_input(("Enter name of task to delete:\n")) #tasky holds the title of the task that will be deleted
				AllocationSpace.Dela(tasky) #calls the function that will delete the task which the user entered
			if (event=="Q"):
				break
		print ("saving...")
		AllocationSpace.Save("Data\DataFiles\myData.in")

if __name__=="__main__":
	pass
