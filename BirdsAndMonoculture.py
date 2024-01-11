import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    if(key!="Species"):
        column_count[key]=(columns[key].count("Y"))

print(column_count)

keys = list(column_count.keys())
values = list(column_count.values())

plt.barh(keys, values)

plt.xlabel("Amount of Given Species in Given Location")
plt.ylabel("Location + Species")
plt.title("Canadian Trees")
plt.show()