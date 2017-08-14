#here we will cross correlate the speed to ROIs and find signficance with a shuffle test
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import numpy as np
number_of_shuffles = 100


f = open('C_df_filtered.txt', 'r')
rawData = f.read()
f.close()

ROIs = map(lambda x: 
	map(lambda y: float(y), x.strip().split(',')), 
	rawData.strip().split('\n'))

f = open('speed.txt', 'r')
rawSpeed = f.read()
f.close()

speed = map(float, rawSpeed.strip().split())

def analyzeROI(ROInum):
	neuron = ROIs[ROInum]
	correlationVal=scipy.stats.pearsonr(neuron, speed)[0]
	tempCorVals=0
	tempNeuron=neuron[:]
	lessThanCounter=0.0
	

	if math.isnan(correlationVal):
		percentile=correlationVal

		significance=0
	else:
		for x in range(number_of_shuffles):
			random.shuffle(tempNeuron)
			tempCorVal=scipy.stats.pearsonr(speed,tempNeuron)[0]
			
			if tempCorVal <= correlationVal:
				lessThanCounter += 1.0

		percentile=lessThanCounter / number_of_shuffles
		if percentile < .05:
			significance = -1
		elif percentile > .95:
			significance = 1
		else:
			significance = 0

	return [ROInum, correlationVal, percentile, significance]

analyzedROIs = sorted(map(analyzeROI,range(len(ROIs))), key=lambda x: x[2])

f = open('allROIsShuffleTest.txt', 'w')
for line in analyzedROIs:
	f.write(str(line)[1:-1]+'\n')
f.close()

goodNeurons = []
for ROI in analyzedROIs:
	if ROI[2]>.99 and ROI[1]>0:
		goodNeurons.append(ROI[0])

f = open('correlatedNeuronsShuffleTest.txt', 'w')
f.write(str(goodNeurons)[1:-1]+'\n')
f.close()
"""


ROIcors = []
for ROI in data:
	ROIcors.append(scipy.stats.pearsonr(PC,ROI)[0])

from skimage import data
from skimage import filters
thresh = filters.threshold_otsu(np.array([ROIcors]))

correlatedROIs = []
for x in range(len(ROIcors)):
	if ROIcors[x] > thresh:
		correlatedROIs.append(x)

f = open('correlatedROIsOtsu.txt','w')
f.write(str(correlatedROIs)[1:-1])
f.close()

print correlatedROIs"""
