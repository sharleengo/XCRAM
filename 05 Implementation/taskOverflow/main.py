import Data.__init__ as Dat
import Control.__init__  as Con
import UI.__init__ as UI

class main():
	def __init__(self):
		self.myAllocationSpace=Dat.AllocationSpace("myTasks")
		self.Allocator=Con.Menu()
		self.Allocator.ActiveState(self.myAllocationSpace)
	def loadData(self,fileName):
		pass


if __name__=="__main__":
	myAS=main()
