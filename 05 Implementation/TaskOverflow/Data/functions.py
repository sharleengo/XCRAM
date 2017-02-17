# Given a start time and a duration, it returns the end time. Example: start=215 duration=55 end=310
def addTime(start,duration):
	hours=start/100 + duration/100
	mins=start%100 + duration%100
	return (hours+mins/60)*100+(mins%60)

#Given a start time and end time, it returns the duration. Example: start=1215 end=1345 duration=130
def getDuration(start,end):
	min1= (start/100)*60+(start%100)
	min2= (end/100)*60+(end%100)
	min3= min2-min1
	return (min3/60)*100+(min3%60)