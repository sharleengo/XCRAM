import sys
import os

import Data.__init__ as Dat
import UI.__init__ as UI




class AddTask():
	def __init__(self):
		self.title=None
	def addTask(self,task,AllocationSpace):
		'''check parameters of task'''

		if isinstance(task,Dat.FixTask):
			if(task.title==None):
				print ("error you entered a task with no title") 
				return False
			if(task.duration==None):
				print ("error you entered a task with no duration") 
				return False
			if(task.muststart<0 or task.muststart>=2400 ):
				print ('error your mustart must lie from 0 to not higher than 2400') 
				return False
			if(task.mustend<=0 or task.muststart>2400 ):
				print ('error your mustend must be greater than 0 but not higher than 2400') 
				return False
			if(task.mustend<=task.muststart ):
				print ('error your mustend must be greater muststart') 
				return False
			if(duration !=task.mustend-task.muststart ):
				print ('error your mustend must be greater muststart') 
				return False				
			AllocationSpace.AllocateTimeFix(task)				
	
		elif isinstance(task,Dat.FlexibleTask):
			if(task.title==None):
				print ("error you entered a task with no title")
				return False
			if(task.duration==None):
				print ("error you entered a task with no duration") 
				return False
			if(task.lowerbound<0 or task.upperbound>=2400 ):
				print ('error your lowerbound must lie from 0 to not higher than 2400') 
				return False
			if(task.lowerbound<=0 or task.upperbound>2400 ):
				print ('error your upperbound must be greater than 0 but not higher than 2400') 
				return False
			if(task.lowerbound<=task.upperbound ):
				print ('error your upperbound must be greater lowerbound') 
				return False
			if(duration <=task.upperbound-task.lowerbound ):
				print ('error your mustend must be greater muststart') 
				return False
			if(task.priority<0):
				print ('error entered number is not allowed') 
				return False
			AllocationSpace.AllocateTime(task)

class Menu():
	def __init__(self):
		self.Allocator=AddTask()

	def ActiveState(self,AllocationSpace):
		while(True):
			os.system('cls')
			AllocationSpace.GetData()		
			print ("[A].Add task\n")
			event=raw_input("")
			if(event=="A"):
				newT=None
				title=raw_input("enter task title\n")
				duration=raw_input("enter duration\n")
				ttype=input("enter task type\n[1].Fix Task \t[2].Flexible Task\n")
				if(ttype==1):
					mustart=input("enter start time\n")
					mustend=input("enter end time\n")
					newT=Dat.FixTask(title,duration,mustart,mustend)
					newT=self.Allocator.addTask(newT,AllocationSpace)
				elif(ttype==2):
					priority=input("enter priority")
					lowerbound=input("inter lowerbound\n")
					upperbound=input("inter upperbound\n")
					newT=Dat.FlexibleTask(title,duration,priority,lowerbound,upperbound)
					newT=self.Allocator.addTask(newT,AllocationSpace)







