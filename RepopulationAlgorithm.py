
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
def dist(a,b): # UNUSED
    return math.sqrt(abs(b[0]-a[0]) + abs(b[1]-a[1]))

# distance accurate and accounting for the earths curvature. result is returned in kilometers
def haversine(a,b): # [longitude, latitude]
    lat1=a[1]
    lon1=a[0]
    lat2=b[1]
    lon2=b[0]
    
    R = 6371  # earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c
    return distance

# turned to method due to amount of use
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
        return haversine([x,y],[xavg,yavg])
    else:
        return 0


def biodiversity_score(long, lat, species, acceptable_range=10000):
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
            if(haversine([x,y],point)<=acceptable_range):
                sia.append(name)
            if(haversine([x,y],point)<=acceptable_range and name not in sia_culled):
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
    # find whatever a big number seems (8? 9?) and do between 1 and that
    # FOR FINAL EQUATION: if you have small native score and big biodiversity score? YOU FOUND THE ONE
    # means its growth should be encouraged, as it's in the area but being beaten out by more common species
    if(species in ranked_species):
        return (ranked_counts[ranked_species.index(species)] * ranked_species.index(species))
    else:
        return 0


def carbonSequesteration_score(long, lat, species, acceptable_range):
    summation_list=[]
    species_list=[]
    for row in rows:
        if(row[7]==species):
            try:
                if(haversine(getposition(row),[long,lat])<=acceptable_range*1.5): # can estimate little beyond given area for this
                    species_list.append(row)
            except:
                pass

    for specimen in species_list:
        try:
            summation_list.append(float(specimen[11])/4) # estimation of carbon is (total wood mass / 2) / 2 as you must first isolate dry wood, which is about 48-50% carbon
        except:
            pass
    

    avg_species_mass=sum(summation_list)/len(summation_list)

    return avg_species_mass*2 # scale up

def repopulation_score(lat, long, species, acceptable_range=10000): # lat is y row[17] long is x row[18]
    ns=native_score(long, lat, species)
    bs=biodiversity_score(long, lat, species, acceptable_range)
    cs=carbonSequesteration_score(long, lat, species, acceptable_range)

    if(ns!=0):
        final_score = (bs + cs) / ns  #figure out carbon first
    else:
        final_score = 0
    return final_score

def best_tree(long,lat,acceptable_range=10000):
    y = lat
    x = long
    best=[0,""] # score, species
    
    species_array=[]
    for row in rows:
        if(getposition(row)!=None):
            if(haversine([x,y],getposition(row))<=acceptable_range and row[7]not in species_array):
                species_array.append(row[7])

    for current_species in species_array:
        current_rs = repopulation_score(y,x,current_species,acceptable_range)
        # print(current_rs)
        if(current_rs>best[0]): # TODO: double check biggest is best
            best=[current_rs,current_species]
            print("NEW BEST: "+str(current_rs))

    return best


from_user = [float(item) for item in input("Enter 'lat,long,acceptablerange': ").split(',')] # exact formatting for input (this is silly python code)

values= from_user #lat long acceptablerange

choice_table = best_tree(values[1],values[0],values[2])
choice = choice_table[1] # species
score = choice_table[0] # score

print("\nAt: "+str(values[0])+", "+str(values[1]))
print("N: "+str(native_score(values[1], values[0], choice))+ " B: "+str(biodiversity_score(values[1], values[0], choice, values[2]))
      +" C: "+str(carbonSequesteration_score(values[1], values[0], choice, values[2])))
print("Score: "+str(score))
print(choice)

SpeciesLocationPlot.run(choice,values[1],values[0])