import numpy

class KMeans():

	def __init__(self,N):

		self.xVectors = []
		self.classes = {}
		self.N = N
		self.uMatrix = []

	def addXVector(self,xVector):

		self.xVectors.append(xVector)

	def addClass(self,c):

		self.classes[c.getClassName()] = c

	def setClasses(self,classes):

		self.classes = classes

	def getClasses(self):

		return self.classes

	def setUMatrix(self,matrix):

		self.uMatrix = matrix

	def doTraining(self,epsilonLimit,b):

		xNumber = len(self.xVectors)
		cNumber = len(self.classes)
		bBreak = False
		i = 1
		while not bBreak:

			bBreak = True
			for key in self.classes:
				delta = self.calculateV(self.classes[key],b)
				bBreak = bBreak and (delta<epsilonLimit)
			print ">>>>>>>>>>>>>>>>>>Iteracion ", i
			for key in self.classes:
				print ">>> Vector v de la clase ", self.classes[key].getClassName()
				print  self.classes[key].getVCenter()
			i+=1
			self.updateUMatrix(b)
			print ">>> Matriz U"
			''' set_printoptions for numpy configures the formatter for printing numpy matrix
				linewidth=nan sets no width limits for array lines '''
			numpy.set_printoptions(linewidth=numpy.nan)
			print numpy.transpose(self.uMatrix)
			''' Resets the formatter '''
			numpy.set_printoptions()
		
	def calculateV(self,c,b):

		newV = numpy.zeros((self.N,1),dtype=float)
		newVDividend = numpy.zeros((1,self.N),dtype=float)
		newVDivisor = 0
		
		for i in range(len(self.xVectors)):
			'''dividend is a temp var equals P(uij/xj)'''
			dividend = self.uMatrix[i][c.getIndex()]
			newVDividend = numpy.add(newVDividend, numpy.dot(numpy.power(dividend,b),self.xVectors[i]))
			'''divisor is a temp var equals P(uij/xj) '''
			divisor = self.uMatrix[i][c.getIndex()]
			newVDivisor = numpy.add(newVDivisor, numpy.power(divisor,b))

		newV = numpy.divide(newVDividend,newVDivisor)
		''' numpy.linalg.norm without an exponent parameter equals euclidean distance '''
		delta = numpy.linalg.norm(numpy.subtract(newV,c.getVCenter()))
		c.setVCenter(newV)

		return delta

	def calculateP(self,v1,v2,b):

		'''We calculate the dividend 1/dij ^ 1/b-1 '''
		dij = self.calculateEuclideanDistance2(v1,v2)
		dividend = (1/numpy.power(dij, (1/(b-1))))
		print dividend

		'''We calculate the divisor'''
		divisor = 0
		for key in self.classes:

			drj = self.calculateEuclideanDistance2(v2,self.classes[key].getVCenter())
			divisor +=  (1/numpy.power(drj, (1/(b-1))))
		print divisor
		return dividend/divisor

	def calculateEuclideanDistance2(self,v1,v2):

		return numpy.power(numpy.linalg.norm(numpy.subtract(v2,v1)),2)

	def updateUMatrix(self,b):

		'''We update the values of the fuzzy U matrix for the next iteration'''

		for i in range(len(self.uMatrix)):
			for key in self.classes:
				self.uMatrix[i][self.classes[key].getIndex()] = self.calculateP(self.classes[key].getVCenter(),self.xVectors[i],b)

	def clasifyEuclideanDistance(self,vector):
		
		className= None
		mini = float('inf')

		print ">>>> Clasificacion de distancia vector ",vector
		for key in self.classes:
			distance = self.calculateEuclideanDistance2(self.classes[key].getVCenter(),vector)
			print "Distancia a la clase ",self.classes[key].getClassName(), ": ",distance
			if(distance < mini):
				mini = distance
				className = key
		return className

	def clasifyProbability(self,vector,b):
		
		print ">>>> Clasificacion de probabilidad vector ",vector
		pVector=[]
		for key in self.classes:
			p = self.calculateP(self.classes[key].getVCenter(),vector,b)
			pVector.append(self.classes[key].getClassName() + " = "+str(p))

		return pVector
		
class Class():

	def __init__(self,xIndex,className):

		self.vCenter = []
		self.xIndex = xIndex
		self.className = className

	def getVCenter(self):

		return self.vCenter

	def setVCenter(self,vCenter):

		self.vCenter = vCenter

	def getClassName(self):

		return self.className

	def getIndex(self):

		return self.xIndex

if __name__ == "__main__":
	import sys
	clase1 = Class(0,"Clase 1")
	clase1.setVCenter([6.70,3.43])
	clase2 = Class(1,"Clase 2")
	clase2.setVCenter([2.39,2.94])

	kmedias = KMeans(2)

	matrix = [0.022,0.978,0.003,0.997,0.03,0.97,0.002,0.998,0.0,1.0,0.997,0.003,0.997,0.003,0.946,0.054,1.0,0.0,0.990,0.01]
	matrix = numpy.reshape(matrix,(10,2))
	kmedias.setUMatrix(matrix)

	kmedias.addClass(clase1)
	kmedias.addClass(clase2)

	kmedias.addXVector([1,1])
	kmedias.addXVector([1,3])
	kmedias.addXVector([1,5])
	kmedias.addXVector([2,2])
	kmedias.addXVector([2,3])
	kmedias.addXVector([6,3])
	kmedias.addXVector([6,4])
	kmedias.addXVector([7,1])
	kmedias.addXVector([7,3])
	kmedias.addXVector([7,5])

	kmedias.doTraining(epsilonLimit=0.02,b=2)
	
	print kmedias.clasifyEuclideanDistance([2,3])
	print kmedias.clasifyProbability([2,3],b=2)
	

	
