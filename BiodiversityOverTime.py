
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# summary

filename = "data/ORPHEE_DataForEIDC.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)




richness_data=[]
mildew_data=[]

for i in range(1,len(rows)):
    row=rows[i]
    richness_data.append(float(row[7]))
    mildew_data.append(float(row[12]))

z = np.polyfit(richness_data, mildew_data, 1)
p = np.poly1d(z)

plt.plot(richness_data, p(richness_data))

plt.scatter(richness_data,mildew_data)
plt.show()