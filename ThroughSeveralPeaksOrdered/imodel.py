import igraph
import ifinder
import vertex

class IModel():
	def setGraph(self, graph: igraph.IGraph) -> igraph.IGraph:
		pass		

	def setFinder(self, finder: ifinder.IFinder) -> ifinder.IFinder:
		pass
		
	def appendVertex(self, x: float, y: float) -> vertex.Vertex:
		pass

	def setPath(self, vertex1: vertex.Vertex, vertex2: vertex.Vertex) -> None:
		pass

	def removePath(self, vertex1: vertex.Vertex, vertex2: vertex.Vertex) -> None:
		pass

	def removeVertex(self, vertex: vertex.Vertex) -> vertex.Vertex:
		pass

	def hasPath(self, vertex1: vertex.Vertex, vertex2: vertex.Vertex) -> bool:
		pass

	def getAllVertex(self) -> list:
		pass

	def getAllPath(self) -> list:
		pass

	def setFullPath(self) -> None:
		pass

	def removeAllPath(self) -> None:
		pass