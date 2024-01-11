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

miner_index=0 # im lazy
for i in range(len(rows[0])):
    if(rows[0][i]=="SumMinersTree"):
        miner_index=i

miner_data=[float(row[len(rows[0])-5]) for row in rows if(row[4]=="Y")]
richness_data=[float(row[7])+random.uniform(-0.1,0.1) for row in rows if(row[4]=="Y")] 

# calculating trendline
z = np.polyfit(richness_data, miner_data, 1)
p = np.poly1d(z)

coefficient_of_determination = r2_score(miner_data, p(richness_data))

print(coefficient_of_determination)

plt.plot(richness_data, p(richness_data),color="red") # trendline

plt.scatter(richness_data,miner_data) # mildew data
plt.xlabel("Species Richness")
plt.ylabel("Predicted mildew infection")
plt.title("Canadian Trees")
plt.show()