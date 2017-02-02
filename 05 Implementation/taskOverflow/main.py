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
Initial Software for main Class, its structures and methods.

File created on January 29,2017.
Developed by TaskOverflow group.

This software serves as the primary Class that integrates the modules. 
Software Project (Task OverFlow).

'''


import Data.__init__ as Dat
import Control.__init__  as Con
import UI.__init__ as UI

import pygame

'''
This class integrates an instance of AllocationSpace in Data Classes
and Menu in Control classes.
Attribues are myAllocationSpace, and Allocator

'''

class main():
	def __init__(self):
		self.myAllocationSpace=Dat.AllocationSpace("myTasks") #intializes an instance of AllocationSpace
		
		self.Allocator=Con.Menu() #initializes an instance of Menu Class
		self.Allocator.ActiveState(self.myAllocationSpace) 
		#pygame.init()
		#myUI=UI.mainUI(self.myAllocationSpace)
	def loadData(self,fileName):
		pass


if __name__=="__main__":
	myAS=main()
