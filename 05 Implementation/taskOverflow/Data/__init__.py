'''
MIT License

Copyright (c) 2017 Gerry P. Agluba Jr, Robelle Silverio.

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
Robelle Silverio
last updated on Febbruary 16,2017
Initial Software for Data Classes , its structures and methods.

Robelle Silverio
edited Get data method

File created on January 29,2017.
Developed by TaskOverflow group.

This software serves as the primary Data Classes  of our 
Software Project (Task OverFlow).

'''

from __future__ import print_function

import heapq
import random
import os
import math
'''
For all Classes, no files or database tables had been used.
module from python like heapq and random had been imported.
Python module, and system model was also imported
'''


'''
class Task is a superclass. This describes the primary structure of a task.
Attrubutes involve title and duration.
'''
class Task():
	'''	method  __init__
		created January 29,2017

		This method initializes an object of class Task.
		__init__ methods return None.
		This method have paramaters title and duration of types string and int respectively.
	'''
	def __init__(self, title,duration):
		self.title=title #this variable describes the title of title task
		self.duration=duration 	#this variable describes the duration of the task


'''
class FixTask is a subclass of Task. FixTask is a task that cannot be moved.
Attributes involve title,duration,mustart and mustend
'''
class FixTask(Task):
	'''	method  __init__
		created January 29,2017

		This method initializes an object of class FixTask.
		__init__ methods return None.
		This method have paramaters title,duration,muststart,mustend of types string and ints respectively.
	'''
	def __init__(self,title,duration,mustart,mustend):
		Task.__init__(self,title,duration) 	
		self.mustart=mustart 	#this variable indicates where the FixTask must start
		self.mustend=mustend 	#this variable indicates where the FixTask must end



'''
Class FlexibleTask is a subclass of Task. FlexibleTask is a task that can be deleted and partitioned.
Attributes involve title,priority,duration,lowerbound,and upperbound
'''
class FlexibleTask(Task):
	'''	method  __init__
		created January 29,2017

		This method initializes an object of class FlexibleTask.
		__init__ methods return None.
		This method have paramaters title,duration,priority,lowerbound,upperbound of types string and ints respectively.
	'''
	def __init__(self,title,duration,priority,lowerbound,upperbound):
		Task.__init__(self,title,duration)
		self.priority=priority 	#this variable indicates the priority of a flexible Task, lower value means higher priority
		self.lowerbound=lowerbound #this variable indicates the upper allowance when a flexible task must at least start
		self.upperbound=upperbound #this variable indicates the lower allowance when a flexible task must at most end


'''
Class TimeBlock is a block of time where tasks are allocated.
Attributes involve startTime,endTime,span and status.
Methods are isFree and isEnoudh
'''
class TimeBlock():
	'''	method  __init__
		created January 29,2017

		This method initializes an object of class TimeBlock.
		__init__ methods return None.
		This method have paramaters startTime,endTime,span,status of types ints for the first three parameters 
		and Task type for the last parameter.
	'''
	def __init__(self,startTime,endTime,span,status):
		self.startTime=startTime #this variable describes TimeBlock's initial time
		self.endTime=endTime #this variable describes TimeBlock's end time
		self.span=span #this variable describes the timespan or the space of the block
		self.status=status #this variable describes if the timeBlock is allocated to a fix task, flexible task or None.


	'''	
		method  isFree
		created January 29,2017

		This method is a method of the TimeBlock class.
		It returns a boolen value. It returns True if a Timeblock's status is  None.Otherwise, it returns false. 
		This method has no paramater aside from the Timeblock itself.
	'''
	def isFree(self):
		if self.status==None:
			return True
		else:
			return False


	'''	
		method  isEnough
		created January 29,2017

		This method is a method of the TimeBlock class.
		It returns a boolen value. It returns True if a the TimeBlock's span is enough for a Task type parameter.
		it returns false otherwise.
		This method has paramater newTask of type Task.
	'''
	def isEnough(self,newTask):
		if(self.span>=newTask.duration):
			return True
		else:
			return False

	
