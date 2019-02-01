import math
import random

class Hedge():
	def __init__(self,epsilon=0.1,N=4):
		self.weights = []
		self.N = N
		self.epsilon = epsilon

		for i in range(0,self.N) :
			self.weights.append(1)

	
	def info(self):
		print ("weights are : ")
		s = sum(self.weights)
		for i in range(0,self.N) :
			print ("weight %d = %f , prob = %f " % (i,self.weights[i], self.weights[i]/s ))

	def next_action(self):
		return random.choices(range(0,self.N),weights=self.weights)[0]

	def update_weights(self,rewards):
		if ( len(rewards) != self.N ):
			raise Exception('rewards list size should be same as actions list size.')

		for i in range(0, self.N):
			self.weights[i] = self.weights[i] * math.exp(self.epsilon*rewards[i])
