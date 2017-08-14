#Script
import oPCA
import numpy as np
f = open('C_df_filtered.txt', 'r')
rawData = f.read()
f.close()

data = map(lambda x: 
		map(lambda y: float(y), x.strip().split(',')), 
	rawData.strip().split('\n'))
data = np.array(data)
print len(data)
print len(data[0])
eigvals, eigvecs, PCs = oPCA.offsetPCA(data.T, 5)
PCs = PCs.T

f = open('C_df_oPCA_output.txt','w')
for x in PCs:
	f.write(str(x.tolist())[1:-1]+'\n')
f.close()