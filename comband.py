import random
import itertools
import math
import numpy as np
from scipy.special import binom


class ComBand():
	def __init__(self,gamma=0.3,K=[1,2,3],k=1):
		self.weights = []
		self.probs = []
		self.gamma = gamma
		self.k = k
		self.K = K
		self.CKk = int(binom(len(K),k))
		self.C = self.gamma / self.CKk
		self.actions = list(itertools.combinations(K , k))
		self.oneUdot1UT = []
		self.mu = -1*gamma*(len(K)-k)/(k*len(K)*(len(K)-1))

		for i in range(0, self.CKk):
			self.weights.append(1)
			self.probs.append(1/self.CKk)

		# generate 1U.1U^T
		for action in self.actions:
			tmp = self.oneU( action )

			self.oneUdot1UT.append(tmp.transpose().dot(tmp))

	def oneU(self, arr ):
		tmp = np.zeros((len(self.K)), dtype=int)[np.newaxis]
		for i in arr:
			tmp[0][self.K.index(i)] = 1

		return tmp

	def info(self):
		print ("weights are : ")
		for i in range(0,len(self.weights)) :
			print ("weight %d = %f and prob = %f for action -> %s" % (i,self.weights[i], self.probs[i], self.actions[i]) )

	def next_action(self):
		return self.actions[random.choices(range(0,self.CKk),weights=self.probs)[0]]

	def update_weights(self,rewards,action):
		if ( len(rewards) != self.k ):
			raise Exception('rewards list size should be same as actions list size.')

		P_t = np.zeros( (len(self.K), len(self.K)) )

		for i in range(0, self.CKk) :
			P_t = P_t + self.probs[i] * self.oneUdot1UT[i]

		l_t = ( self.k - sum(rewards) ) * self.oneU( action ).dot(P_t)

		for i in range(0, self.CKk):
			self.weights[i] = self.weights[i] * math.exp(self.mu*sum(l_t[0]*self.oneU(self.actions[i])[0]))


	def update_probabilities(self):

		for i in range(0,len(self.weights)) :
			pr = (1 - self.gamma)*self.weights[i]/sum(self.weights) + self.C
			self.probs[i] = pr
