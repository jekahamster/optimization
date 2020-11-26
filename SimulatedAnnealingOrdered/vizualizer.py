import tkinter as tk
import random as rnd
import colorama as cl
import time
from threading import Thread
from PIL import ImageTk, Image

from vertex import Vertex 
from pair import Pair

class Visualizer:
	ADD = 0
	CHANGE_PATH = 1
	SELECT_DIRECTION = 2
	DELETE = 3

	vertexSize = 20
	vertexBorderWidth = 2


	def __init__(self):
		self.vertex = []
		self.path = {}

		self.vertexCounter = 0
		self.mode = Visualizer.ADD
		self.selectedV1 = None
		self.selectedV2 = None
		self.start = None
		self.end = None


		self.root = tk.Tk()
		self.root.title("Ant Colony")

		self.canvas = tk.Canvas(self.root, bg="white", width=800, height=800)

		self.modeLabel = tk.Label(text="Mode: ADD")
		self.fromLabel = tk.Label(text="From: ")
		self.toLabel = tk.Label(text="To: ")
		self.modeAddButton = tk.Button(text="Set ADD mode", command=self.setAddMode)
		self.modeChangeWeightsButton = tk.Button(text="Set CHANGE_PATH mode", command=self.setChangeWeightsMode)
		self.modeSelectDirectionButton = tk.Button(text="Set SELECT_DIRECTION mode", command=self.setSelectDirectionMode)
		self.modeDelete = tk.Button(text="Delete mode", command=self.setDeleteMode)
		self.startButton = tk.Button(text="start", command=lambda: print(1))
		self.clearButton = tk.Button(text="clear", command=self.reset)


		self.rightSideWidgets = []
		self.rightSideWidgets.append(self.modeLabel)
		self.rightSideWidgets.append(self.fromLabel)
		self.rightSideWidgets.append(self.toLabel)
		self.rightSideWidgets.append(self.modeAddButton)
		self.rightSideWidgets.append(self.modeChangeWeightsButton)
		self.rightSideWidgets.append(self.modeSelectDirectionButton)
		self.rightSideWidgets.append(self.modeDelete)
		self.rightSideWidgets.append(self.startButton)
		self.rightSideWidgets.append(self.clearButton)


		self.canvas.bind("<Button-1>", self.canvasClick)

		self.canvas.grid(row=0, column=0, rowspan=10, columnspan=10)
		for i in range(len(self.rightSideWidgets)):
			self.rightSideWidgets[i].grid(row=i, column=10, columnspan=4)

		self.root.mainloop()


	def canvasClick(self, event):
		if self.mode == Visualizer.ADD:
			self.createVertex(event)

		elif self.mode == Visualizer.CHANGE_PATH:
			self.selectVertex(event)

			if (self.selectedV1 != None) and (self.selectedV2 != None):
				color = "black"
				if self.setPath(self.selectedV1, self.selectedV2):
					color = "black"
				else:
					color = "white"

				Visualizer.drawPath(self.canvas, self.selectedV1, self.selectedV2, color)
				Visualizer.drawVertex(self.canvas, self.selectedV1)
				Visualizer.drawVertex(self.canvas, self.selectedV2)
				self.selectedV1 = None
				self.selectedV2 = None

		elif self.mode == Visualizer.SELECT_DIRECTION:
			self.selectVertex(event)

			if self.selectedV1 != None:
				self.start = self.selectedV1
				self.fromLabel['text'] = "From: " + str(self.selectedV1.i)


			if self.selectedV2 != None:
				self.end = self.selectedV2
				self.toLabel['text'] = "To: " + str(self.selectedV2.i)

			if (self.selectedV1 != None) and (self.selectedV2 != None):
				Visualizer.drawVertex(self.canvas, self.selectedV1)
				Visualizer.drawVertex(self.canvas, self.selectedV2)
		
		elif self.mode == Visualizer.DELETE:
			v1 = self.findVertex(event)
			for v2 in v1.adjacent:
				v2.adjacent.remove(v1)

			v1.adjacent.clear()
			self.vertex.remove(v1)
			self.clearCanvas()
			Visualizer.drawAllPath(self.canvas, self.vertex)
			Visualizer.drawAllVertex(self.canvas, self.vertex)




	def createVertex(self, event):
		vertex = Vertex(event.x, event.y, self.vertexCounter)

		self.vertex.append(vertex)
		self.vertexCounter += 1
		Visualizer.drawVertex(self.canvas, vertex)

	def reset(self):
		self.clearCanvas()
		self.selectedV1 = None
		self.selectedV2 = None
		self.start = None
		self.end = None
		self.vertex = []
		self.path = []
		self.vertexCounter = 0

	def clearCanvas(self):
		self.canvas.delete("all")
		

	def setAddMode(self):
		self.mode = Visualizer.ADD
		self.modeLabel["text"] = "Mode: ADD"

	def setChangeWeightsMode(self):
		self.selectedV1 = None
		self.selectedV2 = None
		self.mode = Visualizer.CHANGE_PATH
		self.modeLabel["text"] = "Mode: CHANGE_PATH"

	def setSelectDirectionMode(self):
		self.selectedV1 = None
		self.selectedV2 = None
		self.mode = Visualizer.SELECT_DIRECTION
		self.modeLabel["text"] = "Mode: SELECT_DIRECTION"

	def setDeleteMode(self):
		self.mode = Visualizer.DELETE
		self.modeLabel["text"] = "Mode: DELETE"

	def selectVertex(self, event):
		if (self.selectedV1 is None):
			self.selectedV1 = self.findVertex(event)

		elif (self.selectedV2 is None):
			self.selectedV2 = self.findVertex(event)

		if (self.selectedV1 is not None):
			Visualizer.drawVertex(self.canvas, self.selectedV1, "white", "red")
		
		if (self.selectedV2 is not None):
			Visualizer.drawVertex(self.canvas, self.selectedV2, "white", "red")

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


	def setPath(self, v1, v2):
		add = True
		if (v2 not in v1.adjacent):
			v1.adjacent.append(v2)
		else:
			add = False
			v1.adjacent.remove(v2)

		if (v1 not in v2.adjacent):
			v2.adjacent.append(v1)
		else:
			add = False
			v2.adjacent.remove(v1)

		for v in self.vertex:
			print(v.i, end=" => ")
			print(v.adjacent)
		print()
		return add

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
		for v1 in vertex:
			for v2 in v1.adjacent:
				canvas.create_line(v1.x, v1.y, v2.x, v2.y)

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



Visualizer()
