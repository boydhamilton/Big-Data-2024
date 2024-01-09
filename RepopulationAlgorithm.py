
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import SpeciesLocationPlot # graph

# source link: https://open.canada.ca/data/en/dataset/fbad665e-8ac9-4635-9f84-e4fd53a6253c/resource/15cb39a0-b591-4947-9e6c-e4d2e12b3346

filename = "data/EnforCanadaBiomassFinalData_v2007-ENG.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)


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

    if(len(xarr)!=0 and len(yarr)!=0):
        xavg=sum(xarr)/len(xarr)
        yavg=sum(yarr)/len(yarr)
        return dist([x,y],[xavg,yavg]) # smaller is better
    else:
        return 0


def biodiversity_score(long, lat, species, acceptable_range=6):
    # get species in range, number of choice species in area over number of average species in area? idk 
    # range in distance measured by lat long. totally arbitrary. tune maybe? should be big, we just take topmost common species
    
    x=long
    y=lat
    sia=[] # species in area
    sia_culled=[]
    sia_count=[]
    for row in rows:
        name = row[7]
        point = getposition(row)
        if(point!=None):
            if(dist([x,y],point)<=acceptable_range):
                sia.append(name)
            if(dist([x,y],point)<=acceptable_range and name not in sia_culled):
                sia_culled.append(name)


    for s in sia_culled:
        sia_count.append(sia.count(s))

    # next lines are wild python list stuff, sorts count and sorts culled accordingly
    combo = list(zip(sia_culled,sia_count))
    ranked_data = sorted(combo, key=lambda x: x[1], reverse=True)
    ranked_species = [item[0] for item in ranked_data]
    ranked_counts = [item[1] for item in ranked_data]

    if(len(sia)==0):
        pass # biod score Out of range
    
    # returns 0 for most common/least diverse so dont make multiplier cause biodiversity is not that serious
    # small if native. big if not native. in all honesty might want to judge more off domain specification than big or small
    # as approaching zero could encourage monoculture but approaching big number could lead to low survivability
    # find whatever a big number seems (8? 9?) and do between 1 and that methinks
    # FOR FINAL EQUATION: if you have small native score and big biodiversity score? YOU FOUND THE ONE
    # means its growth should be encouraged, as it's in the area but being beaten out by more common species
    # print(sia)
    if(species in ranked_species):
        return (ranked_counts[ranked_species.index(species)] * ranked_species.index(species)) / (sum(ranked_counts)/len(ranked_counts))
    else:
        return 0


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

def repopulation_score(lat,long,species,acceptable_range=6): # lat is y row[17] long is x row[18]
    ns=native_score(long, lat, species)
    bs=biodiversity_score(long, lat, species, acceptable_range)
    # print(str(ns)+" "+str(bs))
    # cs=carbonSequesteration_score(long, lat, species)

    if(ns!=0):
        final_score = (bs / ns) #+ cs figure out carbon first
    else:
        final_score = 0
    return final_score

def best_tree(long,lat,acceptable_range=6):
    y = lat
    x = long
    best=[0,""] # score, species
    
    species_array=[]
    for row in rows:
        if(getposition(row)!=None):
            if(dist([x,y],getposition(row))<=acceptable_range and row[7]not in species_array):
                species_array.append(row[7])
        else:
            print('fuck')

    for current_species in species_array:
        current_rs = repopulation_score(y,x,current_species,acceptable_range)
        #print(str(current_rs)+" "+str(best[0]))
        print(current_rs)
        if(current_rs>best[0]): # TODO: double check biggest is best
            best=[current_rs,current_species]
            # print("split "+ str(native_score(long,lat,current_species)) + " "+str(biodiversity_score(long,lat,current_species,acceptable_range)))
            print("NEW BEST: "+str(current_rs))

    return best


from_user = [int(item) for item in input("Enter 'lat,long,acceptablerange': ").split(',')] # exact formatting for input (this is silly python code)

values= from_user #lat long acceptablerange

choice_table = best_tree(values[1],values[0],values[2])
choice = choice_table[1] # species
score = choice_table[0] # score

print("\nAt: "+str(values[0])+", "+str(values[1]))
print("N: "+str(native_score(values[1], values[0], choice))+ " B: "+str(biodiversity_score(values[1], values[0], choice, values[2])))
print("Score: "+str(score))
print(choice)

SpeciesLocationPlot.run(choice,values[1],values[0])
