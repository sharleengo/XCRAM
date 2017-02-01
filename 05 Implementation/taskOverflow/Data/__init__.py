'''
	Gerry Agluba Jr.
	This is a course requirement for CS192 Software Engineering II
	under the supervision of Asst. Prof. Ma.Rowena C. Solamo 
	of the Department of Computer Science, College of Engineering,
	University of the Philippines, Diliman for the AY 2016-2017

	Gerry Agluba Jr.
	last updated on January 31,2017
	Initial Software for Data Classes , its structures and methods.

	File created on January 29,2017
	Developed by TaskOverflow group

	This software serves as the primary Data Classes  of our 
	Software Project (Task OverFlow).

'''

from __future__ import print_function

import heapq
import random

class Task():
	def __init__(self, title,duration):
		self.title=title
		self.duration=duration

	'''method  __init__
		created on January 29,2017
		
	'''

class FixTask(Task):
	def __init__(self,title,duration,mustart,mustend):
		Task.__init__(self,title,duration)
		self.mustart=mustart
		self.mustend=mustend

class FlexibleTask(Task):
	def __init__(self,title,duration,priority,lowerbound,upperbound):
		Task.__init__(self,title,duration)
		self.priority=priority
		self.lowerbound=lowerbound
		self.upperbound=upperbound

class TimeBlock():
	def __init__(self,startTime,endTime,span,status):
		self.startTime=startTime
		self.endTime=endTime
		self.span=span
		self.status=status
	def isFree(self):
		if self.status==None:
			return True
		else:
			return False
	def isEnough(self,newTask):
		if(self.span>=newTask.duration):
			return True
		else:
			return False


