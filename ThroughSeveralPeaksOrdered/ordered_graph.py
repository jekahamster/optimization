import igraph
from pair import Pair
from vertex import Vertex

class OrderedGraph():
	def __init__(self):
		self.vertexCounter = 0
		self.vertex = {}

	def appendVertex(self, x, y):
		vertex = Vertex(x, y, self.vertexCounter)
		self.vertex[vertex] = set()
		self.vertexCounter += 1
		return vertex

	def setPathFromTo(self, vertex1, vertex2):
		self.vertex[vertex1].add(vertex2)

	def removePathFromTo(self, vertex1, vertex2):
		self.vertex[vertex1].discard(vertex2)

	def removeVertex(self, vertex):
		self.vertex.pop(vertex)
		for key in self.vertex.keys():
			self.vertex[key].discard(vertex)

	def hasRelation(self, vertex1, vertex2):
		return vertex2 in self.vertex[vertex1]

	def getVertexs(self):
		return [v for v in self.vertex.keys()]

	def getPaths(self):
		paths = []

		for v1 in self.vertex.keys():
			for v2 in self.vertex[v1]:
				paths.append(Pair(v1, v2))

		return paths

	def setFullPath(self):
		for v in self.vertex.keys():
			self.vertex[v] = set(self.vertex.keys())
			self.vertex[v].discard(v)

	def removeAllPath(self):
		for v in self.vertex.keys():
			self.vertex[v] = set()

	def getMatrix(self):
		pass
