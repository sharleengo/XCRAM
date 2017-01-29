from __future__ import print_function

import heapq


class Task():
	def __init__(self, title,duration):
		self.title=title
		self.duration=duration

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
	def free(self):
		del self
	def Merge(self):
		pass

	def shouldSplit(self,newTask):
		if(self.space>newTask.duration):
			return True
		else:
			return False		
	def split(self,newTask):
		oldEndTime=self.endTime
		self.endTime=self.startTime+newTask.duration
		self.space=newTask.duration
		self.status=newTask

		'''create the new TB'''
		newTimeBlock=TimeBlock(self.endTime+1,oldEndTime,oldEndTime-(self.endTime+1),None,self.next,self)
		self.next=newTimeBlock
		return newTimeBlock



class AllocationSpace():

	def __init__(self,name):
		'''this constructor initializes the class and sets the name; new space is created and initialized priorityQueue to be empty'''
		self.name=name
		self.space=[TimeBlock(0,2400,2400,None)]
		self.priorityQueue=[]
		self.maxPriority=None


	def GetData(self):
		for i in self.space:
			print ("\n",i.startTime,"\t",i.endTime,"\t",i.span,end="\t")
			if i.status!=None:
				print (i.status.title)		
		print ("\nPila\t ",self.priorityQueue)

	
		print ("\n")


	def AllocateTime(self,tflex):
		print ("allocating")
		startTB=self.SearchStartingTimeBlock(tflex)
		old=startTB
		if(startTB==None):
			startTB=self.SearchStartingFlexibleTaskTimeBlock(tflex)
			if startTB==None:
				print ("task cannot be allocated")
				return
			'''else:
				timeRemaining=tflex.duration
				#while(timeRemaining>0):
				tasktokick=self.LocateKick(self.space.index(startTB),tflex)
				if(tasktokick==None):
					return
				else:
					self.Kick(tasktokick)
					self.Merge()
					startTB=self.SearchStartingTimeBlock(tflex)					
					print "startingBlock","\t",startTB.startTime,startTB.endTime
					print self.priorityQueue'''

		print (startTB.startTime,startTB.endTime)
		if(not startTB.isFree()):
			tasktokick=self.LocateKick(self.space.index(startTB),tflex)
			if(tasktokick==None):
				print ("task cannot be allocated")
				return
			else:
				self.Kick(tasktokick)
				self.Merge()
				startTB=self.SearchStartingTimeBlock(tflex)	


		if(startTB.isEnough(tflex)):
			if(self.inTheMiddle(startTB,tflex)):
				print ("in the middle")
				startTB=self.splitAndReturnMiddle(startTB,tflex)
			elif(self.leftSided(startTB,tflex)):
				print ("left")				
				startTB=self.splitAndReturnLeft(startTB,tflex)
			elif(self.rightSided(startTB,tflex)):
				print ("right")	
				startTB=self.splitAndReturnRight(startTB,tflex)			
		timeRemaining=tflex.duration


		while(timeRemaining>0):
			'''tasktokick=self.LocateKick(self.space.index(startTB),tflex)
			if(tasktokick==None):
				print "unable to allocate space for the given task"
				return
			else:
				self.Kick(tasktokick)
				self.Merge()
				timeRemaining=self.AllocateMaxTime(self.space.index(startTB),tflex,tflex.duration)		
				startTB=self.SearchStartingTimeBlock()'''
			if(startTB==None):				
				startTB=self.SearchStartingFlexibleTaskTimeBlock(tflex)
				if(startTB==None):
					print ("cannot Allocate")
					return
				else:
					tasktokick=self.LocateKick(self.space.index(startTB),tflex)
					if(tasktokick==None):
						print ("unable to allocate space for the given task")
						return
					else:
						self.Kick(tasktokick)
						self.Merge()
						startTB=self.SearchStartingTimeBlock(tflex)
						timeRemaining=self.AllocateMaxTime(self.space.index(startTB),tflex,tflex.duration)	

						startTB=self.SearchStartingTimeBlock(tflex)
			else:

				timeRemaining=self.AllocateMaxTime(self.space.index(startTB),tflex,timeRemaining)
				oldstartTb=startTB
				startTB=self.SearchStartingTimeBlock(tflex)				

				if(oldstartTb==startTB):
					startTB=None
					#print ("task is not allocated")
					#return


		print ("Task Allocated is a success")
		'''startTB=old
		if(self.maxPriority==None):
			self.maxPriority=startTB.status.priority
		else:
			if(self.maxPriority>startTB.status.priority):
				self.maxPriority=startTB.status.priority'''
		self.GetData()
	
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
					print (startTB.startTime,startTB.endTime)
				elif(self.rightSided(startTB,tfix)):
					print ("right")	
					startTB=self.splitAndReturnRight(startTB,tfix)			
			#self.Merge()
		elif startTB==None:
			TBtokick=self.LocateKickFix(tfix)
			tasktokick=[]
			totalspan=0
			print (TBtokick)			
			for i in TBtokick:
				totalspan+=i.span
				tasktokick.append(i.status.title)
			if(totalspan<tfix.duration):
				print ("not enoug space, cannot be allocated")
				return
			else:
				for i in self.space:
					#print ("im heres")
					if(isinstance(i.status,FlexibleTask)):
						if i.status.title in tasktokick:
							self.Kick(i.status)
			startTB=self.SearchStartingTimeBlock(tfix)
			if(self.inTheMiddle(startTB,tfix)):
				print ("in the middle")
				tartTB=self.splitAndReturnMiddle(startTB,tfix)
			elif(self.leftSided(startTB,tfix)):
				print ("left")				
				startTB=self.splitAndReturnLeft(startTB,tfix)
				print (startTB.startTime,startTB.endTime)
			elif(self.rightSided(startTB,tfix)):
				print ("right")	
				startTB=self.splitAndReturnRight(startTB,tfix)			
		index=self.space.index(startTB)	
		self.space[index].status=tfix	
		self.Merge()
		self.GetData()

	def SearchStartingTimeBlock(self,tflex):
		if isinstance(tflex,FlexibleTask):
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

			if (self.space[pointer].isFree() and self.space[pointer].startTime>=tflex.lowerbound and self.space[pointer].endTime<=tflex.upperbound):
				self.space[pointer].status=tflex
				timeRemaining-=self.space[pointer].span
			pointer+=1
		return timeRemaining


	def LocateKick(self,counter,tflex):
		if(counter<0):
			pointer=0
		else:
			pointer=counter
		minPriority=self.space[pointer]
		'''while(pointer<len(self.space)):
			print self.space[pointer].startTime,tflex.upperbound
			if(self.space[pointer].startTime>tflex.upperbound):
				return minPriority.status
			if(self.space[pointer].status!=None):
				if(isinstance(self.space[pointer].status,FlexibleTask) and self.space[pointer].status.priority>minPriority.status.priority):
					minPriority=self.space[pointer]	
			pointer+=1
		'''

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
				print (i.startTime,i.endTime)
				if(i.startTime<= tfix.mustart and i.endTime>tfix.mustend):
					tokick.append(i)
				elif(i.startTime<tfix.mustart and i.endTime>=tfix.mustend):
					tokick.append(i)
				elif(i.startTime>tfix.mustart and i.endTime<tfix.mustend):
					tokick.append(i)
				elif(i.startTime==tfix.mustart and i.endTime==tfix.mustend):
					tokick.append(i)					
		return tokick


	def Kick(self,tobekicked):
		for i in self.space:
			if isinstance(i.status,FlexibleTask):
				if i.status==tobekicked:
					heapq.heappush(self.priorityQueue,(i.status.priority,i.status))
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
		self.space.remove(self.space[0])
		self.space.pop()


if __name__=="__main__":
	AS=AllocationSpace("myTasks")
	AS.AllocateTime(FlexibleTask("haha1",100,0,800,2400))
	tflex=FlexibleTask("title",200,1,800,2000)
	AS.AllocateTime(tflex)

	AS.AllocateTime(FlexibleTask("haha2",100,0,0,2400))
	#AS.AllocateTime(FlexibleTask("haha3",1100,0,0,2400))
	#AS.AllocateTime(FlexibleTask("haha4",500,0,1300,1900))	
	AS.AllocateTime(FlexibleTask("haha5",500,0,900,1400))	
	AS.AllocateTimeFix(FixTask("haha6",200,1400,1600))				
	AS.AllocateTimeFix(FixTask("haha6",200,900,	1100))					



		