class AllocationSpace():

	def __init__(self,name):
		'''this constructor initializes the class and sets the name; new space is created and initialized priorityQueue to be empty'''
		self.name=name
		self.space=[TimeBlock(0,2400,2400,None)]
		self.priorityQueue=[]
		self.maxPriority=None


	def GetData(self):
		for i in self.space:
			startTime=i.startTime-(i.startTime%100)+(i.startTime%100)*(60.0/100)
			endTime=i.endTime-(i.endTime%100)+(i.endTime%100)*(60.0/100)
			span=i.span-(i.span%100)+(i.span%100)*(60.0/100)		
			#i.spa
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


	def AllocateTime(self,tflex):
		print ("allocating",tflex.title,tflex.duration,tflex.lowerbound,tflex.upperbound)

		'''temp=self.space
		oldSpace=temp
		oldSpace=[]


		for i in range(0,len(temp)):
			tempTB=temp[i]
			oldTB=tempTB
			oldSpace.append(oldTB)'''
		#tempSpace=self.space

		#self.GetData()
		#tempSpace=self.space
		#oldSpace=tempSpace
		oldSpace=[]
		print (self.space)
		for i in self.space:
			j=TimeBlock(i.startTime,i.endTime,i.span,i.status)
			oldSpace.append(j)
		if(self.space==oldSpace):
			print ("magkapareho")

		#save
		startTB=self.SearchStartingTimeBlock(tflex)



		if(startTB==None):
			startTB=self.SearchStartingFlexibleTaskTimeBlock(tflex)
			if startTB==None:
				print ("task cannot be allocated")
				self.space=oldSpace
				return False

		if(not startTB.isFree()):
			tasktokick=self.LocateKick(self.space.index(startTB),tflex)
			if(tasktokick==None):
				self.space=oldSpace				
				print ("task cannot be allocated")
				return False
			else:
				self.Kick(tasktokick)
				self.Merge()
				startTB=self.SearchStartingTimeBlock(tflex)	

		if(startTB.isEnough(tflex)):
			if(self.inTheMiddle(startTB,tflex)):
				startTB=self.splitAndReturnMiddle(startTB,tflex)
			elif(self.leftSided(startTB,tflex)):
				startTB=self.splitAndReturnLeft(startTB,tflex)
			elif(self.rightSided(startTB,tflex)):
				startTB=self.splitAndReturnRight(startTB,tflex)			
		timeRemaining=tflex.duration


		for i in oldSpace:
			print (i.status)
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
				print ("im here",startTB.startTime,startTB.endTime)
				timeRemaining=self.AllocateMaxTime(self.space.index(startTB),tflex,timeRemaining)
				print ("adad")

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
	def AllocateTimeFix(self,tfix):
		startTB=self.SearchStartingTimeBlock(tfix)
		if startTB!=None:
			if(startTB.isEnough(tfix)):
				if(self.inTheMiddle(startTB,tfix)):
					print ("in the middle")
					tartTB=self.splitAndReturnMiddle(startTB,tfix)
				elif(self.leftSided(startTB,tfix)):
					print ("left")				
					startTB=self.splitAndReturnLeft(startTB,tfix)
					#print (startTB.startTime,startTB.endTime)
				elif(self.rightSided(startTB,tfix)):
					print ("right")	
					startTB=self.splitAndReturnRight(startTB,tfix)			
		elif startTB==None:
			print ("None")
			TBtokick=self.LocateKickFix(tfix)
			tasktokick=[]
			totalspan=0

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
				return 
			else:
				for i in self.space:
					#print ("im heres")
					if(isinstance(i.status,FlexibleTask)):
						if i.status.title in tasktokick:
							self.Kick(i.status)
			self.Merge()
			startTB=self.SearchStartingTimeBlock(tfix)
			#print (startTB.startTime)

			'''if(self.inTheMiddle(startTB,tfix)):
				tartTB=self.splitAndReturnMiddle(startTB,tfix)
			elif(self.leftSided(startTB,tfix)):
				startTB=self.splitAndReturnLeft(startTB,tfix)
			elif(self.rightSided(startTB,tfix)):
				startTB=self.splitAndReturnRight(startTB,tfix)			'''
		if(startTB!=None):
			index=self.space.index(startTB)	
			self.space[index].status=tfix	
			self.Merge()
		#self.GetData()

	def SearchStartingTimeBlock(self,tflex):
		if isinstance(tflex,FlexibleTask):
			for i in self.space:
				print (i.startTime)
				if(i.isFree() and i.startTime>=tflex.lowerbound and i.startTime<tflex.upperbound and i.span>=tflex.duration and tflex.upperbound-i.startTime>=tflex.duration):
					#self.GetData()
					print ("dasdasdasd",i.startTime,i.endTime)
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

	def SearchStartingFlexibleTaskTimeBlock(self,tflex):
		for i in self.space:
			if(isinstance(i.status,FlexibleTask) and i.endTime>tflex.lowerbound and i.startTime<tflex.upperbound):
				if(i.status.priority>tflex.priority):
					return i

		return None
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

	
	def exactlyFitted(self,startTB,tflex):
		if startTB.span==tflex.duration and startTB.startTime==tflex.lowerbound and startTB.endTime==tflex.upperbound:		
			return True
		else:
			return False

	def splitAndReturnMiddle(self,startTB,tflex):
		index=self.space.index(startTB)
		

		if (isinstance(tflex,FlexibleTask)):
			newTB1=TimeBlock(startTB.startTime,tflex.lowerbound,tflex.lowerbound-startTB.startTime,None)
		elif isinstance(tflex,FixTask):
			newTB1=TimeBlock(startTB.startTime,tflex.mustart,tflex.mustart-startTB.startTime,None)

		newTB2=TimeBlock(newTB1.endTime+tflex.duration,startTB.endTime,startTB.endTime-newTB1.endTime-tflex.duration,None)
		
		self.space[index].startTime=newTB1.endTime
		self.space[index].endTime=newTB2.startTime	
		self.space[index].span=newTB2.startTime-newTB1.endTime

		self.space.insert(index,newTB1)
		self.space.insert(index+2,newTB2)


		return self.space[index+1]
	
	def splitAndReturnLeft(self,startTB,tflex):
		index=self.space.index(startTB)

		newTB1=TimeBlock(startTB.startTime+tflex.duration,startTB.endTime,startTB.endTime-startTB.startTime-tflex.duration,None)
		self.space[index].startTime=startTB.startTime
		self.space[index].endTime=newTB1.startTime
		self.space[index].span=newTB1.startTime-startTB.startTime
		self.space.insert(index+1,newTB1)

		return self.space[index]
	def splitAndReturnRight(self,startTB,tflex):
		index=self.space.index(startTB)

		newTB1=TimeBlock(startTB.startTime,startTB.endTime-tflex.duration,startTB.endTime-tflex.duration,None)
		self.space[index].startTime=startTB.endTime-tflex.duration
		self.space[index].endTime=startTB.endTime
		self.space[index].span=startTB.endTime-startTB.endTime+tflex.duration
		self.space.insert(index,newTB1)

		return self.space[index+1]


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


	def LocateKick(self,counter,tflex):
		if(counter<0):
			pointer=0
		else:
			pointer=counter
		minPriority=self.space[pointer]

		for i in self.space:
			if i.startTime >=tflex.lowerbound and i.startTime<tflex.upperbound:
				if(isinstance(i.status,FlexibleTask) and i.status.priority>minPriority.status.priority):
					minPriority=self.space[pointer]
		if(minPriority.status.priority>tflex.priority):
			return minPriority.status
		else:
			return None


	def LocateKickFix(self,tfix):
		tokick=[]
		for i in self.space:
			if (isinstance(i.status,FlexibleTask)):
				'''if(i.startTime<= tfix.mustart and i.endTime>tfix.mustend):
					tokick.append(i)
				elif(i.startTime<tfix.mustart and i.endTime>=tfix.mustend):
					tokick.append(i)
				elif(i.startTime>tfix.mustart and i.endTime<tfix.mustend):
					tokick.append(i)
				elif(i.startTime==tfix.mustart and i.endTime==tfix.mustend):
					tokick.append(i)'''

				if(i.startTime >= tfix.mustart and i.startTime<tfix.mustend):

					tokick.append(i)										
				elif(i.endTime <= tfix.mustend and i.endTime>tfix.mustart):
					tokick.append(i)
				elif(i.startTime<tfix.mustart and i.endTime>tfix.mustend) :
					tokick.append(i)
		for i in tokick:
			print (i.startTime)
		return tokick


	def Kick(self,tobekicked):
		heapq.heappush(self.priorityQueue,(tobekicked.priority,tobekicked))
		for i in self.space:
			if isinstance(i.status,FlexibleTask):
				if i.status.title==tobekicked.title:
					i.status=None


	def AllocateRemainingTime(self,counter,tflex,remainingTime):
		pass

	def Merge(self):
		#def __init__(self,title,duration,mustart,mustend):
	#	def __init__(self,startTime,endTime,span,status):		
		#dagdag muna ng fix sa bawat end	
		self.space.insert(0,TimeBlock(0,0,0,(FixTask("temp",0,0,0))))
		self.space.append(TimeBlock(2400,0,0,(FixTask("temp",0,0,0))))
		head=tail=0
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
	#myAS.AllocateTime(FlexibleTask("B",100,1,1000,1100))		

	#myAS.AllocateTimeFix(FixTask("D",100,1100,1200))		
	myAS.AllocateTimeFix(FixTask("E",100,700,800))			
	myAS.AllocateTimeFix(FixTask("F",200,600,800))			
	#myAS.AllocateTimeFix(FixTask("D",100,700,800))		
	#myAS.AllocateTimeFix(FixTask("D",200,600,800))				
	#myAS.GetData()
	for i in myAS.priorityQueue:
		myAS.AllocateTime(i[1])
	myAS.GetData()
	#myAS.AllocateTime(FlexibleTask("A",800,1,0,800))
	#myAS.GetData()	
	#for i in myAS.priorityQueue:
	#	myAS.AllocateTime(i[1])

	#pass
