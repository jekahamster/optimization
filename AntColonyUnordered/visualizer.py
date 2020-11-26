import tkinter as tk
import random as rnd
import colorama as cl
import json
import time

from threading import Thread
from PIL import ImageTk, Image

from vertex import Vertex 
from pair import Pair
from ant_colony import AntTSP

def showMatrix(matrix):
	for y in matrix:
		for x in y:
			print(round(x, 2), end="\t")
		print()


class Visualizer:
	ADD = 0
	DELETE = 1

	vertexSize = 20
	vertexBorderWidth = 2


	def __init__(self):
		self.vertex = []
		self.matrix = None

		self.vertexCounter = 0
		self.mode = Visualizer.ADD


		self.root = tk.Tk()
		self.root.title("Ant Colony")

		self.canvas = tk.Canvas(self.root, bg="white", width=800, height=800)

		self.bestResult = tk.Label(text="Best Result: None")
		self.modeLabel = tk.Label(text="Mode: ADD")
		self.modeAddButton = tk.Button(text="Set ADD mode", command=self.setAddMode)
		self.modeDelete = tk.Button(text="Delete mode", command=self.setDeleteMode)
		self.startButton = tk.Button(text="start", command=self.getPath)
		self.saveGraph = tk.Button(text="Save Graph", command=self.saveGraph)
		self.loadGraph = tk.Button(text="Load Graph", command=self.loadGraph)
		self.clearButton = tk.Button(text="clear", command=self.reset)


		self.rightSideWidgets = []
		self.rightSideWidgets.append(self.bestResult)
		self.rightSideWidgets.append(self.modeLabel)
		self.rightSideWidgets.append(self.modeAddButton)
		self.rightSideWidgets.append(self.modeDelete)
		self.rightSideWidgets.append(self.startButton)
		self.rightSideWidgets.append(self.saveGraph)
		self.rightSideWidgets.append(self.loadGraph)
		self.rightSideWidgets.append(self.clearButton)


		self.canvas.bind("<Button-1>", self.canvasClick)

		self.canvas.grid(row=0, column=0, rowspan=10, columnspan=10)
		for i in range(len(self.rightSideWidgets)):
			self.rightSideWidgets[i].grid(row=i, column=10, columnspan=4)

		self.root.mainloop()


	def getPath(self):
		timeStart = int(round(time.time() * 1000))

		self.matrix = self.getMatrix(self.vertex)
		# showMatrix(self.matrix)
		colony = AntTSP(self.matrix)

		bestPath, bestRes = colony.run(10)
		# bestPath, bestRes = colony.run(len(self.vertex)*10)
		
		path = [self.vertex[i] for i in bestPath]

		self.bestResult['text'] = "Best Result: " + str(bestRes)
		self.clearCanvas()
		Visualizer.drawAllPath(self.canvas, self.vertex)
		Visualizer.drawListVertex(self.canvas, path, "red", 10)
		Visualizer.drawAllVertex(self.canvas, self.vertex)

		timeStop = int(round(time.time() * 1000))
		print("Time:", timeStop - timeStart)

	def canvasClick(self, event):
		if self.mode == Visualizer.ADD:
			self.createVertex(event)

		elif self.mode == Visualizer.DELETE:
			v1 = self.findVertex(event)

			self.vertex.remove(v1)

			self.clearCanvas()
			Visualizer.drawAllVertex(self.canvas, self.vertex)




	def createVertex(self, event):
		vertex = Vertex(event.x, event.y, self.vertexCounter)

		self.vertex.append(vertex)
		self.vertexCounter += 1
		Visualizer.drawVertex(self.canvas, vertex)

	def reset(self):
		self.clearCanvas()
		self.vertex = []
		self.matrix = None
		self.vertexCounter = 0

	def clearCanvas(self):
		self.canvas.delete("all")
		

	def setAddMode(self):
		self.mode = Visualizer.ADD
		self.modeLabel["text"] = "Mode: ADD"

	def setDeleteMode(self):
		self.mode = Visualizer.DELETE
		self.modeLabel["text"] = "Mode: DELETE"

	def findVertex(self, event):
		minV = None
		minL = self.vertexSize+1

		for v in self.vertex:
			dx = v.x - event.x
			dy = v.y - event.y
			l = ((dx)**2 + (dy)**2)**0.5
			if (l <= self.vertexSize) and (l < minL):
				minV = v 
				minL = l

		return minV

	def saveGraph(self):
		tempVertex = []
		for v in self.vertex:
			vData = {
				"i": v.i,
				"x": v.x,
				"y": v.y 
			}
			tempVertex.append(vData)

		data = { "vertex": tempVertex }

		with open("graph.json", "w") as file:
			json.dump(data, file)

	def loadGraph(self):
		data = None
		self.vertex = [] 

		with open("graph.json", "r") as file:
			data = json.load(file)

		for d in data["vertex"]:
			tempVertex = Vertex( d["x"], d["y"], d["i"] )
			self.vertex.append( tempVertex )

		self.clearCanvas()
		Visualizer.drawAllPath(self.canvas, self.vertex)
		Visualizer.drawAllVertex(self.canvas, self.vertex)

	def getMatrix(self, vertex):
		matrix = [[0 for x in range(len(vertex))] for y in range(len(vertex))]

		for i in range(len(vertex)):
			for j in range(len(vertex)):
				if (matrix[i][j] == 0):
					matrix[i][j] = vertex[i].distanceTo(vertex[j])
					matrix[j][i] = matrix[i][j]

		return matrix

	@staticmethod
	def drawVertex(canvas, vertex, vertexColor="white", vertexBorder="black"):
		x1 = vertex.x - Visualizer.vertexSize
		x2 = vertex.x + Visualizer.vertexSize
		y1 = vertex.y - Visualizer.vertexSize
		y2 = vertex.y + Visualizer.vertexSize

		canvas.create_oval(x1, y1, x2, y2, fill=vertexColor, 
			outline=vertexBorder, width=Visualizer.vertexBorderWidth)
		canvas.create_text(vertex.x-10, vertex.y, 
			anchor=tk.W, text=vertex.i, font=("Courier", 15))


	@staticmethod
	def drawPath(canvas, v1, v2, color="black"):
		canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=color)

	@staticmethod
	def drawAllPath(canvas, vertex, color="black"):
		visited = [[False for x in range(len(vertex))] for y in range(len(vertex))]
		for i in range(len(vertex)):
			for j in range(len(vertex)):
				if (i != j) and (not visited[i][j]):
					visited[i][j] = True
					v1 = vertex[i]
					v2 = vertex[j]
					canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=color)

	@staticmethod
	def drawAllVertex(canvas, vertex):
		for v in vertex:
			x1 = v.x - Visualizer.vertexSize
			x2 = v.x + Visualizer.vertexSize
			y1 = v.y - Visualizer.vertexSize
			y2 = v.y + Visualizer.vertexSize
			canvas.create_oval(x1, y1, x2, y2, fill="white", 
				outline="black", width=Visualizer.vertexBorderWidth)
			canvas.create_text(v.x-10, v.y, 
				anchor=tk.W, text=v.i, font=("Courier", 15))

	@staticmethod 
	def drawListVertex(canvas, vlist, color="red", width=2):
		for i in range(len(vlist)-1):
			v1 = vlist[i]
			v2 = vlist[i+1]
			canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=color, width=width)


Visualizer()
