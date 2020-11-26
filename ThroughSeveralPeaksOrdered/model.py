import imodel

class Model(imodel.IModel):
	def __init__(self, graph=None, finder=None):
		self.graph = graph
		self.finder = finder

	def setGraph(self, graph):
		self.graph = graph
		return self.graph

	def setFinder(self, finder):
		self.finder = finder
		return self.graph

	def appendVertex(self, x, y):
		return self.graph.appendVertex(x, y)

	def setPath(self, vertex1, vertex2):
		self.graph.setPathFromTo(vertex1, vertex2)

	def removePath(self, vertex1, vertex2):
		self.graph.removePathFromTo(vertex1, vertex2)

	def removeVertex(self, vertex):
		self.graph.removeVertex(vertex)

	def hasPath(self, vertex1, vertex2):
		return self.graph.hasRelation(vertex1, vertex2)

	def getAllVertex(self):
		return self.graph.getVertexs()

	def getAllPath(self):
		return self.graph.getPaths()

	def setFullPath(self):
		self.graph.setFullPath()

	def removeAllPath(self):
		self.graph.removeAllPath()

	def save(self, fileName):
		pass

	def load(self, fileName):
		pass

