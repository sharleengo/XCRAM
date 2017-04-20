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
last updated on March 16,2017
Initial Software for Control Classes , its structures and methods.

File created on Febuary 11, 2017.
Developed by TaskOverflow group.

This software serves as the primary Control Classes  of our 
Software Project (Task OverFlow).

'''
from Data.__init__ import *
from collections import deque
import heapq

# Given a schedule, this class hanldles all the possible manipulations (add task, delete task, clear schedule) that 
# the user may perform on the given schedule.				
class Scheduler:
	# NT: the new task to be added
	# CS: the current schedule
	def __init__(self):
		self.CS = Schedule()
		self.messages = deque([])
		self.loadSched()
	def displaySched(self): 
		pointer=self.CS.sched
		print "Time\t\tTask\tDuration\tType\t\tBounds(Lower,Upper)"
		print '-'*100
		while(pointer!=None):
			pointer.display()
			pointer=pointer.next

	def menu(self):
		while (True):
			print "priority queue: ",self.CS.PQ,"\n"
			self.displaySched()
			response = raw_input("[A]Add task     [C]Clear Schedule     [D]Delete Task     [E]Edit Task 	[Q]Quit\n ")
			print "\n"
			if(response.lower() == 'q' ):
				self.saveSched()
				break
			elif (response.lower() == 'a'):
				NT= Task()
				NT.title = raw_input("Enter task title:\n ")
				NT.tType = input("Enter task type (0-Fixed 1-Flexible):\n ")
				NT.duration = input("Enter task duration (min=1  maximum=2400):\n ")
				if(NT.tType == 0):
					NT.mStart= input("Enter start time:\n ")
					NT.mEnd = addTime(NT.mStart,NT.duration)
				else:	
					NT.mStart= input("Enter the earliest time that the task should start:\n ")
					NT.mEnd = input("Enter the latest time that the task should be finished:\n ")
					response = raw_input("Would you like to assign a priority to this task (y/n):\n ")
					if(response.lower() == 'y' ):
						NT.priority = input("Enter the priority (0-100 with 0 being the highest):\n ")
					else:
						NT.priority = 101
					response = raw_input("Would you allow this task to be partitioned? (y/n):\n ")	
					if(response.lower() == 'y' ):
						NT.partition = 1
				self.addTask(NT)

			elif (response.lower() == 'c'):
				response = raw_input("Are you sure you want to clear the current schedule? (y/n): \n ")	
				if(response.lower()=='y'):
					self.clearSched()

			elif (response.lower() == 'd'):
				self.CS.displaytasksList()
				response = raw_input("Enter the id of the task to be deleted (C to cancel) : \n ")	
				if(response.lower()!='c'):
					self.deleteTask(int(response))
			
			elif (response.lower() == 'e'):
				self.CS.displaytasksList()
				response = raw_input("Enter the id of the task to be edited (C to cancel) : \n ")	
				if(response.lower()!='c'):
					self.editTask(int(response))


				# Insert code for delete task
			else:
				print "Please enter a valid option\n"	

	def message(self,msg):
		print '*'*(len(msg)+4)+"\n"
		print " "+msg+" "
		print '*'*(len(msg)+4)+"\n"

	def addTask(self,NT):
		TB=None
		error=0		#this will be set to 1 if the new task can no longer be added to the current schedule
		if(NT.tType==0):	#adding a fixed task
			TB=self.CS.locateTB(NT.mStart)	
			if(getDuration(NT.mStart,TB.etime)>=NT.duration):
				if(not TB.isFree()):
					if(TB.status.tType==0):
						error+=1	#the timeslot is already taken by another fixed task
					else:	#the timeslot is taken by a flexible task that must be rescheduled
						tasksToKick = []
						tasksToKick.append(TB.status.tid)
						self.CS.Kick(tasksToKick)
						TB = self.CS.locateTB(NT.mStart)
			else: 
				tasksToKick = self.CS.canKickFix(TB,NT.mEnd)
				if(tasksToKick):
					self.CS.Kick(tasksToKick)
					TB = self.CS.locateTB(NT.mStart)
				else:
					error+=1 # There is no use in kicking the flexible tasks(if any) because there is another fixed task
							 # that is occupying the desired timeslot.			
			if(error>0):
				m="The new task: \""+ NT.title +"\" may no longer be added due to conflicts with another fixed task."
				self.message(m)
				self.messages.append(m)
				return None

			else:			
				if(TB.shouldSplit(NT.duration)):				# We were able to obtain a TimeBlock that could fit the new fixed task
					slotFound=self.CS.split(TB,NT.mStart,NT.mEnd)	# But, we not allot the whole block for our fixed task if the TimeBlock's
																# duration is greater than our fixed task's duration.
				else:
					slotFound=TB # The slot that we found exactly fits the new fixed task so no splitting is needed.
			
				slotFound.status=NT
				m= "The new fixed task: \""+ NT.title +"\" was successfully added!"	
				self.message(m)
				self.messages.append(m)

		else:	#Adding a flexible task			
			TB= self.CS.locateFreeFitTB(NT)
			if (TB!=None): #Best case scenario, there was an existing free timeblock in the schedule that could fit the new flexible task
				if(TB.shouldSplit(NT.duration)):
					if(TB.stime<NT.mStart):
						slotFound=self.CS.split(TB,NT.mStart,addTime(NT.mStart,NT.duration))
					else:
						slotFound=self.CS.split(TB,TB.stime,addTime(TB.stime,NT.duration))
				else:
					slotFound = TB
				slotFound.status=NT
				self.displaySched()
				m= "The new flexible task \"" + NT.title +"\" was successfully added!"	
				self.message(m)
				self.messages.append(m)
				return 	

			elif(NT.partition==1 and self.CS.canPartition(NT)):	
				self.CS.partition(NT)
				self.displaySched()
				m= "The new flexible task \""+ NT.title +"\" was added by partitioning."	
				self.message(m)
				self.messages.append(m)	
				return 

			tasksToKick = self.CS.canKickFree(NT)	
			if(tasksToKick):
				self.message("Do kicking ....")
				print "Tasks to Kick ",tasksToKick,"\n"
				self.CS.Kick(tasksToKick)
				heapq.heappush(self.CS.PQ,NT)

			else:
				m="The task \""+NT.title+"\" can no longer fit into the schedule."
				self.message(m)
				self.messages.append(m)
				return 

		if(len(self.CS.PQ)!=0):
			self.reschedule()
		self.displaySched()
	def reschedule(self):
		while (len(self.CS.PQ)!=0):
			self.addTask(heapq.heappop(self.CS.PQ))	

	def deleteTask(self,tid):						
		tasktodelete=[]
		tasktodelete.append(tid)
		self.CS.Kick(tasktodelete)
		deletedTask =heapq.heappop(self.CS.PQ)
		m= "The task \"" + deletedTask.title +"\" was successfully deleted!"
		self.message(m)
		self.messages.append(m)	

	def editTask(self,NT,tid):
		pointer = self.CS.sched
		while (pointer!=None):
			if(pointer.status!=None and pointer.status.tid == tid):
				break
			pointer = pointer.next

		editThis = pointer.status
		editThis.display()	
		
		mustReschedule = False
		if(NT.duration!=editThis.duration or NT.mStart!=editThis.mStart or editThis.mEnd!=NT.mEnd or NT.partition<editThis.partition):
			mustReschedule = True

		if(mustReschedule):
			self.deleteTask(tid)
			self.addTask(NT)
		else:
			pointer.status = NT
			while(pointer!=None):
				if(pointer.status!=None and pointer.status.tid == tid):
					pointer.status = NT
				pointer = pointer.next	

		m= "The task \"" + editThis.title +"\" was successfully edited!"
		self.message(m)
		self.messages.append(m)	

	def clearSched(self):
		self.CS.clear()	
		m= "The schedule was successfully cleared!"
		self.message(m)
		self.messages.append(m)

	def saveSched(self):
		fob=open("Data/mySched.txt","w")
		pointer = self.CS.sched
		while (pointer!=None):
			fob.write(str(pointer.stime)+","+str(pointer.etime)+","+str(pointer.duration))
			if(pointer.status!=None):
				fob.write(",taken,")
				fob.write(str(pointer.status.tid)+","+pointer.status.title+","+str(pointer.status.tType)+","+str(pointer.status.duration)+","+str(pointer.status.mStart)+","+str(pointer.status.mEnd)+","+str(pointer.status.priority)+","+str(pointer.status.partition)+"\n")
			else:
				fob.write(",free\n")

			pointer=pointer.next
		fob.write("EOF")
		fob.close()

	def loadSched(self):
		fob=open("Data/mySched.txt","r")
		prev = None
		sched = TimeBlock()
		pointer = sched
		numberOfTasks = 0
		for line in fob:
			line= line.rstrip("\n")
			line= line.split(",")
			if(line[0]=="EOF"):
				break
			else:	
				if(prev!=None):
					prev.next=pointer
		    	pointer.stime =int(line[0])
		    	pointer.etime =int(line[1])
		    	pointer.duration = int(line[2])	
		    	if(line[3]=="taken"):
		    		task = Task()
		    		task.tid = int(line[4])
		    		numberOfTasks = max(numberOfTasks,task.tid)
		    		task.title = line[5]
		    		task.tType = int(line[6])
		    		task.duration = int(line[7])
		    		task.mStart = int(line[8])
		    		task.mEnd = int(line[9])
		    		task.priority = int(line[10])
		    		task.partition = int(line[11])
		    		pointer.status = task
		    	else:	   		
		    		pointer.status = None
		    	pointer.prev = prev
		    	pointer.next = None
		    	prev = pointer
		    	pointer = TimeBlock()
		Task.numberOfTasks = numberOfTasks    	
		fob.close()
		self.CS.sched = sched	
		self.displaySched()
