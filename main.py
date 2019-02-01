import filePlacement as fp
import requests as req
import timer
import time
import comband
import hedge
import random
import numpy as np
#import itertools

#print( list(itertools.combinations(range(1,4), 2)))

# X = fp.FilePlacement()

#X.show_all()

hg = hedge.Hedge(epsilon=0.1,N=5)

hg.info()
total = np.zeros(hg.N, dtype=int)

rewards=[0.1,0.2,0.3,0.4,0.5]

for i in range(1,7000):
	action = hg.next_action()
	total[action] += 1
	hg.update_weights(rewards=rewards)

hg.info()
print (total)

exit(0)

cb = comband.ComBand(K=[1,2,3,4,5,6],k=2)
a = [6207, 6254, 6285, 6512, 6680, 6247, 6436, 6694, 6922, 6698, 6770, 7006, 6970, 7073,7246]

print (a)


X_t = np.array([0,0.1,0.1,0.1,0.5,0.5,0.5])
total = np.zeros((cb.CKk), dtype=int)

for i in range(0,100000):
	cb.update_probabilities()

	action,index = cb.next_action()
	total[index] += 1
	print("%dth, %s" % (i,action))

	cb.update_weights(X_t[action],action)

	# cb.info()

cb.info()
print (total)

b = np.sum(cb.actions,axis=1)
print (b)

t = np.zeros(12, dtype=int)

for i in range (3,12):
	for j in range(0,len(b)):
		if i == b[j]:
			t[i] += total[j]

print (t)


exit(0)

R = req.Requests()
R.show_all()

#print (X.request_cache_hits([1,3,5,7],2))

t = timer.MyTimer(5)
t.set_interval(R.update_req)
time.sleep(3)
print (R.get_car_req(3))
t.stop_intervals()
