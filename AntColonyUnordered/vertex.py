from pair import Pair

class Vertex:
	def __init__(self, x=None, y=None, i=None):
		self.x = x
		self.y = y
		self.i = i

	def __repr__(self):
		return "V({0};{1};{2})".format(self.x, self.y, self.i)

	def __hash__(self):
		return self.i

	def getX(self):
		return x

	def getY(self):
		return y

	def getI(self):
		return i

	def setX(self, x):
		self.x = x

	def setY(self, y):
		self.y = y

	def setY(self, i):
		self.i = i

	def distanceTo(self, v):
		dx = self.x - v.x
		dy = self.y - v.y
		return ((dx)**2 + (dy)**2)**0.5