from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import csv
import random
import os

""" Data Format: 
carLocX_0, carLocY_0, carDirX_0, carDirY_0, carVelX_0, carVelY_0,
carLocX_1, carLocY_1, carDirX_1, carDirY_1, carVelX_1, carVelY_1,
throttle, steer, time
 """
def identicalLists(A, B):
		for i, a in enumerate(A):
			if a != B[i]:
				return False
		return True

class GroundLearner:

	def __init__(self, dirName):
		self.dirName = dirName
		self.readCSV()
	
	def getFeatures(self, row):
		#ignore the ball; carPrevState is 6:15, carAfterState is 21:30
		f = row[6:15]
		f.extend(row[21:30])
		return f

	def getTargets(self, row):
		#instructions are 30:32, time is 32.
		return row[30:33]

	def getInstructions(self, row):
		return row[30:32] #30: throttle, 31: steer

	def getTime(self, row):
		return row[32]

	def readCSV(self):
		self.features = []
		self.targets = []
		dataFormat = ""
		for f in os.listdir(self.dirName):
			fileName = self.dirName + f
			with open(fileName, 'r') as csvFile:
				print("Reading inputs from ", fileName)
				dataReader = csv.reader(csvFile, lineterminator='')
				dataFormat = next(dataReader)

				for c, row in enumerate(dataReader):
					row = [float(i) for i in row]

					t = self.getTargets(row)
					f = self.getFeatures(row)
					if (f[2] < 20 and f[2] > 14 and f[11] < 20 and f[11] > 14):
						#print("only ground driving")
						if (random.uniform(0,1) > 0.5):
							self.features.append(f)
							self.targets.append(t)

				#for i, f in enumerate(features):
				#	print("Feature ", i, ": ", f, "\nMapsTo: Target: ", targets[i], "\n\n")
			print("Length  of features, targets is: ", len(self.features), " - ", len(self.targets))
		print(dataFormat)
	def trainMLPRegressor(self):
		mapping = list(zip(self.features, self.targets))
		random.shuffle(mapping)
		print("Running MLP Regression\n\n")

		#print(features)
		#print("\n\n\n\n\n\n\n\n\n\n\n")

		f_train, f_test, t_train, t_test = train_test_split(self.features, self.targets)

		#for i,a in enumerate(t_train):
		#	if i % 100 ==0:
		#		print("Split target: ", a)

		print("Size of training set is: f, t: ", len(f_train), ", ", len(t_train))
		print("Size of testing set is: f, t: ", len(f_test), ", ", len(t_test))
		dataScaler = StandardScaler()
		dataScaler.fit(f_train)

		f_train = dataScaler.transform(f_train)
		f_test = dataScaler.transform(f_test)


		self.mlp = MLPRegressor(early_stopping=True, hidden_layer_sizes=(64,16,8), max_iter=10000)

		self.mlp.fit(f_train, t_train)

		print("Training score: ", self.mlp.score(f_train, t_train))
		print("Testing score: ", self.mlp.score(f_test, t_test))
		return self.mlp

	def trainLinearRegressor(self):
		mapping = list(zip(self.features, self.targets))
		random.shuffle(mapping)
		print("Running Linear Regression\n\n")

		#print(features)
		#print("\n\n\n\n\n\n\n\n\n\n\n")

		f_train, f_test, t_train, t_test = train_test_split(self.features, self.targets)

		print("Size of training set is: f, t: ", len(f_train), ", ", len(t_train))
		print("Size of testing set is: f, t: ", len(f_test), ", ", len(t_test))
		dataScaler = StandardScaler()
		dataScaler.fit(f_train)

		f_train = dataScaler.transform(f_train)
		f_test = dataScaler.transform(f_test)

		self.lr = LinearRegression()
		self.lr.fit(f_train, t_train)

		#predictions = lr.predict(f_test)
		print("Training score: ", self.lr.score(f_train, t_train))
		print("Testing score: ", self.lr.score(f_test, t_test))
		return self.lr





def main():

	#fileName = "MovementData/1541104299.059675.csv" #example file (700 lines only) with uniform instructions
	fileName = "MovementData/1541114893.1472585.csv" #example file (7000 records) with uniform^2 instructions
	dirName = "MovementData/"

	gl = GroundLearner(dirName)
	gl.trainLinearRegressor()
	gl.trainMLPRegressor()


if __name__ == "__main__":
    main()