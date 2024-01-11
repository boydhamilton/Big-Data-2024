import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

filename = "data/41467_2016_BFncomms12717_MOESM1715_ESM.csv"

file_opened = open(filename, 'r')
 
# creating dictreader object
file = csv.DictReader(filename)

df=[]
rows = []

columns = {}
column_count = {}
    
with open(filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Assuming the first row contains column headers
    for column in csv_reader.fieldnames:
        columns[column] = []
    
    # Iterate through each row and append values to respective columns
    for row in csv_reader:
        for column in csv_reader.fieldnames:
            columns[column].append(row[column])

for key in columns:
    if(key!="Species"and ("Cropland") not in key):
        column_count[key]=(columns[key].count("Y"))

keys = list(column_count.keys())
values = list(column_count.values())

combo = list(zip(keys,values))
ranked_data = sorted(combo, key=lambda x: x[1], reverse=True)
ranked_keys = [item[0] for item in ranked_data]
ranked_values = [item[1] for item in ranked_data]

x_values=[0,1,2,3,4]

z = np.polyfit(x_values, ranked_values, 1)
p = np.poly1d(z)

coefficient_of_dermination = r2_score(ranked_values, p(x_values))

print(coefficient_of_dermination)

plt.plot(x_values, p(x_values),color="red") # trendline

plt.bar(ranked_keys, ranked_values)

plt.xlabel("Tree Species")
plt.ylabel("Birds in Biome")
plt.title("Birds in Tree Biome")
plt.show()