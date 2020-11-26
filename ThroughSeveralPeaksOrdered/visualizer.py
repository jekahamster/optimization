import tkinter as tk
import json
import time

from threading import Thread

import ordered_graph
from vertex import Vertex
from pair import Pair
from model import Model

class Visualizer:

	vertexSize = 20
	vertexBorderWidth = 2


	def __init__(self):
		self.model = Model()
		self.graph = self.model.setGraph(ordered_graph.OrderedGraph())

		self.__currentMenuEvent = None

		self.selectedFirst = None
		self.selectedSecond = None
		self.currentSelected = None

		self.root = tk.Tk()
		self.root.title("Ant Colony")

		self.firstToSecondCheckboxVal = tk.BooleanVar()
		self.secondToFirstCheckboxVal = tk.BooleanVar()

		self.menu = tk.Menu(tearoff=0)
		self.menu.add_command(label="Select as first", command=self.selectAsFirstVertex)
		self.menu.add_command(label="Select as second", command=self.selectAsSecondVertex)
		self.menu.add_command(label="Cancel Selection", command=self.cancelSelection)
		self.menu.add_command(label="Remove Vertex", command=self.removeVertex)
		self.menu.add_command(label="Set as Begin", command=self.removeVertex)
		self.menu.add_command(label="Set as End", command=self.removeVertex)
		self.menu.add_command(label="Must visit", command=self.removeVertex)

		self.canvas = tk.Canvas(self.root, bg="white", width=800, height=800)

		self.selectedVertexFrame	= tk.Frame(self.root, borderwidth=2, relief="groove")
		self.firstVertexLabel 		= tk.Label(self.selectedVertexFrame, text="First Vertex")
		self.secondVertexLabel 		= tk.Label(self.selectedVertexFrame, text="Second Vertex")
		self.firstVertexEntry 		= tk.Entry(self.selectedVertexFrame)
		self.secondVertexEntry	 	= tk.Entry(self.selectedVertexFrame)
		self.firstToSecondCheckbox 	= tk.Checkbutton(self.selectedVertexFrame, text="First to second", var=self.firstToSecondCheckboxVal, onvalue=1, offvalue=0, command=self.changeRelation)
		self.secondToFirstCheckbox 	= tk.Checkbutton(self.selectedVertexFrame, text="Second to first", var=self.secondToFirstCheckboxVal, onvalue=1, offvalue=0, command=self.changeRelation)
		self.pathButtonsFrame		= tk.Frame(self.selectedVertexFrame)
		self.setFullPathButton 		= tk.Button(self.pathButtonsFrame, text="Set full path", command=self.setFullPath)
		self.clearPathButton 		= tk.Button(self.pathButtonsFrame, text="Clear path", command=self.removeAllPath)
		self.loadSaveButtonsFrame	= tk.Frame(self.root, borderwidth=2, relief="groove")
		self.saveGraphButton 		= tk.Button(self.loadSaveButtonsFrame, text="Save Graph")
		self.loadGraphButton		= tk.Button(self.loadSaveButtonsFrame, text="Load Graph")

		self.bestResultLabel 		= tk.Label(text="Best Result: None")
		self.startButton 			= tk.Button(text="start")
		self.clearButton 			= tk.Button(text="clear", command=self.reset)


		self.firstVertexLabel.grid(row=0, column=0, padx=20, pady=5)
		self.secondVertexLabel.grid(row=0, column=1, padx=20, pady=5)
		self.firstVertexEntry.grid(row=1, column=0, padx=20, pady=5)
		self.secondVertexEntry.grid(row=1, column=1, padx=20, pady=5)
		self.firstToSecondCheckbox.grid(row=2, column=0, columnspan=2)
		self.secondToFirstCheckbox.grid(row=3, column=0, columnspan=2)
		self.setFullPathButton.grid(row=0, column=0)
		self.clearPathButton.grid(row=0, column=1)
		self.pathButtonsFrame.grid(row=4, column=0, columnspan=2)



		self.saveGraphButton.grid(row=0, column=0, padx=20, pady=20)
		self.loadGraphButton.grid(row=0, column=1, padx=20, pady=20)


		self.rightSideWidgets = []
		self.rightSideWidgets.append(self.bestResultLabel)
		self.rightSideWidgets.append(self.selectedVertexFrame)
		self.rightSideWidgets.append(self.loadSaveButtonsFrame)
		self.rightSideWidgets.append(self.clearButton)


		self.canvas.bind("<Button-1>", self.canvasLeftClick)
		self.canvas.bind("<Button-3>", self.canvasRightClick)

		self.canvas.grid(row=0, column=0, rowspan=10, columnspan=10)
		for i in range(len(self.rightSideWidgets)):
			self.rightSideWidgets[i].grid(row=i, column=10, columnspan=4)

		self.root.mainloop()


	def canvasLeftClick(self, event):
		self.createVertex(event)


	def canvasRightClick(self, event):
		self.currentSelected = self.findVertex(event)
		self.__currentMenuEvent = event
		if not self.currentSelected is None:
			self.menu.post(event.x_root, event.y_root)

	def createVertex(self, event):
		vertex = self.model.appendVertex(event.x, event.y)
		self.drawVertex(vertex)

	def removeVertex(self):
		vertex = self.findVertex(self.__currentMenuEvent)
		self.model.removeVertex(vertex)
		self.updateCanvas()

	def reset(self):
		self.graph = self.model.setGraph(ordered_graph.OrderedGraph())
		self.selectedFirst = None
		self.selectedSecond = None
		self.currentSelected = None
		self.clearCanvas()

	def findVertex(self, event):
		minV = None
		minL = Visualizer.vertexSize+1

		for v in self.model.getAllVertex():
			dx = v.x - event.x
			dy = v.y - event.y
			l = ((dx)**2 + (dy)**2)**0.5
			if (l <= self.vertexSize) and (l < minL):
				minV = v
				minL = l

		return minV

	def selectAsFirstVertex(self):
		if self.selectedFirst is None:
			self.selectedFirst = self.currentSelected

		elif not self.selectedFirst is self.currentSelected:
			self.selectedFirst = self.currentSelected

		elif self.selectedFirst == self.currentSelected:
			self.selectedFirst = None

		self.firstVertexEntry.delete(0, tk.END)
		self.firstVertexEntry.insert(0, str(self.selectedFirst))
		self.getRelation()
		self.updateCanvas()

	def selectAsSecondVertex(self):
		if self.selectedSecond is None:
			self.selectedSecond = self.currentSelected

		elif not self.selectedSecond is self.currentSelected:
			self.selectedSecond = self.currentSelected

		elif self.selectedSecond == self.currentSelected:
			self.selectedSecond = None

		self.secondVertexEntry.delete(0, tk.END)
		self.secondVertexEntry.insert(0, str(self.selectedSecond))
		self.getRelation()
		self.updateCanvas()

	def cancelSelection(self):
		self.selectedFirst = None
		self.selectedSecond = None
		self.currentSelected = None
		self.firstToSecondCheckbox.deselect()
		self.secondToFirstCheckbox.deselect()
		self.firstVertexEntry.delete(0, tk.END)
		self.secondVertexEntry.delete(0, tk.END)
		self.updateCanvas()



	def getRelation(self):
		if (not self.selectedFirst is None) and (not self.selectedSecond is None):
			firstToSecond = self.model.hasPath(self.selectedFirst, self.selectedSecond)
			secondToFirst = self.model.hasPath(self.selectedSecond, self.selectedFirst)

			self.firstToSecondCheckboxVal.set(firstToSecond)
			self.secondToFirstCheckboxVal.set(secondToFirst)

			self.firstToSecondCheckbox["var"] = self.firstToSecondCheckboxVal
			self.secondToFirstCheckbox["var"] = self.secondToFirstCheckboxVal


	def changeRelation(self):
		if self.firstToSecondCheckboxVal.get():
			self.model.setPath(self.selectedFirst, self.selectedSecond)
		else:
			self.model.removePath(self.selectedFirst, self.selectedSecond)
		
		if self.secondToFirstCheckboxVal.get():
			self.model.setPath(self.selectedSecond, self.selectedFirst)
		else:
			self.model.removePath(self.selectedSecond, self.selectedFirst)

		self.updateCanvas()


	def setFullPath(self):
		self.model.setFullPath()
		self.updateCanvas()

	def removeAllPath(self):
		self.model.removeAllPath()
		self.updateCanvas()
	
	def updateCanvas(self):
		self.clearCanvas()
		self.drawAllPath()
		self.drawAllVertex()
		self.drawSelectedVertex()


	def drawAllVertex(self):
		for v in self.model.getAllVertex():
			x1 = v.x - Visualizer.vertexSize
			x2 = v.x + Visualizer.vertexSize
			y1 = v.y - Visualizer.vertexSize
			y2 = v.y + Visualizer.vertexSize
			self.canvas.create_oval(x1, y1, x2, y2, fill="white", 
				outline="black", width=Visualizer.vertexBorderWidth)
			self.canvas.create_text(v.x-10, v.y, 
				anchor=tk.W, text=v.i, font=("Courier", 15))

	def drawAllPath(self):
		for pair in self.model.getAllPath():
			self.drawPath(pair.first, pair.second)

	def drawVertex(self, vertex, vertexColor="white", vertexBorder="black"):
		x1 = vertex.x - Visualizer.vertexSize
		x2 = vertex.x + Visualizer.vertexSize
		y1 = vertex.y - Visualizer.vertexSize
		y2 = vertex.y + Visualizer.vertexSize

		self.canvas.create_oval(x1, y1, x2, y2, fill=vertexColor,
			outline=vertexBorder, width=Visualizer.vertexBorderWidth)
		self.canvas.create_text(vertex.x-10, vertex.y,
			anchor=tk.W, text=vertex.i, font=("Courier", 15))

	def drawPath(self, v1, v2, color="black"):
		if v1.x < v2.x:
			x1 = v1.x + Visualizer.vertexSize/2 + Visualizer.vertexBorderWidth
			x2 = v2.x - Visualizer.vertexSize/2 - Visualizer.vertexBorderWidth
		else:
			x1 = v1.x - Visualizer.vertexSize/2 - Visualizer.vertexBorderWidth
			x2 = v2.x + Visualizer.vertexSize/2 + Visualizer.vertexBorderWidth

		if v1.y < v2.y:
			y1 = v1.y + Visualizer.vertexSize/2 + Visualizer.vertexBorderWidth
			y2 = v2.y - Visualizer.vertexSize/2 - Visualizer.vertexBorderWidth
		else:
			y1 = v1.y - Visualizer.vertexSize/2 - Visualizer.vertexBorderWidth
			y2 = v2.y + Visualizer.vertexSize/2 + Visualizer.vertexBorderWidth

		self.canvas.create_line(x1, y1, x2, y2, fill=color, arrow=tk.LAST, arrowshape="15 20 10")

	def drawSelectedVertex(self):
		if not self.selectedFirst is None:
			self.drawVertex(self.selectedFirst, vertexBorder="red")

		if not self.selectedSecond is None:
			self.drawVertex(self.selectedSecond, vertexBorder="red")



	def clearCanvas(self):
		self.canvas.delete("all")
