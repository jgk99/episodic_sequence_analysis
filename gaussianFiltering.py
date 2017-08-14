import scipy.ndimage.filters
import matplotlib.pyplot as plt

f = open('C_df.txt', 'r')
rawData = f.read()
f.close()
#print rawData
data = map(lambda x: 
	map(lambda y: float(y), x.strip().split('  ')), 
	rawData.strip().split('\n'))

filteredData5s = map(lambda x: scipy.ndimage.filters.gaussian_filter(x, 5).tolist(), data)

f = open('C_df_filtered5s.txt','w')
for x in filteredData5s:
	f.write(str(x)[1:-1]+'\n')
f.close()

filteredData2s = map(lambda x: scipy.ndimage.filters.gaussian_filter(x, 2).tolist(), data)

f = open('C_df_filtered2s.txt','w')
for x in filteredData2s:
	f.write(str(x)[1:-1]+'\n')
f.close()

#plt.plot(data[50][:1000])
#plt.plot(filteredData[50][:1000])

#plt.ylabel('')
#plt.show()
#plt.close()