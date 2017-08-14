import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
ThresholdForMax = .05



f = open('C_df_filtered2s.txt', 'r')
rawData = f.read()
f.close()

ROIs = map(lambda x: 
		map(lambda y: float(y), x.strip().split(',')), 
	rawData.strip().split('\n'))


f = open('correlatedROIsOtsu.txt','r')
rawCorrelated = f.read()
f.close()

correlatedROIs = map(int,rawCorrelated.strip().split(','))



f = open('runEpochs.txt','r')
rawEpochs = f.read()
f.close()

runEpochs = map(lambda x: 
				map(lambda y: int(y), x.strip().split(',')), 
			rawEpochs.strip().split('\n'))

def differences(t):
	return [j - i for i, j in zip(t[:-1], t[1:])]
	
def findTimeOFMaximumOfRunEpochs(ROI):
	ROIDifferences = differences(ROI)
	

	ROIwithTimes = []
	for x in xrange(len(ROIDifferences)):
		ROIwithTimes.append([x, ROIDifferences[x]])
	def timeOfMaxRunOfEpoch(interval):
		ROIinterval = ROIwithTimes[interval[0]:interval[1]]
		sortedROIinterval = sorted(ROIinterval, key  = lambda x: x[1])
		if sortedROIinterval[-1][0] >= ThresholdForMax:
			return [sortedROIinterval[-1][0],sortedROIinterval[-1][0]-interval[0]]
		else:
			return [None, None]


	ROIOnsets = np.array(map(timeOfMaxRunOfEpoch,runEpochs)).transpose()
	return [[np.median(filter(lambda x: x!= None, ROIOnsets[1]))], ROIOnsets[0].tolist()]



roiNUMs = range(len(ROIs))
onsets = np.array(map(findTimeOFMaximumOfRunEpochs,ROIs)).transpose().tolist()

ROIonsets = onsets[1]
medianOnsets = np.array([roiNUMs,reduce(lambda x, y: x+y, onsets[0])]).transpose().tolist()

parsedMedianOnsets = []
for x in correlatedROIs:
	parsedMedianOnsets.append(medianOnsets[x])

sortedMedianOnsets = sorted(parsedMedianOnsets,key=lambda x: x[1])
ROIOrder = map(int,np.array(sortedMedianOnsets).transpose().tolist()[0])
ROIonsetsForPlot = []
for x in ROIOrder:
	ROIonsetsForPlot.append(ROIonsets[x])

def makePlot(ROIsForPlot):
	def addNeuronNum(ROI,num):
		for x in range(len(ROI)):
			ROI[x] = [ROI[x], num]
		return ROI

	allROIs = []
	for x in range(len(ROIsForPlot)):
		allROIs.append(addNeuronNum(ROIsForPlot[x], x+1))

	allROIsPlotting = reduce(lambda x, y: x+y, allROIs)

	Xss,Yss = np.array(allROIs).transpose().tolist()
	#for i in range(len(Xss)):
	#model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
	slopes = []
	'''for i in range(len(Xss)):
		model_ransac = linear_model.LinearRegression()

		model_ransac.fit(map(lambda a: [a], Xss[i]), Yss[i])
		tempYIntercept = model_ransac.predict([0])[0]
		tempSlope = (model_ransac.predict([1])[0]-tempYIntercept)/1
		slopes.append(tempSlope)
	
	print np.median(slopes)
'''



	'''x,y = np.array(allROIsPlotting).transpose().tolist()
	plt.scatter(x, y, alpha=0.5)
	plt.show()
	plt.close()'''

	f = open('XssForRegression.txt','w')
	for x in Xss:
		f.write(str(x)[1:-1] + '\n')
	f.close()

	f = open('YssForRegression.txt','w')
	for y in Yss:
		f.write(str(y)[1:-1] + '\n')
	f.close()


f= open('ROIOrder.txt','w')
f.write(str(ROIOrder)[1:-1])
f.close()
 
makePlot(ROIonsetsForPlot)














