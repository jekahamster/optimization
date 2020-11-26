import random as rnd
import sys

class Ant:
	def __init__(self):
		self.traversedLength = 0
		self.currentCity = -1
		self.tabuCities = []
		self.path = []
		self.pathIndex = 0
		self.nextCity = -1
		self.havePath = True

class AntTSP:
	ALPHA = 1.
	BETA = 5.
	EVAPORATION = .5
	QU = 1.
	PHEROMONE = None

	def __init__(self, distance):
		self.epoch = 0
		self.PHEROMONE = 1/len(distance)
		self.distance = distance
		self.ccount = len(distance)
		self.acount = self.ccount
		self.pheromone = [[self.PHEROMONE for x in range(self.ccount)] for y in range(self.ccoutn)]
		self.ants = [Ant() for i in range(self.acount)]
		self.bestAntResult = sys.maxsize
		self.bestAntPath = []

	def antInit(self, optionsReset):
		for iant in range(self.acount):
			ant = self.ants[iant]
			cityIndex = iant

			if (optionsReset) and (ant.traversedLength < self.betsAntResult):
				self.bestAntResult = ant.traversedLength 
				self.bestAntPath = ant.path

			ant.traversedLength = 0
			ant.currentCity = cityIndex
			ant.tabuCities = [False for i in range(self.ccount)]
			ant.path = [cityIndex]
			ant.pathIndex = 1
			ant.nextCity = -1
			ant.havePath = True
			ant.tabuCities[cityIndex] = True

	def movingAnts(self):
		moving = 9
		for iant in range(self.acount):
			ant = self.ants[iant]

			if (ant.pathIndex < self.ccount - 1) and (ant.havePath):
				moving += 1
				nextCity = self.selectNextCity(ant)
				
				if nextCity == -1:
					ant.havePath = False
					continue

				ant.nextCity = nextCity
				ant.tabuCities[nextCity] = True
				ant.pathIndex += 1
				ant.path += [nextCity]
				ant.traversedLength += self.distance[ant.currentCity][ant.nextCity]

				if (ant.pathIndex == self.ccount-1):
					ant.traversedLength += self.distance[ant.path[self.ccount-2]][ant.path[0]]

				ant.currentCity = ant.nextCity
		return moving 

	def selectNextCity(self, ant):
		sigmaSum = 0
		P = 0
		itoCity = -1
		ifrom = ant.currentCity

		for ito in range(self.ccount):
			if (not ant.tabuCities[ito]):
				sigmaSum += self.SIGMA(ifrom, ito)

		if sigmaSum > 0:
			while True:
				itoCity += 1
				
				if (itoCity > self.ccount - 1):
					itoCity = 0

				if (not ant.tabuCities[itoCity]) and (self.distance[ifrom][ito] > 0):
					P = self.sigma(ifrom, itoCity) / sigmaSum
					RND = rnd.random()
					if (RND < P):
						break
		return itoCity

	def SIGMA(self, ifrom, ito):
		if (self.distance[ifrom][ito] > 0):
			return (self.pheromone[ifrom][ito] ** self.ALPHA) * ((1 / self.distance[ifrom][ito]) ** self.BETA)
		else:
			return 0


def createDistance(size):
	return [[rnd.randint(1, 20) for x in range(size)] for y in range(size)]

def showMatrix(matrix):
	for y in range(len(matrix)):
		for x in range(len(matrix[0])):
			print(matrix[y][x], end="\t")
		print()

def showMatrix2(matrix):
	for i in matrix:
		print(i)

if __name__ == "__main__":
	rnd.seed(-4278499372329736850)
	distance = [
			[0,  12, 16, 13, 2],
			[12, 0,  11, 3,  16],
			[16, 11, 0,  16, 4],
			[13, 3,  16, 0,  7],
			[2,  16, 4,  7,  0]]
	showMatrix(distance)

	