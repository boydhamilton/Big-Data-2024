
import csv 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# using data to create a bar graph representing the amount of each species in each province of Canada

filename = "data/EnforCanadaBiomassFinalData_v2007-ENG.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

    print("Rows: ", str(csvreader.line_num))

# bar graph. xaxis has 'location species' and then the height value is amount. 
# to accomplish this, one first has to get all the different locations and species to populate the xaxis with the needed bars

location = []
amount = []

for row in rows:
    if(row!=rows[0]): # so we dont get 'province species' as an element haha
        element = str(row[2]+" "+row[7])
        location.append(element)

# logic here is that locations should appear sequentially, ergo if we put the amount in the same order it should line up
location_culled = []
for locale in location:
    print(location.count(locale))
    if(not (locale in location_culled)):
        amount.append(location.count(locale))
        location_culled.append(locale)
    else:
        print(locale + " previously tested")


plt.barh(y = location_culled, width = amount, color ='maroon', 
         height = 0.4)

plt.xlabel("Amount of Given Species in Given Location")
plt.ylabel("Location + Species")
plt.title("Canadian Trees")
plt.show()