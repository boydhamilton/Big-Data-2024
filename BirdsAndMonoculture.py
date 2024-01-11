import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename = "data/41467_2016_BFncomms12717_MOESM1715_ESM.csv"
rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

        
print(rows)
tree_species=[]


print(tree_species)

# plt.barh(y = location_culled, width = amount, color ='maroon', 
#          height = 0.4)

plt.xlabel("Amount of Given Species in Given Location")
plt.ylabel("Location + Species")
plt.title("Canadian Trees")
plt.show()