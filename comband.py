import random

class ComBand():
	def __init__(self,gamma=0.3,K=[1,2,3],k=1):
		self.weights = []
		self.probs = []
		self.actions = []
		self.gamma = gamma
		self.k = k
		self.CKk = choose(len(K),k)
		self.C = self.gamma / self.CKk
		self.prob_updated = False

		for i in range(0, self.CKk):
			self.weights.append(1)
			self.probs.append(0)


	def info(self):
		print ("weights are : ")
		for i in range(0,len(self.weights)) :
			print ("weight %d = %f , prob = %f" % (i,self.weights[i], self.probs[i]) )

	def next_actions(self):
		if (not self.prob_updated ):
			update_probabilities()
		actions = []
		while ( len(actions) < self.k):
			actions = actions + random.choices(range(0,self.CKk),weights=self.probs,k=self.k-len(actions))
			print(actions)
			actions = list(set(actions))

		self.prob_updated = False
		self.actions = actions
		return actions

	def receive_rewards(self,rewards):
		if ( len(rewards) != len(self.actions) ):
			raise Exception('rewards list size should be same as actions list size.')


	def update_probabilities(self):
		sum = 0
		for weight in self.weights :
			sum = sum + weight
		for i in range(0,len(self.weights)) :
			pr = (1 - self.gamma)*self.weights[i]/sum + self.C
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

if __name__ == '__main__':
	print ( choose(4,2))
