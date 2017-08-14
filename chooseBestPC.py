#find best oPCA
NUMBER_SHUFFLES = 100


import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
import random
import timeit


f = open('C_df_oPCA_output.txt', 'r')
rawPCs = f.read()
f.close()

PCs = map(lambda x: 
	map(lambda y: float(y), x.strip().split(',')), 
	rawPCs.strip().split('\n'))




f = open('speed.txt', 'r')
rawSpeed = f.read()
f.close()

speed = map(float, rawSpeed.strip().split())

def analyzePC(PC):
	actualCor = scipy.stats.pearsonr(PC, speed)[0]
	tempPC = PC[:]
	numTimesActualCorGreater = 0.
	for _ in range(NUMBER_SHUFFLES):
		random.shuffle(tempPC)
		#print scipy.stats.pearsonr(tempPC, speed)[0]
		if actualCor > scipy.stats.pearsonr(tempPC, speed)[0]:
			numTimesActualCorGreater += 1.
	
	return actualCor, numTimesActualCorGreater / NUMBER_SHUFFLES



analyzedPCs = map(analyzePC,PCs)
validPCs = []
for x in range(len(analyzedPCs)):
	if analyzedPCs[x][1] > .95:
		validPCs.append([x, analyzedPCs[x][0]])

bestPC = sorted(validPCs, key=lambda x: x[1])[-1]

f = open('bestPC.txt','w')
f.write(str(bestPC)[1:-1])
f.close()