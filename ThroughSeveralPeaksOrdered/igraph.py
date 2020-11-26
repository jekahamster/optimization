import vertex

class IGraph():
	def appendVertex(self, x: int, y: int) -> vertex.Vertex:
		pass
	
	def getVertexs(self) -> list:
		pass

	def getPaths(self) -> list:
		pass

	def getMatrix(self) -> list:
		pass

	def setPath(self, vertex1: vertex.Vertex, vertex2: vertex.Vertex) -> None:
		pass

	def setFullPath(self) -> None:
		pass
	
	def removePath(self, vertex1: vertex.Vertex, vertex2: vertex.Vertex) -> None:
		pass

	def removeVertex(self, vertex: vertex.Vertex) -> None:
		pass

	def removeAllPath(self) -> None:
		pass
	
	def hasRelation(self, vertex1: vertex.Vertex, vertex2: vertex.Vertex) -> bool:
		pass