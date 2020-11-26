import time
import random as rnd 
from colorama import * 


init(autoreset=True)

class Ant:
	def __init__(self):
		self.traversed_length = 0
		self.current_city = -1
		self.tabu_cities = []
		self.path = []
		self.path_index = 0
		self.next_city = -1

class AntTSP:
	ALPHA = 1.
	BETA = 5.
	EVAPORATION = .5
	QU = 1.
	PHEROMONE = None

	def __init__(self, ccount):
		self.PHEROMONE = 1 / ccount
		self.current_epoch = 0
		self.ccount = ccount
		self.acount = ccount
		self.distance = []
		self.pheromone = []
		self.ants = []
		self.bets_ant_index = -1
		self.best_ant_result = 9999
		self.best_ant_path = []

		self.distance = [[rnd.randint(1, 20) for x in range(ccount)] for y in range(ccount)]
		for i in range(ccount):
			self.distance[i][i] = 0
		self.pheromone = [[self.PHEROMONE for x in range(ccount)] for y in range(ccount)]
		self.ants = [Ant() for i in range(self.acount)]

		showMatrix(self.distance)

	def antInit(self, option_reset = False):
		for iant in range(self.acount):
			ant = self.ants[iant]
			city_index = iant

			if option_reset and ant.traversed_length < self.best_ant_result:
				self.best_ant_result = ant.traversed_length
				self.bets_ant_index = iant
				self.best_ant_path = ant.path

			ant.traversed_length = 0
			ant.current_city = city_index
			ant.tabu_cities	= [False for i in range(self.ccount)]
			ant.path = []
			ant.path_index = 1
			ant.next_city = -1 

			ant.path.append(city_index)
			ant.tabu_cities[city_index] = True

	def movingAnts(self):
		moving = 0 
		for iant in range(self.ccount):
			ant = self.ants[iant]
			if (ant.path_index < self.ccount-1):	# пртому что мы проходим все города и не возвращаемся обратно. Для этого мы вручную вписали условие
				moving += 1
				ant.next_city = self.selectNextCity(ant)
				ant.tabu_cities[ant.next_city] = True
				ant.path_index += 1
				ant.path.append(ant.next_city)
				ant.traversed_length += self.distance[ant.current_city][ant.next_city]
				if (ant.path_index == self.ccount-1):
					ant.traversed_length += self.distance[ant.path[self.ccount-2]][ant.path[0]]	# -2, а не -1 потому что у мы не возврщаемся в начальный город

				ant.current_city = ant.next_city
		return moving


	def selectNextCity(self, ant):
		sigma_sum = 0
		P = 0
		ito_city = 0
		ifrom = ant.current_city


		print(Fore.RED + Back.WHITE + "Start selectNextCity")


		temp_sigma_path = ""
		temp_index_path = "" 
		for ito in range(self.ccount):
			if (not ant.tabu_cities[ito]):
				sigma_sum += self.SIGMA(ifrom, ito)
				temp_sigma_path += str( self.SIGMA(ifrom, ito) ) + " -> "
				temp_index_path += str( ito ) + " -> " 

		print("SigmaSumPath:", temp_sigma_path)
		print("IndexPath:", temp_index_path)
		print("SigmaSum:", sigma_sum)

		if sigma_sum > 0:
			while (True):
				ito_city += 1
				if (ito_city >= self.ccount):			# FIXED. not self.ccount-1 -> self.ccoutn !!!!
					ito_city = 0
					print("Back Index to 0")
					print()

				if (not ant.tabu_cities[ito_city]):
					print("Index:", ito_city)
					P = self.SIGMA(ifrom, ito_city) / sigma_sum
					RND = rnd.random()
					print("P =", round(P, 10), 0 < P, P < 1)
					print("RND =", RND)
					print("RND > P", RND > P)
					if (RND < P):
						break


		print()
		print()
		return ito_city


	def SIGMA(self, ifrom, ito):
		if (self.distance[ifrom][ito] > 0):
			return (self.pheromone[ifrom][ito] ** self.ALPHA) * ((1 / self.distance[ifrom][ito]) ** self.BETA)
		else:
			return 0

	def updatePheromone(self):
		for ifrom in range(self.ccount):
			for ito in range(self.ccount):
				if (ifrom != ito):
					self.pheromone[ifrom][ito] *= (1-self.EVAPORATION)
					if (self.pheromone[ifrom][ito] < 0):
						self.pheromone[ifrom][ito] = self.PHEROMONE
						

		for iant in range(self.acount):
			ant = self.ants[iant]

			for i in range(self.ccount-2):
				if (i < self.ccount-1):
					ifrom = ant.path[i]
					ito = ant.path[i+1]
				else:
					ifrom = ant.path[i]
					ito = ant.path[0]
				print("Trav Len:", ant.traversed_length)
				print("Path:", ant.path)
				self.pheromone[ifrom][ito] += (self.QU / ant.traversed_length)
				self.pheromone[ito][ifrom] = self.pheromone[ifrom][ito]

		for ifrom in range(self.ccount):
			for ito in range(self.ccount):
				self.pheromone[ifrom][ito] *= self.EVAPORATION				

	def run(self, epochs):
		while (self.current_epoch <= epochs):
			self.current_epoch += 1
			if self.current_epoch == 1:
				self.antInit(False)
			else:
				if (self.movingAnts() == 0):
					self.updatePheromone()
					self.antInit(True)

		print("Best result:", self.best_ant_result)
		print("Best path:", self.best_ant_path)


def showMatrix(matrix):
	for y in matrix:
		for x in y:
			print(x, end="\t")
		print()

def f():
	print(1)
	return True

if __name__ == "__main__":
	
	colony = AntTSP(10)
	colony.run(10)