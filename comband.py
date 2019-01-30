import random
import itertools
import numpy as np

class ComBand():
	def __init__(self,gamma=0.3,K=[1,2,3],k=1):
		self.weights = []
		self.probs = []
		self.actions = []
		self.gamma = gamma
		self.k = k
		self.K = K
		self.CKk = choose(len(K),k)
		self.C = self.gamma / self.CKk
		self.prob_updated = False
		self.actions = list(itertools.combinations(K , k))
		self.oneUdot1UT = []


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
		if (not self.prob_updated ):
			update_probabilities()

		action_index = random.choices(range(0,self.CKk),weights=self.probs)

		self.prob_updated = False

		return self.actions[action_index[0]]

	def update_weights(self,rewards,action):
		if ( len(rewards) != self.k ):
			raise Exception('rewards list size should be same as actions list size.')

		P_t = np.zeros( (len(self.K), len(self.K)) )

		for i in range(0, self.CKk) :
			P_t = P_t + self.probs[i] * self.oneUdot1UT[i]

		l_t = ( self.k - sum(rewards) ) * self.oneU( action ).dot(P_t)

		print(l_t)


	def update_probabilities(self):

		for i in range(0,len(self.weights)) :
			pr = (1 - self.gamma)*self.weights[i]/sum(self.weights) + self.C
			self.probs[i] = pr

		self.prob_updated = True


def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0
