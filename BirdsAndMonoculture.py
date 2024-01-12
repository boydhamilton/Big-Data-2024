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

    for column in csv_reader.fieldnames:
        columns[column] = []

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

avg_monoculture=[column_count[key] for key in column_count if("monoculture" in key.lower())]
avg_native=[column_count[key] for key in column_count if("monoculture" not in key.lower())]

avg_monoculture_v = sum(avg_monoculture)/len(avg_monoculture)
avg_native_v = sum(avg_native)/len(avg_native)

x_values=[0,1,2,3,4]

z = np.polyfit(x_values, ranked_values, 1)
p = np.poly1d(z)
coefficient_of_determination = r2_score(ranked_values, p(x_values))
print("Brunt r2 value :"+str(coefficient_of_determination))

z_2 = np.polyfit([1,2], [avg_native_v, avg_monoculture_v], 1)
p_2 = np.poly1d(z_2)
coefficient_of_determination_2 = r2_score(ranked_values, p(x_values))
print("Mean r2 value :"+str(coefficient_of_determination_2))



plt.plot(x_values, p(x_values),color="red") # trendline
plt.plot([5,6], p_2([1,2]) , color="purple")
plt.bar(ranked_keys, ranked_values)

plt.bar(["Native Mean", "Monoculture Mean"], [avg_native_v, avg_monoculture_v], color="pink")


plt.xlabel("Tree Species")
plt.ylabel("Birds in Biome")
plt.title("Birds in Tree Biome")
plt.show()