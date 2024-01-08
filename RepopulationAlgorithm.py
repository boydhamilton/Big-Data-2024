
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import SpeciesLocationPlot

# summary

filename = "data/EnforCanadaBiomassFinalData_v2007-ENG.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

    #print("Rows: ", str(csvreader.line_num))


# staples
def dist(a,b): # [x,y], [x,y]
    return math.sqrt(abs(b[0]-a[0]) + abs(b[1]-a[1]))

def getposition(row):
    if(row[18]!=''and row[17]!=''and row!=rows[0]):
        return [float(row[18]),float(row[17])]
    # add nonetype check on use. stupid data set not having position for all elements 

# scoring
def native_score(x, y, species):
    xarr=[]
    yarr=[]
    for row in rows:
        if(row[7]==species):
            p = getposition(row)
            if(p!=None):
                xarr.append(p[0]) # lat is y, long is x
                yarr.append(p[1])
            else:
                print("fail on "+str(p))

    
    xavg=sum(xarr)/len(xarr)
    yavg=sum(yarr)/len(yarr)
    return dist([x,y],[xavg,yavg]) # smaller is better


def biodiversity_score(x, y, species, acceptable_range=6):
    # get species in range, number of choice species in area over number of average species in area? idk 
    # range in distance measured by lat long. totally arbitrary. tune maybe? should be big, we just take topmost common species
    sia=[] # species in area
    sia_culled=[]
    sia_count=[]

    for row in rows:
        if(row!=rows[0]):
            point=getposition(row)
            name=row[7]
            if(getposition(row)!=None):
                if(dist([x,y],point)<=acceptable_range):
                    sia.append(name)
                if(dist([x,y],point)<=acceptable_range and name not in sia_culled):
                    sia_culled.append(name)
                    

    for s in sia_culled:
        sia_count.append(sia.count(s))

    # next lines are wild python list stuff, sorts count and sorts culled accordingly
    combo = list(zip(sia_culled,sia_count))
    sorted_data = sorted(combo, key=lambda x: x[1], reverse=True)
    sorted_species = [item[0] for item in sorted_data]
    sorted_counts = [item[1] for item in sorted_data]

    if(len(sia)==0):
        print("biod score Out of range")
    
    # returns 0 for most common/least diverse so dont make multiplier cause biodiversity is not that serious
    # small if native. big if not native. in all honesty might want to judge more off domain specification than big or small
    # as approaching zero could encourage monoculture but approaching big number could lead to low survivability
    # find whatever a big number seems (8? 9?) and do between 1 and that methinks
    # FOR FINAL EQUATION: if you have small native score and big biodiversity score? YOU FOUND THE ONE
    # means its growth should be encouraged, as it's in the area but being beaten out by more common species
    return (sorted_counts[sorted_species.index(species)] * sorted_species.index(species)) / (sum(sorted_counts)/len(sorted_counts))


# TODO: on the low no way om_total is mass of tree so this needs to be fixed this is genuine nonsense
def carbonSequesteration_score(x, y, species):
    species_list = [row for row in rows if(row[7]==species)] # HOW DOES THIS WORK LMAO PYTHON IS SO DUMB
    
    avg_species_mass=0 # on the low just *assuming* om_total is mass of tree
    # okie dokie carbon = 0.5(mass) tree organic chem formula i take internets word for it
    # do i care abt location?? for now i shall not include
    for row in species_list:
        avg_species_mass = float(row[16])

    avg_species_mass=avg_species_mass/len(species_list)

    return avg_species_mass

# tests

test_values=[45,-60,"Trembling Aspen"] # lat long species
def repopulation_score(lat,long,species): # lat is y row[17] long is x row[18]
    ns=native_score(long, lat, species)
    bs=biodiversity_score(long, lat, species)
    cs=carbonSequesteration_score(long, lat, species)

    #print("Native score: "+str(ns))

    #print("Biodiversity score: "+str(bs))

    #print("Carbon Sequesteration score: "+str(cs))

    final_score = (bs / ns) + cs
    return final_score

def best_tree(long,lat,acceptable_range=6):
    y = lat
    x = long
    best=[0,""] # score, species
    # giving a global searchable range cause ngl i dont need to test a tree that only lives on nova scoticaisda when im in van like be so fr rn PLEASSE
    sia=[] # species in area. all trees in area
    for row in rows:
        if(row!=rows[0]):
            point=getposition(row)
            if(getposition(row)!=None):
                if(dist([x,y],point)<=acceptable_range):
                    sia.append(row)
                    

    for i in range(1,len(sia)):
        row=sia[i]
        current_species = row[7]
        current_rs = repopulation_score(x,y,current_species)
        if(current_rs>best[0]): # TODO: double check biggest is best
            best=[current_rs,current_species]

    return best[1]

# graph for context because i was getting confused mental-ing positions and trees and whatnot
print(best_tree(test_values[1],test_values[0]))

SpeciesLocationPlot.run(test_values[2],test_values[1],test_values[0])