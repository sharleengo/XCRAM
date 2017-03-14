'''
MIT License

Copyright (c) 2017 Sharleen Go.

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

Sharleen Go
last updated on Febuary 17,2017
Initial Software for Data Classes , its structures and methods.

File created on Febuary 11, 2017.
Developed by TaskOverflow group.

This software serves as the primary Data Classes  of our 
Software Project (Task OverFlow).

'''


from functions import *
import heapq

# Task class variables
# tType: 0 for a fixed task, 1 for a flexible task.
# duration: The length of the Task represented in hours and minutes. Example: duration=215 means 2 hrs and 15 minutes.	
# mStart: For a fixed task, mStart is the time that task MUST start.
# 	  For a flexible task, mStart is the time that the task MAY start. The task may start at a later time compared to 
#         mStart ;however, it CANNOT start earlier than stime. If none is given, the default value is 0 (the start of the day).
# mEnd: For a fixed task, mEnd is the time that task MUST end.
#	For a flexible task, mEnd is the time that the task MAY end. The task may end at an earlier time compared to 
#	mEnd ;however, it CANNOT end later than mEnd. If none is given, the default value is 2400 (the end of the day).
# priority: For all fixed tasks, priority is -1
#	        For all flexible tasks whose priority is not assigned, priority is 101
#	        0 is the highest priority, 100 is the lowest priority
# partition: For a flexible task, this may either be 0 or 1. 1 means that the user allowed this task to be partitioned.

class Task:
	numberOfTasks= 0
	highestPriority= 0
	def __init__(self,title='',tType=-1,duration=0,mstart=0,mend=0,priority=-1,partition=0):
		Task.numberOfTasks +=1
		self.tid = Task.numberOfTasks
		self.title = title
		self.tType = tType
		self.duration = duration
		self.mStart=mstart
		self.mEnd=mend
		self.partition=partition
		self.priority = priority

	def __cmp__(self,other):				# this will be used by the methods of heapq defined in python
		if(other!=None):
			return cmp(self.priority, other.priority)
		else:
			return 1	

	def display(self):
		print "title = ",self.title,"\ntype = ",self.type,"\nduration = ",self.duration,"\nstime = ",self.stime,"\netime = ",self.etime,"\npriority = ",self.priority,"\ntid=",self.tid,"\n"

# TimeBlock class variables
# stime: the start time of the TimeBlock
# etime: the end time of the TimeBlock
# duration : the length of the TimeBlock
# status: if None, the TimeBlock is free
# prev: refers to the previous TimeBlock in the Schedule
# next: refers to the next TimeBlock in the Schedule
class TimeBlock:
	def __init__(self,stime=0,etime=2400,duration=2400,status=None,prevb=None,nextb=None):
		self.stime=stime
		self.etime=etime
		self.duration=duration
		self.status=status
		self.prev=prevb
		self.next=nextb
	def display(self):
		print self.stime,"-",self.etime,"\t",
		if(self.status!=None):
			print self.status.title,"\t",
			print self.duration,"\t",
			if(self.status.tType == 1):
				print "Flexible",
				if(self.status.priority==101):
					print "(None)",
				else:
					print "(P= ",self.status.priority,")",
				print "\t(",self.status.mStart," , ",self.status.mEnd,")\n"	
			else:
				print "Fixed\n"	
		else:
			print '---     ',		
			print self.duration,"\n"

	def isFree(self):
		return 1 if(self.status==None) else 0	
	def isEnough(self,duration):	
		if(self.duration>=duration):
			return 1
		else:
			return 0					
	def free(self):
		self.status=None	
	def shouldSplit(self,duration):
		if(self.duration>duration):
			return 1
		else:
			return 0			

