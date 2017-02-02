import sys
import os
import math 

import Data.__init__ as Dat
import UI.__init__ as UI




class AddTask():
	def __init__(self):
		pass
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
			if(task.title==None):
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



			AllocationSpace.AllocateTimeFix(task)	
	
		elif isinstance(task,Dat.FlexibleTask):
			if(task.lowerbound%100 > 59 or task.upperbound%100>59 or task.duration%59>100):
				print ("invalid time input")				

			task.duration=task.duration-(task.duration%100)+((task.duration%100)*(100.0/60))
			task.lowerbound=task.lowerbound-(task.lowerbound%100)+((task.lowerbound%100)*(100.0/60))
			task.upperbound=task.upperbound-(task.upperbound%100)+(task.upperbound%100)*(100.0/60)


			if(task.title==None):
				print ("error you entered a task with no title")
				return False
			if(task.duration==None):
				print ("error you entered a task with no duration") 
				return False
			if(task.duration<=0):
				print ("error duration must be greater than 0") 
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


			AllocationSpace.AllocateTime(task)

		AllocationSpace.GetData()
		for i in AllocationSpace.priorityQueue:
			if(AllocationSpace.AllocateTime(i[1])==True):
				print ("true")
				AllocationSpace.priorityQueue.pop()

class Menu():
	def __init__(self):
		self.Allocator=AddTask()

	def ActiveState(self,AllocationSpace):
		while(True):
			#os.system('cls')
			AllocationSpace.GetData()		
			print ("[A].Add task\n")
			event=raw_input("")
			if(event=="A"):
				newT=None
				title=raw_input("enter task title\n")
				duration=input("enter duration\n")
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