'''
Class AllocationSpace is the backbound embodying all the timeblocks,tasks and priorityQueues involved in Alloation.
Primary attribute is name.
Methods are getData,AllocateTime,AllocateTimeFix,SearchStartingTimeBlock,SearchStartingFlexibleTaskTimeBlock,
inTheMiddle,LeftSided,RightSided,exactlyFitted,spltAndReturnMiddle,splitAndReturnLedt,splitAndReturnRight,
AllocateMaxTime,LocateKick,LocateKickFix,Kick and Merge
'''
class AllocationSpace():

	'''	method  __init__
		created January 29,2017

		This method initializes an object of class AllocationSpace.
		__init__ methods return None.
		This method have paramaters string name.
	'''
	def __init__(self,name):
		'''this constructor initializes the class and sets the name; new space is created and initialized priorityQueue to be empty'''
		self.name=name #this variable describes the name of the AllocationSpace.
		self.space=[TimeBlock(0,2400,2400,None)] #this variable is a list of timeBlocks, but is initially has only one primary TimeBlock
		#self space should load the file
		self.priorityQueue=[] #this variable is a list of task that is kicked throughout the Allocation, it is sorted according to priority
		self.maxPriority=None #this variable indicates the current highest priority in the current space.



	'''	
		method  getData
		created January 29,2017

		This method is a method of the AllocationSpace class.
		It does not return anything, but it is responsible for displaying data involved in the class AllocationSpace.
		The formal parameter name is of type String
	'''
	def GetData(self):
		for i in self.space:
			startTime=i.startTime-(i.startTime%100)+(i.startTime%100)*(60.0/100) #this variable is a recomputed startTime for data output purposes
			endTime=i.endTime-(i.endTime%100)+(i.endTime%100)*(60.0/100) #this variable is a recomputed endTime for data output purposes
			#span= (int(i.span/100)*100+(i.span%100)*(60.0/100))
			i.span=math.ceil(i.span)
			span=i.span-(i.span%100)+(i.span%100)*(60.0/100) #this variable is a recomputed span for data output purposes	
			
			print ("\n",int(startTime),"\t",int(endTime),"\t",int(span),end="\t")
			if isinstance(i.status,FlexibleTask):
				print (i.status.title,i.status.priority)
			elif isinstance(i.status,FixTask):	
				print (i.status.title)	
			else:
				print ("___________")							
		print ("\nPriorityQueue\t ")
		for i  in self.priorityQueue:
			print (i[1].title,"\t",i[1].priority)
		print ("\n")


	'''method AllocateTime
		created February 8,2017	

		This method is the core Allocation Algorithm for a given task. 
		It returns a boolean value True if the allocation is successful, otherwise False.
		The formal parameter is task of type Task, and an optional boolen parameter Partition.
		This paramter is initialized to be False, and this gives information if
		a user wants to partition its task.
	'''
	def AllocateTime(self,task,Partition=False):
		print ("allocating",task.title)

		oldSpace=[] #this variable is a list the saves the current space in case the Allocation fails and needs to be undone.
		#print (self.space)

		for i in self.space:
			j=TimeBlock(i.startTime,i.endTime,i.span,i.status)
			oldSpace.append(j)


		if(isinstance(task,FixTask)):
			TB=self.SearchFreeTimeBlockFix(task)
			if TB!=None:
				TB.status=task
				self.Merge()
				print ("Allocation Successful.")
				return True
			else:
				tobekicked=self.LocateKickFix(task)
				if len(tobekicked)==0:
					print ("Allocation UnSuccessful.")
					return False
				else:
					for i in tobekicked:
						self.Kick(i)

					self.Merge()
					TB=self.SearchFreeTimeBlockFix(task)
					TB.status=task
					print ("Allocation Successful.")
					return True				

		elif (isinstance(task,FlexibleTask)):
			TB=self.SearchFreeTimeBlockFlex(task)
			if TB!=None:
				TB.status=task
				self.Merge()
				print ("Allocation Successful")
				return True
			else:
				print (Partition)
				if Partition==False:
					self.Merge()
					print ("Allocation Unsuccessful")
					return False
		
				else:
					print ("proceeding to partinioning")
					self.Partition(task)



	'''method SeachFreeTimeBlockFix
		created January 29,2017	

		This method basically searches for free blocks if a given task to be added is fix.
		Searchinf free timeblocks is different for each type of task. (see method, searchFreeTimeBlockFlex).
		It returns a free block enough for a fixtask to be allocated.
		The formal parameter is task of type FixTask.
	'''
	def SearchFreeTimeBlockFix(self,task):
		'''
			for all blocks, check if it overlaps wit task's time range. it check if it is enough
			and performs necesarry splitting.
		'''
		for i in self.space:
			if (i.isFree() and i.startTime<=task.mustart and i.endTime>=task.mustend):
				if i.isEnough(task):
					if self.exactlyFitted(i,task):
						return i
					elif self.inTheMiddle(i,task):
						TB=self.splitAndReturnMiddle(i,task)
						return TB
					elif self.leftSided(i,task):
						TB=self.splitAndReturnLeft(i,task)
						return TB					
					elif self.rightSided(i,task):
						TB=self.splitAndReturnRight(i,task)
						return TB
		return None
	
	
	'''method SeachFreeTimeBlockFlex
		created January 29,2017	

		This method basically searches for free blocks if a given task to be added is flexible.
		It returns a free block enough for a fixtask to be allocated.
		The formal parameter is task of type FlexibleTask.
	'''
	def SearchFreeTimeBlockFlex(self,task):
		'''start with checking if the bounds are in the middle of a Free Block
		if it is, temporarily split it because we have to cut overlaps for searching precision
		then split necessary splitting.
		'''
		startPointer=0
		endPointer=1
		for i in self.space:
			if i.isFree():
				if task.lowerbound>i.startTime and task.lowerbound<i.endTime:
					#split 
					newTB=TimeBlock(task.lowerbound,i.endTime,i.endTime-task.lowerbound,None)
					i.endTime=newTB.startTime
					i.span=i.endTime-i.startTime
					self.space.insert(self.space.index(i)+1,newTB)
				if task.upperbound>i.startTime and task.upperbound<i.endTime:
					#split
					newTB=TimeBlock(task.upperbound,i.endTime,i.endTime-task.lowerbound,None)
					i.endTime=newTB.startTime
					i.span=i.endTime-i.startTime
					self.space.insert(self.space.index(i)+1,newTB)

		for i in  self.space:

			if i.isFree() and (i.startTime>=task.lowerbound) and (i.startTime<task.upperbound):
				if i.isEnough(task):
					#check kung exactlyFitted,lefside
					if self.exactlyFitted(i,task):
						return i
					elif self.leftSided(i,task):
						TB=self.splitAndReturnLeft(i,task)
						return TB										
		return None

	'''method inTheMiddle
		created January 29,2017	

		This method checks if a task is contained exactly in the span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are TB and t of type TimeBlock and Task respectively.
	'''
	def exactlyFitted(self,TB,t):
		if isinstance(t,FlexibleTask):
			if t.duration==TB.span:
				return True
			else:
				return False
		elif isinstance(t,FixTask):
			if t.mustart==TB.startTime and t.mustend==TB.endTime:		
				return True
			else:
				return False			


	'''method inTheMiddle
		created January 29,2017	

		This method checks if a task is contained between span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are TB and t of type TimeBlock and Task respectively.
	'''
	def inTheMiddle(self,TB,t):

		if isinstance(t,FlexibleTask):
			if t.lowerbound>TB.startTime and t.lowerbound+t.duration<TB.endTime:	
				return True
			else:
				return False
		elif isinstance(t,FixTask):
			if t.mustart>TB.startTime and t.mustend<TB.endTime:		
				return True
			else:
				return False			


	'''method leftSided
		created January 29,2017	

		This method checks if a task is on the left side of the span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def leftSided(self,TB,t):
		if isinstance(t,FlexibleTask):
			if TB.span>t.duration:
				return True
			else:
				return False
		elif isinstance(t,FixTask):
			if t.mustart==TB.startTime and t.mustend<TB.endTime:		
				return True
			else:
				return False			
	

	'''method rightSided
		created January 29,2017	

		This method checks if a task is on the right side of the span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def rightSided(self,TB,t):
		if isinstance(t,FlexibleTask):
			if t.lowerbound==TB.startTime and t.lowerbound+t.duration<TB.endTime:	
				return True
			else:
				return False
		elif isinstance(t,FixTask):
			if t.mustart>TB.startTime and t.mustend==TB.endTime:		
				return True
			else:
				return False			
	
	'''method exactlyFitted
		created January 29,2017	

		This method checks if a task exactly contained in the  span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''	



	'''method spltAndReturnMiddle
		created January 29,2017	

		This method splits a specified TimeBlock into three sub TimeBlocks.
		This is usually called when the method inTheMiddle returns True.
		The middle sublock is then returned.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def splitAndReturnMiddle(self,startTB,tflex):
		index=self.space.index(startTB)
		

		if (isinstance(tflex,FlexibleTask)):
			newTB1=TimeBlock(startTB.startTime,tflex.lowerbound,tflex.lowerbound-startTB.startTime,None) #this variable is the newly generated timeblock because of the split
		elif isinstance(tflex,FixTask):
			newTB1=TimeBlock(startTB.startTime,tflex.mustart,tflex.mustart-startTB.startTime,None) #this variable is the newly generated timeblock because of the split

		newTB2=TimeBlock(newTB1.endTime+tflex.duration,startTB.endTime,startTB.endTime-newTB1.endTime-tflex.duration,None) #this variable is the newly generated timeblock because of the split
		
		self.space[index].startTime=newTB1.endTime
		self.space[index].endTime=newTB2.startTime	
		self.space[index].span=newTB2.startTime-newTB1.endTime

		self.space.insert(index,newTB1)
		self.space.insert(index+2,newTB2)


		return self.space[index+1]
	

	'''method spltAndReturnLeft
		created January 29,2017	

		This method splits a specified TimeBlock into two sub TimeBlocks.
		This is usually called when the method leftSided returns True.
		The left sublock is then returned.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def splitAndReturnLeft(self,startTB,tflex):
		index=self.space.index(startTB)

		newTB1=TimeBlock(startTB.startTime+tflex.duration,startTB.endTime,startTB.endTime-startTB.startTime-tflex.duration,None) #this variable is the newly generated timeblock because of the split
		self.space[index].startTime=startTB.startTime
		self.space[index].endTime=newTB1.startTime
		self.space[index].span=newTB1.startTime-startTB.startTime
		self.space.insert(index+1,newTB1)

		return self.space[index]


	'''method splitAndReturnRight
		created January 29,2017	

		This method splits a specified TimeBlock into two sub TimeBlocks.
		This is usually called when the method rightSided returns True.
		The right sublock is then returned.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def splitAndReturnRight(self,startTB,tflex):
		#print ("im here")
		index=self.space.index(startTB)

		newTB1=TimeBlock(startTB.startTime,startTB.endTime-tflex.duration,startTB.endTime-tflex.duration-startTB.startTime,None) #this variable is the newly generated timeblock because of the split
		self.space[index].startTime=startTB.endTime-tflex.duration
		self.space[index].endTime=startTB.endTime
		#print (self.space[index].startTime,self.space[index].endTime)
		self.space[index].span=self.space[index].endTime-self.space[index].startTime
		self.space.insert(index,newTB1)

		return self.space[index+1]


	'''method LocateKick
		created January 29,2017	

		This method is responsible for searching for TimeBlock with a flexibleTas status 
		given that there is no possible free TimeBlock for such task.
		The method returns a TimeBlock of the lowest priority within the task's bounds 
		but returns None once it does not find any TimeBlock that is a candidate to be kicked.
		Formal parameters are counter an integer, which describes the index of the current startTB
		and tflex of type FlexibleTask.
	'''
	def LocateKickFlexible(self,task,timeRemaining):
		#take note of the lowest prioruty
		tokick=[]
		sortedList=[]
		tR=timeRemaining
		for i in self.space:
			if(i.endTime>task.lowerbound and i.endTime<=task.upperbound) or (i.startTime>=task.lowerbound and i.startTime<task.upperbound):
				if isinstance(i.status,FlexibleTask):
					if i.status.priority>task.priority:
						heapq.heappush(sortedList,(i.status.priority,i))

		for i in sortedList:
			if tR<=0:
				break
			else:
				tokick.append(i[1])
				print (tR)
				print ("span",i[1].span)
				tR-=i[1].span
		if(int(tR)>0):
			return []
		else:
			return (tokick,tR)


	'''method LocateKickFix
		created January 29,2017	

		This method is a counter part of LocateKick but in this case, a fixTask must be allocated.
		This method searches for the list of TimeBlocks that needs to be kicked
		in order for the fixTask to be allocated.
		The method returns a list of TimeBlocks.
		Formal parameter is tfix of type FixTask.
	'''
	def LocateKickFix(self,task):
		tokick=[]
		startingPoint=None
		endPoint=None
		for i in self.space:
			print (i.startTime,i.endTime)
			if i.startTime >=task.mustart and i.startTime<task.mustend:

				if isinstance(i.status,FlexibleTask):
					print ("to kicked",i.startTime)	

					tokick.append(i.status)
					if startingPoint==None:
						startingPoint=i.startTime

					endPoint=i.endTime
				if i.isFree():
					endPoint=i.endTime
				if isinstance(i.status,FixTask):
					return []
			elif i.endTime >task.mustart and i.endTime<=task.mustend:
				if isinstance(i.status,FixTask):
					return []
				if isinstance(i.status,FlexibleTask):
					tokick.append(i.status)
					if startingPoint==None:
						startingPoint=i.startTime

					endPoint=i.endTime
				if i.isFree():
					endPoint=i.endTime				

		if startingPoint==None or endPoint==None:
			return []
		if endPoint - startingPoint >= task.duration:
			return tokick
		else:
			return []

	'''method Kick
		created January 29,2017	

		This method is responsible for kicking tasks in a TimeBlock. 
		Information about this task is then push to a heap that is needed for resheduling.
		The method does not return anything.
		Formal parameter is tobekicked of type FlexibleTask.
	'''
	def Kick(self,tobekicked):

		heapq.heappush(self.priorityQueue,(tobekicked.priority,tobekicked)) #heapq is a method from one of the modules of python
		for i in self.space:
			if (isinstance(i.status,FlexibleTask)):
				if id(i.status)==id(tobekicked):
					i.status=None
	

	'''method Merge
		created January 29,2017	

		This method is responsible for merging consecutive free TimeBlocks and 
		merging consecutive blocks with the same status.
		Merging is necessary because the Allocation Algorithm involves partitioning and spliting of TimeBLocks. 
		The method does not return anything.
		This method doent have any parameters.
	'''
	def Merge(self):

		self.space.insert(0,TimeBlock(0,0,0,(FixTask("temp",0,0,0))))
		self.space.append(TimeBlock(2400,0,0,(FixTask("temp",0,0,0))))
		head=tail=0 #this variable is a pointer to the space, this will specify which timeblocks must be merged.
		while(head<len(self.space)):
			if self.space[head].isFree():
				pass
			elif not self.space[head].isFree():
				if head>tail+2:
					for i in range(tail+1,head):
						self.space.remove(self.space[tail+1])
					head=tail+1
					newTB=TimeBlock(self.space[tail].endTime,self.space[head].startTime,self.space[head].startTime-self.space[tail].endTime,None)
					self.space.insert(tail+1,newTB)
					tail=head
				else:
					tail=head
			head+=1
		head=tail=0
		self.space.remove(self.space[0])
		self.space.pop()

		while(head<len(self.space)-1):
			if (isinstance(self.space[head].status,FlexibleTask) and isinstance(self.space[head+1].status,FlexibleTask)):
				if(id(self.space[head].status)==id(self.space[head+1].status)):
					self.space[head].endTime=self.space[head+1].endTime
					self.space[head].span=self.space[head].endTime-self.space[head].startTime
					self.space.remove(self.space[head+1])
			head+=1


	'''method Load
		created February 08,2017	

		This method is the main function for loading data from our files.
		It parses the file input so that it matches the current state of the AllocationSpace.
		This method has formal parameter filename of type string.
	'''
	def Load(self,filename):
		f=open(filename,'r')
			#check if the file is empty
		if os.path.getsize(filename) > 0:
			self.name = f.readline()
			f.readline()
			taskList=[]
			#taskList.append(None)
			numTask=int(f.readline())
			f.readline()
			for i in range(0,numTask-1):
				t=f.readline()
				t = t[1:-2]
				t=t.split(',')
				t[0]=int(t[0])
				t[1]=t[1].strip("'")
				t[1]=t[1].strip(" '")
				t[2]=t[2].strip("'")
				t[2]=t[2].strip(" '")	
				t[3]=float(t[3])			
				t[4]=float(t[4])			
				t[5]=float(t[5])	
				if(t[1]=='fix'):
					nt=FixTask(t[2],t[3],t[4],t[5])
				elif(t[1]=='flexible'):
					t[6]=float(t[6])
					nt=FlexibleTask(t[2],t[3],t[4],t[5],t[6])

				taskList.append((nt,t[0]))

			print (taskList)
			numTB=int(f.readline())
			self.space=[]
			for i in range(0,numTB):
				tb=f.readline()
				tb = tb[1:-2]
				tb=tb.split(',')
				tb[0]=float(tb[0])
				tb[1]=float(tb[1])
				tb[2]=float(tb[2])
				tb[3]=tb[3].strip("'")
				tb[3]=tb[3].strip(" '")	
				if (tb[3]!='None'):
					tb[4]=int(tb[4])
					nTB=TimeBlock(tb[0],tb[1],tb[2],None)
					for i in taskList:
						if i[1]==tb[4]:
							nTB.status=i[0]
							self.space.append(nTB)
				else:
					nTB=TimeBlock(tb[0],tb[1],tb[2],None)
					self.space.append(nTB)
			self.GetData()

		else:
			"print file is empty"
		f.close()


	'''method Save
		created February 08,2017	

		This method is the main function for saving data into our files.
		The method functions by first saving all infomration about all the tasks.
		It involves adding some refrenceNumber in order for the method Load 
		to properly identify which task is contained in a specific TimeBlock.
		Morover, it saves informations about the AllocationSpace, the timeblocks. etc.
		This method has formal parameter filename of type string.
	'''
	def Save(self,filename):
		f=open(filename,"w")
		f.write(self.name+"\n")
		#save task info
		x={None}
		for i in self.space:
			if i.status!=None:
				if isinstance(i.status,FixTask):
					x.add((id(i.status),"fix",i.status.title,i.status.duration,i.status.mustart,i.status.mustend))
					#print i.status.title
				elif isinstance(i.status,FlexibleTask):
					x.add((id(i.status),"flexible",i.status.title,i.status.duration,i.status.priority,i.status.lowerbound,i.status.upperbound))				

			else:
				x.add(None)
		f.write(str(len(x))+"\n")
		#save 
		for i in x:

			if i==None:
				f.write(str(None))
			else:
				f.write(str(i))
			f.write("\n")

		#for in Timeblock

		#save TimeBlocks info
		f.write(str(len(self.space))+"\n")
		for i in self.space:
			if i.status==None:
				f.write(str((i.startTime,i.endTime,i.span,i.status)))
			elif isinstance(i.status,FixTask):
				f.write(str((i.startTime,i.endTime,i.span,"Fix",id(i.status))))
			elif isinstance(i.status,FlexibleTask):
				f.write(str((i.startTime,i.endTime,i.span,"Flexible",id(i.status))))				
			f.write("\n")
		
		'''f.write(str(len(self.priorityQueue))+"\n")	
		for i in self.priorityQueue:
			f.write(str((i[1].title,i[1].duration,i[1].priority,i[1].lowerbound,i[1].upperbound)))
		f.close()''' #I COMMENTED THIS BECAUSE THERE'S NO NEED TO SAVE THE PRIORITYQUEUE



	'''method Partition
		created February 08,2017	

		This method, basically partition a task into multiple timeblocks if in case,
		if there is not anough space in the bounds of the task(note: partition is only available for flexible task)
		First it searches and take notes of the the free space withing the bounds.
		If the space is enough., then allocation follows. If not,
		kicking of flexible priorities is enforced. Kicking is ended, if such space 
		is generated and allocation follows. If in case kicking fails, or generated
		space is still not enough, then Allocation is aborted. and state of the AllocationSpace
		is redone.

		This medthod returns False if partitioning fails.
		Formal parameters is task of type FlexibleTask. 
	'''
	def Partition(self,task):
		print ("partitioning...")
		freeSpace=[]
		generatedSpace=0

		for i in self.space:
			if i.startTime>=task.lowerbound and i.endTime<=task.upperbound:
				if i.isFree():
					if(generatedSpace>=task.duration):
						break
					print (i.startTime,i.endTime,i.span)
					freeSpace.append(i)
					generatedSpace+=i.span

		if(generatedSpace>task.duration):
			#split yung last na in-add mo
			newTB=TimeBlock(freeSpace[-1].endTime-(generatedSpace-task.duration),freeSpace[-1].endTime,generatedSpace-task.duration,None)
			index=self.space.index(freeSpace[-1])
			self.space[index].endTime=newTB.startTimes
			self.space[index].span=(self.space[index].endTime-self.space[index].startTime)

			self.space.insert(index+1,newTB)
		self.GetData()



		print ("generateSpace/taskduration",generatedSpace,float(task.duration))
		if(abs(generatedSpace-task.duration)<=1):#hindi gumagana yung comparision lang, kaya naglagay ako ng degree of error
			for i in self.space:
				if i in freeSpace:
					i.status=task
			print ("Allocation Successful")
		else:
			print ("kicking lower priorities")
			timeRemaining=task.duration-generatedSpace
			toKickTimeRemainingTuple=self.LocateKickFlexible(task,timeRemaining)

			if (toKickTimeRemainingTuple==[]): #list is empty 
				self.Merge()
				print ("Allocation Unsuccessful")
				return False

			if toKickTimeRemainingTuple[1]>0:
				self.Merge()
				print ("Allocation Unsuccessful")
				return False

			for i in toKickTimeRemainingTuple[0]:
				self.Kick(i.status)				
				freeSpace.append(i)

			self.GetData()

			if (toKickTimeRemainingTuple[1]-0<1):
				print ("splitting excess")
				excess=int(-toKickTimeRemainingTuple[1])
				for i in freeSpace:
					print (i.span,excess)

					if i.span>excess:
						#split

						newTB=TimeBlock(i.endTime-excess,i.endTime,excess,None)
						index=self.space.index(i)
						self.space[index].endTime=newTB.startTime
						self.space[index].span=self.space[index].endTime-self.space[index].startTime
						self.space.insert(index+1,newTB)

				self.GetData()



			for i in freeSpace:
				i.status=task
			for i in toKickTimeRemainingTuple[0]:
				i.status=task


		self.Merge()
		

	'''method Clear
		created February 08,2017
		This method clear the whole AllocationSpace.
		This wil be refected to the file, because saving is done.
	'''
	def Clear(self):
		self.space=[TimeBlock(0,2400,2400,None)] #this variable is a list of timeBlocks, but is initially has only one primary TimeBlock
		#self space should load the file
		self.priorityQueue=[] #this variable is a list of task that is kicked throughout the Allocation, it is sorted according to priority
		self.maxPriority=None #this variable indicates the current highest priority in the current space.
		print ("saving...")
		self.Save("Data\DataFiles\myData.in")


	'''this method will delete user's selected task
		arguemnts are:
		self- the object AllocationSpace
		tasky- task to be deleted
		TimeBlock- the object TimeBlock
		
		this method returns nothing
	'''
	def Dela(self,tasky):
		check=0
		for i in self.space:
			if isinstance(i.status,FixTask):
				if (i.status.title==tasky):
					i.status=None
					check=1
			elif isinstance(i.status,FlexibleTask):
				if isinstance(i.status,FlexibleTask):
					if (i.status.title==tasky):
						i.status=None
						check=1
		if check==0:
			print ("Task is not in the schedule")
		self.Merge()
		print ("saving...")
		self.Save("Data\DataFiles\myData.in")
			
if __name__=="__main__":
	pass
