
# plot location asp

import csv 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# using data to create a scatterplot representing amount of trees of different species at positions


filename = "data/EnforCanadaBiomassFinalData_v2007-ENG.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

    print("Rows: ", str(csvreader.line_num))

run=True
while run:
    desired_species = input("Species to plot: ")
    
    if(desired_species=="exit"): # gotta have exit code for looping program
        run=False
        quit()

    coordinates = []


    for row in rows:
        if(row != rows[0] and row[7]==desired_species):
            coordinates.append([row[17], row[18]])
            
    coordinates_culled = []

    latitude = []
    longitude = []
    size = []

    for point in coordinates:
        if(not (point in coordinates_culled)):
            try:
                # HOW DOES LATITUDE AND LONGITUDE WORK WHAT
                longitude.append(float(point[0]))
                latitude.append(float(point[1]))
                
                coordinates_culled.append(point)
                size.append(coordinates.count(point))
            except:
                print("conversion fail "+point[0]+" or "+point[1]) # failure stems from the fact that many samples have unrecorded latitudes and longitudes

    # clamp graph display to range representitive of canada. overlay is doing too much, this allows us to still get an idea of position in space
    plt.xlim(-145,-40)
    plt.ylim(40,80)
    plt.scatter(latitude,longitude,s=size)
    plt.show()


    