#find run epochs
import operator
import numpy as np

framesPerSecond = 30.2 #frames/second
secondsRequiredToBeEpoch = 2 # secs
maximumTimeBetweenToAllowMerge = 1 #secs


f = open('speed.txt', 'r')
rawSpeed = f.read()
f.close()
runningThresh = 1

speed = map(float, rawSpeed.strip().split())
fastInstances = []
start = True
for x in range(len(speed)):
	if speed[x] > runningThresh:
		fastInstances.append(x)

def group(L):
    first = last = L[0]
    for n in L[1:]:
        if n - 1 == last: # Part of the group, bump the end
            last = n
        else: # Not part of the group, yield current group and start a new
            yield first, last
            first = last = n
    yield first, last # Yield the last group



runEpochs = list(group(fastInstances))
epochsToMerge = []
'''for x in range(len(runEpochs) - 1):
    if runEpochs[x+1][0] - runEpochs[x][1] < framesPerSecond* maximumTimeBetweenToAllowMerge:
        epochsToMerge.append(x)
        epochsToMerge.append(x + 1)'''
def mergeEpochsFunc(runEpochs):
    frame = 0
    epochsToMerge = []
    while frame < len(runEpochs)-1:
        if abs(runEpochs[frame + 1][0] -  runEpochs[frame][1]) < framesPerSecond * maximumTimeBetweenToAllowMerge:
            epochsToMerge.append([runEpochs[frame][0],runEpochs[frame + 1][1]])
            frame +=1
        else:
            epochsToMerge.append(list(runEpochs[frame]))
        frame +=1
    if runEpochs[-1][0] - runEpochs[-2][1] > framesPerSecond * maximumTimeBetweenToAllowMerge:
        epochsToMerge.append(list(runEpochs[-1]))
    return epochsToMerge

def mergeEpochs(runEpochs,prevLen):
    mergedEpochs = mergeEpochsFunc(runEpochs)
    #print prevLen
    if len(mergedEpochs) == prevLen:
        return mergedEpochs

    else:
        return mergeEpochs(mergedEpochs, len(mergedEpochs))

mergedEpochs = mergeEpochs(runEpochs,len(runEpochs))
runEpochsFinal = []
for x in mergedEpochs:
    if x[1]-x[0] > framesPerSecond * secondsRequiredToBeEpoch:
        runEpochsFinal.append(x)

print runEpochsFinal
print len(runEpochsFinal)
f = open('runEpochs.txt','w')
for x in runEpochsFinal:
	f.write(str(x)[1:-1]+'\n')
f.close()
