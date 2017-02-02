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
Initial Software for Data Classes , its structures and methods.

File created on January 29,2017.
Developed by TaskOverflow group.

This software serves as the primary Data Classes  of our 
Software Project (Task OverFlow).

'''

from __future__ import print_function

import heapq
import random


'''
class Task is a superclass. This describes the primary structure of a task.
Attrubutes involve title and duration.
'''
class Task():
	def __init__(self, title,duration):
		self.title=title #this variable describes the title of title task
		self.duration=duration 	#this variable describes the duration of the task


'''
class FixTask is a subclass of Task. FixTask is a task that cannot be moved.
Attributes involve title,duration,mustart and mustend
'''
class FixTask(Task):
	def __init__(self,title,duration,mustart,mustend):
		Task.__init__(self,title,duration) 	
		self.mustart=mustart 	#this variable indicates where the FixTask must start
		self.mustend=mustend 	#this variable indicates where the FixTask must end



'''
Class FlexibleTask is a subclass of Task. FlexibleTask is a task that can be deleted and partitioned.
Attributes involve title,priority,duration,lowerbound,and upperbound
'''
class FlexibleTask(Task):
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

	def __init__(self,name):
		'''this constructor initializes the class and sets the name; new space is created and initialized priorityQueue to be empty'''
		self.name=name #this variable describes the name of the AllocationSpace.
		self.space=[TimeBlock(0,2400,2400,None)] #this variable is a list of timeBlocks, but is initially has only one primary TimeBlock
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
		created January 29,2017	

		This method is the core Allocation Algorithm for flexible tasks. 
		It returns a boolean value True if the allocation is successful, otherwise False.
		The formal parameter tflex is of type FlexibleTask.
	'''
	def AllocateTime(self,tflex):
		print ("allocating",tflex.title,tflex.duration,tflex.lowerbound,tflex.upperbound)

		#saving current data...
		oldSpace=[] #this cariable is a list the saves the current space in case the Allocation fails and needs to be undone.
		print (self.space)

		for i in self.space:
			j=TimeBlock(i.startTime,i.endTime,i.span,i.status)
			oldSpace.append(j)
		if(self.space==oldSpace):
			print ("magkapareho")

		temp=oldSpace
		#search for possible TimeBlocks.
		startTB=self.SearchStartingTimeBlock(tflex) #this variable keeps track of the current TimeBlock while traversing the Allocation Space

		#search for timeblock that has lower priority.
		if(startTB==None):
			startTB=self.SearchStartingFlexibleTaskTimeBlock(tflex)
			if startTB==None:
				print ("task cannot be allocated")
				self.space=oldSpace
				return False

		#if startTB is not free, then locate for possible kicks.
		if(not startTB.isFree()):
			tasktokick=self.LocateKick(self.space.index(startTB),tflex) #this variable is a TimeBlocks that needs to be freed/tasks that needs to be kicked
			if(tasktokick==None):
				self.space=oldSpace				
				print ("task cannot be allocated")
				return False
			else:
				self.Kick(tasktokick)
				self.Merge()
				startTB=self.SearchStartingTimeBlock(tflex)	

		#if TimeBLock is enough, do possible splitting
		if(startTB.isEnough(tflex)):
			if(self.inTheMiddle(startTB,tflex)):
				startTB=self.splitAndReturnMiddle(startTB,tflex)
			elif(self.leftSided(startTB,tflex)):
				startTB=self.splitAndReturnLeft(startTB,tflex)
			elif(self.rightSided(startTB,tflex)):
				startTB=self.splitAndReturnRight(startTB,tflex)			
		timeRemaining=tflex.duration #this variable keeps tracks of the remainingTime while doeing the Allocation



		for i in oldSpace:
			print (i.status)

		#Allocate tasks.
		while(timeRemaining>0):
			print ("timeRemaining",timeRemaining)
			if(startTB==None):				
				startTB=self.SearchStartingFlexibleTaskTimeBlock(tflex)
				if(startTB==None):
					for i in oldSpace:
						print (i.status)
					self.space=oldSpace
					print ("cannot Allocate")
					return False
				else:
					tasktokick=self.LocateKick(self.space.index(startTB),tflex)
					if(tasktokick==None):
						self.space=oldSpace		
						print ("unable to allocate space for the given task")
						return False
					else:
						self.Kick(tasktokick)
						self.Merge()
						

			else:
				timeRemaining=self.AllocateMaxTime(self.space.index(startTB),tflex,timeRemaining)
				self.Merge()
				oldstartTb=startTB
				startTB=self.SearchStartingTimeBlock(tflex)


				if( startTB==None):
					self.space=oldSpace
					self.Merge()
					startTB=None

					self.Merge()
					#self.GetData()
					print ("task is not allocated")
					return False
				elif( startTB.startTime==oldstartTb.startTime):
					print (startTB.startTime)
					self.space=oldSpace
					self.Merge()
					startTB=None

					self.Merge()
					#self.GetData()
					print ("task is not allocated")
					return False					

			startTB=self.SearchStartingTimeBlock(tflex)

		print ("Task Allocated is a success")

		self.Merge()
		return True
	

	'''method AllocateTimeFix
		created January 29,2017	

		This method is the core Allocation Algorithm for fix tasks. 
		It returns a boolean value True if the allocation is successful, otherwise False.
		The formal parameter tfix is of type FixTask.
	'''
	def AllocateTimeFix(self,tfix):

		startTB=self.SearchStartingTimeBlock(tfix)
		if startTB!=None:
			if(startTB.isEnough(tfix)):
				if(self.inTheMiddle(startTB,tfix)):
					#print ("in the middle")
					tartTB=self.splitAndReturnMiddle(startTB,tfix)
				elif(self.leftSided(startTB,tfix)):
					#print ("left")				
					startTB=self.splitAndReturnLeft(startTB,tfix)
				elif(self.rightSided(startTB,tfix)):
					#print ("right")	
					startTB=self.splitAndReturnRight(startTB,tfix)			
		elif startTB==None:
			TBtokick=self.LocateKickFix(tfix)
			tasktokick=[] #this variable provides list for the TimeBLocks that needs to be freed and this variable is returned by this method
			totalspan=0  #this keeps tracks of the current free space generated while Kick method is happening

			if(TBtokick==None):
				print ("Unsuccessful Allocation")
				return False

			for i in TBtokick:
				totalspan+=i.span
				tasktokick.append(i.status.title)
			for i in self.space:
				if i.status!=None:
					if i.status.title in tasktokick:
						self.Kick(i.status)
				if i.status==None:
					totalspan+=i.span
			if(totalspan<tfix.duration):
				print ("not enough space, cannot be allocated")
				return False
			else:
				for i in self.space:
					#print ("im heres")
					if(isinstance(i.status,FlexibleTask)):
						if i.status.title in tasktokick:
							self.Kick(i.status)
			self.Merge()
			startTB=self.SearchStartingTimeBlock(tfix)

		if(startTB!=None):
			index=self.space.index(startTB)	
			self.space[index].status=tfix	
			self.Merge()

		print ("Allocation Successful.")
		return True
		#self.GetData()



	'''method SearchStartingTimeBlock
		created January 29,2017	

		This method is responsible in searcheing for possible Free TimeBlock 
		that is contained in the bounds in case of Flexible tasks,
		and a Free TimeBlock contained in the mustart and mustend of a fixed task. 
		It returns a value of type TimeBlock in case the search is successful, otherwise it returns None.
		The formal parameter  tflex is of type Task.
	'''
	def SearchStartingTimeBlock(self,tflex):
		if isinstance(tflex,FlexibleTask):
			for i in self.space:
				print (i.startTime)
				if(i.isFree() and i.startTime>=tflex.lowerbound and i.startTime<tflex.upperbound and i.span>=tflex.duration and tflex.upperbound-i.startTime>=tflex.duration):
					#self.GetData()
					return i				
				if (i.isFree() and  i.startTime>=tflex.lowerbound and i.startTime<=i.endTime):
					return i
				if (i.isFree() and  i.startTime>=tflex.lowerbound and i.startTime<i.endTime):
					return i					
				if (i.isFree() and  i.endTime>tflex.lowerbound and i.startTime<=i.endTime):
					return i										

			for i in self.space:
				if(i.isFree() and i.endTime>tflex.lowerbound and i.startTime<tflex.upperbound):
					return i
			return None
		elif isinstance(tflex,FixTask):
			for i in self.space:
				if(i.isFree() and i.endTime>=tflex.mustend and i.startTime<=tflex.mustart):
					return i
			return None


	'''method SearchStartingFlexibleTaskTimeBlock
		created January 29,2017	

		This method is responsible in searching for possible Free TimeBlock of status flexibleTask 
		that is contained in the bounds in of tflex. This method is used when SearchStartingTimeBlock method
		fails.
		It returns a value of type TimeBlock in case the search is successful, otherwise it returns None.
		The formal parameter is of tflex is of type FlexibleTask.
	'''
	def SearchStartingFlexibleTaskTimeBlock(self,tflex):
		for i in self.space:
			if(isinstance(i.status,FlexibleTask) and i.endTime>tflex.lowerbound and i.startTime<tflex.upperbound):
				if(i.status.priority>tflex.priority):
					return i

		return None


	'''method inTheMiddle
		created January 29,2017	

		This method checks if a task is contained between span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def inTheMiddle(self,startTB,tflex):

		if isinstance(tflex,FlexibleTask):
			if startTB.span>tflex.duration and tflex.lowerbound>startTB.startTime and startTB.endTime>tflex.lowerbound+tflex.duration:		
				return True
			else:
				return False
		elif isinstance(tflex,FixTask):
			if startTB.span>tflex.duration and startTB.startTime<tflex.mustart and startTB.endTime>tflex.mustend:		
				return True
			else:
				return False			


	'''method leftSided
		created January 29,2017	

		This method checks if a task is on the left side of the span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def leftSided(self,startTB,tflex):
		if isinstance(tflex,FlexibleTask):
			if startTB.span>tflex.duration and startTB.startTime==tflex.lowerbound and startTB.endTime>tflex.upperbound:		
				return True
			else:
				return False	
		elif isinstance(tflex,FixTask):
			if startTB.span>tflex.duration and startTB.startTime==tflex.mustart and startTB.endTime>tflex.mustend:		
				return True
			else:
				return False						
	

	'''method rightSided
		created January 29,2017	

		This method checks if a task is on the right side of the span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''
	def rightSided(self,startTB,tflex):
		if isinstance(tflex,FlexibleTask):		
			if startTB.span>tflex.duration and startTB.startTime<tflex.lowerbound and startTB.endTime==tflex.upperbound:		
				return True
			else:
				return False
		elif isinstance(tflex,FixTask):
			if startTB.span>tflex.duration and startTB.startTime<tflex.mustart and startTB.endTime==tflex.mustend:		
				return True
			else:
				return False						

	
	'''method exactlyFitted
		created January 29,2017	

		This method checks if a task exactly contained in the  span of a timeblock.
		It returns True if such condition is satisfied, Otherwise it returns false.
		Formal parameters are startTB and tflex of type TimeBlock and Task respectively.
	'''	
	def exactlyFitted(self,startTB,tflex):
		if startTB.span==tflex.duration and startTB.startTime==tflex.lowerbound and startTB.endTime==tflex.upperbound:		
			return True
		else:
			return False


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
		index=self.space.index(startTB)

		newTB1=TimeBlock(startTB.startTime,startTB.endTime-tflex.duration,startTB.endTime-tflex.duration,None) #this variable is the newly generated timeblock because of the split
		self.space[index].startTime=startTB.endTime-tflex.duration
		self.space[index].endTime=startTB.endTime
		self.space[index].span=startTB.endTime-startTB.endTime+tflex.duration
		self.space.insert(index,newTB1)

		return self.space[index+1]

	

	'''method AllocateMaxTime
		created January 29,2017	

		This method iteratively allocates the task in a free TimeBlock.
		This method return the remaining time at the end of the allocations.
		Formal parameters are counter,tflex and timeRemaining of type integer,FlexibleTask and integer.
	'''
	def AllocateMaxTime(self,counter,tflex,timeRemaining):

		pointer=counter
		timeRemaining=timeRemaining
		if pointer<0:
			return timeRemaining

		while(pointer<len(self.space)):
			if(timeRemaining<=0):
				'''check kung meron pa'''

				break

			if(self.space[pointer].startTime<tflex.lowerbound and self.space[pointer].endTime>tflex.upperbound):
				'''check kung pasok sa range'''

				break
			if(self.space[pointer].isFree() and self.space[pointer].span>timeRemaining):
				'''split into two blocks'''
				newTB=TimeBlock(self.space[pointer].startTime+timeRemaining,self.space[pointer].endTime,self.space[pointer].span-timeRemaining,None)
				self.space[pointer].endTime=newTB.startTime
				self.space[pointer].span=self.space[pointer].endTime-self.space[pointer].startTime
				self.space.insert(pointer+1,newTB)
				self.GetData()

			if (self.space[pointer].isFree() and self.space[pointer].startTime>=tflex.lowerbound and self.space[pointer].endTime<=tflex.upperbound):
				self.space[pointer].status=tflex
				timeRemaining-=self.space[pointer].span
			pointer+=1
		#print ("after allocation")
		#self.GetData()
		return timeRemaining



	'''method LocateKick
		created January 29,2017	

		This method is responsible for searching for TimeBlock with a flexibleTas status 
		given that there is no possible free TimeBlock for such task.
		The method returns a TimeBlock of the lowest priority within the task's bounds 
		but returns None once it does not find any TimeBlock that is a candidate to be kicked.
		Formal parameters are counter an integer, which describes the index of the current startTB
		and tflex of type FlexibleTask.
	'''
	def LocateKick(self,counter,tflex):
		if(counter<0):
			pointer=0
		else:
			pointer=counter
		minPriority=self.space[pointer] #this keeps tracks of the lowest priority in the PriorityQueue

		for i in self.space:
			if i.startTime >=tflex.lowerbound and i.startTime<tflex.upperbound:
				if(isinstance(i.status,FlexibleTask) and i.status.priority>minPriority.status.priority):
					minPriority=self.space[pointer]
		if(minPriority.status.priority>tflex.priority):
			return minPriority.status
		else:
			return None



	'''method LocateKickFix
		created January 29,2017	

		This method is a counter part of LocateKick but in this case, a fixTask must be allocated.
		This method searches for the list of TimeBlocks that needs to be kicked
		in order for the fixTask to be allocated.
		The method returns a list of TimeBlocks.
		Formal parameter is tfix of type FixTask.
	'''
	'''def LocateKickFix(self,tfix):
		tokick=[] #this variable is a list of tasks to be kicked.
		for i in self.space:
			if (isinstance(i.status,FlexibleTask)):


				if(i.startTime >= tfix.mustart and i.startTime<tfix.mustend):

					tokick.append(i)										
				elif(i.endTime <= tfix.mustend and i.endTime>tfix.mustart):
					tokick.append(i)
				elif(i.startTime<tfix.mustart and i.endTime>tfix.mustend) :
					tokick.append(i)
		for i in tokick:
			print (i.startTime)
		return tokick

	'''
	
		def LocateKickFix(self,tfix):
		tokick=[]
		pointer=None
		for i in range(0,len(self.space)):
			if (tfix.mustart>=self.space[i].startTime and self.space[i].endTime>tfix.mustart):
				pointer=i
				break
		while(self.space[pointer].startTime<tfix.mustend):
			if(isinstance(self.space[pointer].status,FlexibleTask)):
				tokick.append(self.space[pointer])
			elif(isinstance(self.space[pointer].status,FixTask)):
				return None
			pointer+=1

		return tokick


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
			if isinstance(i.status,FlexibleTask):
				if i.status.title==tobekicked.title:
					i.status=None


	def AllocateRemainingTime(self,counter,tflex,remainingTime):
		pass

	

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
				if(self.space[head].status.title==self.space[head+1].status.title):
					self.space[head].endTime=self.space[head+1].endTime
					self.space[head].span==self.space[head].endTime-self.space[head].startTime
					self.space.remove(self.space[head+1])
			head+=1


if __name__=="__main__":
	myAS=AllocationSpace("")
	#myAS.AllocateTime(FlexibleTask("A",800,1,0,800))
	myAS.AllocateTime(FlexibleTask("A",300,1,400,700))	
	myAS.AllocateTimeFix(FixTask("B",100,700,800))
	myAS.AllocateTimeFix(FixTask("C",200,600,800))	
	for i in myAS.priorityQueue:
		if(myAS.AllocateTime(i[1])==True):
			print ("true")
			myAS.priorityQueue.pop()
	myAS.GetData()	
	#myAS.AllocateTime(FlexibleTask("B",100,1,1000,1100))		##
	#pass