#sched: the first TimeBlock in the schedule.
class Schedule:
	PQ = []
	def __init__(self):
		self.sched = TimeBlock()

	def displaytasksList(self):
		pointer=self.sched
		while (pointer!=None):		
			if(pointer.status!=None):
				print pointer.status.tid," - ",pointer.status.title,"\n"
			pointer=pointer.next

	def clear(self):
		self.sched = TimeBlock()

	# This function is in charge of looking for the TimeBlock containing the given start time.	
	def locateTB(self,start):
		pointer=self.sched
		while (pointer!=None):		
			if(pointer.stime<=start and pointer.etime>start):
				return pointer
			pointer=pointer.next

	# This function decides whether it is possible to kick some tasks to give way for the new created fixed task.
	# This function will check whether there are other fixed tasks occupying the desired timeslot by going through each time block that lies
	# within the desired timeslot. Once a fixed task is found, that means the addition of the new task is not possible so, return 0.
	# If there are no fixed task occupying the desire timeslot, return the array containing all the ids of the flexible tasks that must be kicked.
	def canKickFix(self,TB,end):
		pointer=TB		#This TB is the one returned by the locateTB function
		tasksToKick=[]
		while(True):
			if(pointer.status!=None):
				if(pointer.status.tType==0):
					return 0
				else:
					if(pointer.status.tid not in tasksToKick):
						tasksToKick.append(pointer.status.tid)
			if(pointer.etime>=end):
				return tasksToKick
			pointer=pointer.next				
	
	# This function checks whether the removal of all flexible tasks that lies within the bounds
	# of the new flexible task and whose priority is less than the priority
	# of the new flexible task to be added will allow the new flexible task to fit the schedule.
	# It returns an array of tasks ids that need to be kicked if kicking those task will 
	# allow the addition of the new flexible task. Otherwise, it returns 0
	def canKickFree(self,NT):
		tasksToKick=[]
		pointer=self.locateTB(NT.mStart)
		totaldur = 0
		pointer=self.locateTB(NT.mStart)	
		if(pointer.isFree() or (pointer.status.tType==1 and pointer.status.priority>NT.priority)):
			if(pointer.status!=None and (pointer.status.tid not in tasksToKick)):
				tasksToKick.append(pointer.status.tid)
			totaldur=addTime(totaldur,getDuration(NT.mStart,pointer.etime))
		pointer = pointer.next	
		while(True):
			if(pointer.etime>=NT.mEnd):	
				break					
			if(pointer.isFree() or (pointer.status.tType==1 and pointer.status.priority>NT.priority)):
				if(pointer.status!=None and (pointer.status.tid not in tasksToKick)):
					tasksToKick.append(pointer.status.tid)
				totaldur=addTime(totaldur,pointer.duration)							
			pointer=pointer.next
		if(pointer.isFree() or (pointer.status.tType==1 and pointer.status.priority>NT.priority)): 
			if(pointer.status!=None and (pointer.status.tid not in tasksToKick)):
				tasksToKick.append(pointer.status.tid)
			totaldur=addTime(totaldur,getDuration(pointer.stime,NT.mEnd))

		print "Total Duration is: ",totaldur,"\n"
		if(totaldur<NT.duration):	
			return 0	
		else:
			return tasksToKick	

	# This functions uses an array of task id's called tasksToKick to determine which tasks need to be kicked
	# to give way for the new flexible task to be added. All the tasks whose ids are in tasksToKick have priorities
	# less than that of the new flexible task
	def Kick(self,tasksToKick):
		pointer=self.sched
		while (pointer!=None):
			if(pointer.status!=None and pointer.status.tid not in tasksToKick):
				pointer = pointer.next
			else:	
				if(pointer.status==None):
					startmerge = pointer
				elif(pointer.status.tid in tasksToKick):
					if(pointer.status not in Schedule.PQ):
						heapq.heappush(Schedule.PQ,pointer.status)
					pointer.status = None
					startmerge = pointer
				pointer = pointer.next
				endmerge = None
				while (pointer!=None and (pointer.status==None or pointer.status.tid in tasksToKick)):
					if(pointer.status!=None):	
						if(pointer.status not in Schedule.PQ):
							heapq.heappush(Schedule.PQ,pointer.status)
						pointer.status = None
					endmerge=pointer
					pointer=pointer.next
				if(endmerge!=None):
					self.merge(startmerge,endmerge)


	# Given two TimeBlocks (TB and last) this function merges all the TimeBlocks (from TB until last, inclusive) 
	# to a single TimeBlock.
	def merge(self,TB,last):
		TB.etime=last.etime
		TB.duration=getDuration(TB.stime,TB.etime)
		TB.next=last.next
		if(last.next!=None):
			last.next.prev = TB	

	# Given a TimeBlock TB containing the times start and end, the function splits TB into a TimeBlock slotFound
	# which perfectly fits the new fixed task. It also returns the slotFound TimeBlock
	# Also, it returns the excess TimeBlocks back into the schedule by merging them with adjacent free TimeBlocks
	# if there are any.
	def split(self,TB,start,end):
		slotFound = TB
		if(slotFound.stime<start):	# remove upper excess
			temp=slotFound.prev
			if(temp!=None and temp.status==None):	# upper excess needs to be merged with its previous free TimeBlock
				temp.etime=start
				temp.duration=getDuration(temp.stime,temp.etime)
				slotFound.stime = start
				slotFound.duration = getDuration(slotFound.stime,slotFound.etime)
			else:	# upper excess becomes a new free TimeBlock
				slotFound = TimeBlock(start,TB.etime,getDuration(start,TB.etime))
				slotFound.prev=TB
				slotFound.next=TB.next
				TB.etime=start
				TB.duration=getDuration(TB.stime,TB.etime)
				TB.next=slotFound			
		if(slotFound.etime>end):	# remove lower excess
			temp=slotFound.next 
			if(temp!=None and temp.status==None):	# lower excess needs to be merged with its next free TimeBlock
				temp.stime=end
				temp.duration=getDuration(temp.stime,temp.etime)
				slotFound.etime = end
				slotFound.duration = getDuration(slotFound.stime,slotFound.etime)
			else:
				extra = TimeBlock(end,slotFound.etime,getDuration(end,slotFound.etime))
				extra.prev=slotFound
				extra.next=slotFound.next
				slotFound.etime=end
				slotFound.duration=getDuration(slotFound.stime,slotFound.etime)
				slotFound.next=extra
		return slotFound

	# Given a flexible task NT, this function looks for a free TimeBlock in the schedule that would fit NT given
	# NT's lower and upper bounds. 	
	def locateFreeFitTB(self,NT):
		pointer=self.locateTB(NT.mStart)	# Check whether the first TimeBlock found can fit this flexible task
		if(pointer.isFree() and getDuration(NT.mStart,pointer.etime)>= NT.duration):
			return pointer
		pointer = pointer.next	
		while(True):
			if(pointer.etime>=NT.mEnd):	# Stop looping when the last potential Time Block is found
				break					
			if(pointer.isFree() and pointer.isEnough(NT.duration)):	# Check whether there is a free TimeBlock whose start time and end time
				return pointer										# falls inside the given lower and upper bound of the new flexible task.
			pointer=pointer.next
		if(pointer.isFree() and getDuration(pointer.stime,NT.mEnd)>= NT.duration): #Check whether the last TimeBlock found can fit the flexible task
			return pointer
		else:		# There is no free TimeBlock within the Schedule that fits the new flexible task.
			return None	


	# Given a new task NT, this function checks whether the free blocks that lies within the bounds of the new task is enough to fit the new task if
	# the new task were partitioned and the user allowed this feature. 
	def canPartition(self,NT):
		totaldur = 0
		pointer=self.locateTB(NT.mStart)	
		if(pointer.isFree()):
			totaldur=addTime(totaldur,getDuration(NT.mStart,pointer.etime))
		pointer = pointer.next	
		while(True):
			if(pointer.etime>=NT.mEnd):	
				break					
			if(pointer.isFree()):
				totaldur=addTime(totaldur,pointer.duration)							
			pointer=pointer.next
		if(pointer.isFree()): 
			totaldur=addTime(totaldur,getDuration(pointer.stime,NT.mEnd))
		
		if(totaldur<NT.duration):	
			return 0	
		else:
			return 1

	# Given a new task NT, this function allots slots to the given task by partitioning it.
	# As a result, the new flexible task will have multiple time slots scattered within the schedule.
	def partition(self,NT):
		remaining = NT.duration
		pointer=self.locateTB(NT.mStart)	
		if(pointer.isFree()):
			slot = self.split(pointer,NT.mStart,pointer.etime)
			slot.status = NT
			remaining=getDuration(slot.duration,remaining)
		pointer = pointer.next	
		while(remaining!=0):
			if(pointer.etime>=NT.mEnd):	
				break					
			if(pointer.isFree()):
				if(pointer.duration>remaining):	# This time slot is the last one that we'll be needing
					slot = self.split(pointer,pointer.stime,addTime(pointer.stime,remaining))
					slot.status = NT
					remaining=getDuration(slot.duration,remaining)
				else:	
					pointer.status=NT
					remaining=getDuration(pointer.duration,remaining)	
			pointer=pointer.next
		if(remaining!=0):
			if(pointer.isFree()): 
				if(getDuration(pointer.stime,NT.mEnd)>remaining):	# This time slot is the last one that we'll be needing
					slot = self.split(pointer,pointer.stime,addTime(pointer.stime,remaining))
				else:	
					slot = self.split(pointer,pointer.stime,NT.mEnd)
				slot.status = NT
				remaining=getDuration(slot.duration,remaining)
				
