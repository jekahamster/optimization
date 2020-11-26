
import tkinter as tk
import random as rnd
import math
import time
from threading import Thread
from PIL import ImageTk, Image


energyStat = []

img = Image.open("map.png")

class Vertex:
	def __init__(self, x=None, y=None):
		self.x = x
		self.y = y

	def __repr__(self):
		return "({0}, {1})".format(self.x, self.y)



class AnnealingSimulator:
	
	@staticmethod
	def run(state, obj):
		canvas = obj.canvas

		global energyStat
		
		s1 = state
		t = 100
		while (t > 5):
			s2 = AnnealingSimulator.getNewSate(s1.copy())
			e1 = AnnealingSimulator.E(s1)
			e2 = AnnealingSimulator.E(s2)
			de = e2 - e1

			if (de > 0):
				p1 = 100*math.e**(-de/t)
				p2 = rnd.randint(1, 100)
				if (p1 > p2):
					s1 = s2
					
				else: 
					s1 = s1
			else:
				s1 = s2
				

			t = AnnealingSimulator.T(t, 0.99)
			energyStat.append(round(e2))

			obj.temperature_label['text'] = "T = " + str(round(t, 5))
			obj.energy_label['text'] = "E = " + str(round(e1, 5))
			AnnealingSimulator.updateCanvas(canvas, s1)
			time.sleep(0.01)

		energyStat.append(round(AnnealingSimulator.E(s1)))
		return s1

	@staticmethod
	def getNewSate(state):
		slen = len(state)
		r1 = 0
		r2 = 0

		while (r1 == r2):
			r1 = rnd.randint(1, slen-2)
			r2 = rnd.randint(1, slen-2)

		temp = state[r1]
		state[r1] = state[r2]
		state[r2] = temp

		return state

	@staticmethod
	def T(t, alpha):
		return t * alpha

	@staticmethod
	def E(state):
		res = 0
		for i in range(len(state)-1):
			p1 = state[i]
			p2 = state[i+1]
			res += ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

		return res

	@staticmethod
	def updateCanvas(canvas, state):
		canvas.delete("all")
		AnnealingSimulator.drawVP(canvas, state)

	@staticmethod
	def drawVP(canvas, state):
		for i in range(0, len(state)-1):
			p1 = state[i]
			p2 = state[i+1]

			canvas.create_line(p1.x, p1.y, p2.x, p2.y)
			x1 = p1.x - 5
			x2 = p1.x + 5
			y1 = p1.y - 5
			y2 = p1.y + 5
			canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
			x1 = p2.x - 5
			x2 = p2.x + 5
			y1 = p2.y - 5
			y2 = p2.y + 5
			canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

		p1 = state[0]
		p2 = state[len(state)-1]

		x1 = p1.x - 5
		x2 = p1.x + 5
		y1 = p1.y - 5
		y2 = p1.y + 5
		canvas.create_oval(x1, y1, x2, y2, fill="red", outline="red")
		x1 = p2.x - 5
		x2 = p2.x + 5
		y1 = p2.y - 5
		y2 = p2.y + 5
		canvas.create_oval(x1, y1, x2, y2, fill="red", outline="red")


class Vizualizator:
	brush_size = 5
	color = "black"

	def __init__(self):
		self.vertex = []

		right_side_widgets = []

		self.root = tk.Tk()
		self.root.title("Annealing Simulator")

		self.canvas = tk.Canvas(self.root, bg="white", width=800, height=800)

		
		self.temperature_label = tk.Label(text="T = ")
		self.energy_label = tk.Label(text="E = ")


		vertex_count_label = tk.Label(text="Vertex count")
		vertex_count_entry = tk.Entry()
		generate_button = tk.Button(text="Generate")
		simulate_button = tk.Button(text="Simulate", command=lambda: Thread(target=self.getPath, args=(), daemon=True).start())
		clear_canvas_button = tk.Button(text="Clear", command=self.clearCanvas)

		right_side_widgets.append(self.temperature_label)
		right_side_widgets.append(self.energy_label)
		right_side_widgets.append(vertex_count_label)
		right_side_widgets.append(vertex_count_entry)
		right_side_widgets.append(generate_button)
		right_side_widgets.append(simulate_button)
		right_side_widgets.append(clear_canvas_button)

		self.canvas.bind("<Button-1>", self.createVertex)
		

		self.canvas.grid(row=0, column=0, rowspan=10, columnspan=10)

		for i in range(len(right_side_widgets)):
			right_side_widgets[i].grid(row=i, column=10, columnspan=2)

		# temperature_label.grid(row=0, column=10, columnspan=2)
		# vertex_count_label.grid(row=1, column=10, columnspan=2)
		# vertex_count_entry.grid(row=2, column=10, columnspan=2)
		# generate_button.grid(row=3, column=10, columnspan=2)
		# simulate_button.grid(row=4, column=10, columnspan=2)
		# clear_canvas_button.grid(row=5, column=10, columnspan=2)

		self.drawMap()

		self.root.mainloop()

	def createVertex(self, event):
		self.vertex.append(Vertex(event.x, event.y))
		
		v = Vertex(event.x, event.y)
		self.drawVertex(v)

	def drawVertex(self, v):
		x1 = v.x - self.brush_size
		x2 = v.x + self.brush_size
		y1 = v.y - self.brush_size
		y2 = v.y + self.brush_size
		self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)


	def getPath(self):
		self.canvas.delete("all")
		global energyStat
		energyStat = []
		state = [v for v in self.vertex]
		s1 = state[0]
		sn = state[len(state)-1]
		so = state[1:len(state)-1]
		rnd.shuffle(so)
		state = [s1]+so+[sn]
		print("Before:", state)
		res = AnnealingSimulator.run(state, self)

		self.drawMap()

		AnnealingSimulator.drawVP(self.canvas, res)
		print("After:", res)
		print("EnergyStat:", energyStat)
		for e in energyStat:
			print(e)
		print("")


	def clearCanvas(self):
		self.canvas.delete("all")
		self.drawMap()
		self.vertex = []
		energyStat = []

	def drawMap(self):
		# return;
		self.canvas.image = ImageTk.PhotoImage(img)
		self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")



	 

Vizualizator()
