
class Pair:
	def __init__(self, first = None, second = None):
		self.first 	= first
		self.second = second

	def __repr__(self):
		return "P({0} ; {1})".format(self.first, self.second)

	def __eq__(self, other):
		return (self.first == other.first) and (self.second == other.second)

	def getFirst(self):
		return self.first

	def getSecond(self):
		return self.second

	def setFirst(self, first):
		self.first = first

	def setSecond(self, second):
		self.second = second