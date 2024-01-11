
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from sklearn.metrics import r2_score


filename = "data/ORPHEE_DataForEIDC.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)


rows=[row for row in rows if(row!=rows[0])] # get titles out so we can convert to floats

chewer_index=0 # im lazy
for i in range(len(rows[0])):
    if(rows[0][i]=="SumMinersTree"):
        chewer_data=i

# add noise to better show the amount of points at each richness interval
richness_data=[float(row[7])+random.uniform(-0.1,0.1) for row in rows] 
mildew_data=[float(row[12]) for row in rows]

# calculating trendline
z = np.polyfit(richness_data, mildew_data, 1)
p = np.poly1d(z)

coefficient_of_dermination = r2_score(mildew_data, p(richness_data))

print(coefficient_of_dermination)

plt.plot(richness_data, p(richness_data),color="red") # trendline
plt.plot(richness_data,[sum(mildew_data)/len(mildew_data)]*len(mildew_data),color="green") # mildew mean

plt.scatter(richness_data,mildew_data) # mildew data
plt.xlabel("Species Richness")
plt.ylabel("Predicted mildew infection")
plt.title("Canadian Trees")
plt.show()