#here we will cross correlate the principal component
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

f = open('C_df_oPCA_output.txt', 'r')
rawPCs = f.read()
f.close()

PCs = map(lambda x: 
	map(lambda y: float(y), x.strip().split(',')), 
	rawPCs.strip().split('\n'))

f = open('C_df_filtered.txt', 'r')
rawData = f.read()
f.close()

data = map(lambda x: 
	map(lambda y: float(y), x.strip().split(',')), 
	rawData.strip().split('\n'))

#Choose your PC. I'm using 0 here. It needs to be chosen based on the activity of the mouse tho
f = open('bestPC.txt','r')
rawBestPC = f.read()
f.close()

bestPC = int(rawBestPC.strip().split(',')[0])
PC = PCs[bestPC]

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

print correlatedROIs
'''print thresh


plt.hist(ROIcors, bins='auto')  # plt.hist passes it's arguments to np.histogram
plt.plot([thresh,thresh],[0,20], lw=1, c='r')
plt.title("Histogram with 'auto' bins")
plt.show()
plt.close()'''

