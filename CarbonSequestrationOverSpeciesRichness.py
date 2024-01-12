
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score


filename = "data/data_plotlevel.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

plot_a=[ [float(row[0]), float(row[5]), float(row[28])] for row in rows if(row[1]=="A")]
# plot_b=[ [float(row[0]), float(row[5]), float(row[28])] for row in rows if(row[1]=="B")]

plot_a_independant=[row[1] for row in plot_a] 
plot_a_dependant=[row[2] for row in plot_a]


def elim_outliers(arr):
    lower_bound = np.quantile(arr, 0.25)
    upper_bound = np.quantile(arr, 0.75)

    filtered_arr = [x for x in arr if(lower_bound <= x <= upper_bound)]

    return np.array(filtered_arr)

plot_a_dependant = elim_outliers(plot_a_dependant)
plot_a_independant = [plot_a_independant[i] for i in range(len(plot_a_dependant))]

plot_a_dependant_1=[]
plot_a_dependant_2=[]
plot_a_dependant_4=[]
plot_a_dependant_8=[]
plot_a_dependant_16=[]
plot_a_dependant_24=[]

for i in range(len(plot_a_independant)):# 1,2,4,8,16,24
    match plot_a_independant[i]:
        case 1:
            plot_a_dependant_1.append(plot_a_dependant[i])
        case 2:
            plot_a_dependant_2.append(plot_a_dependant[i])
        case 4:
            plot_a_dependant_4.append(plot_a_dependant[i])
        case 8:
            plot_a_dependant_8.append(plot_a_dependant[i])
        case 16:
            plot_a_dependant_16.append(plot_a_dependant[i])
        case 24:
            plot_a_dependant_24.append(plot_a_dependant[i])
    
plot_a_dependant_boxplot=[plot_a_dependant_1,plot_a_dependant_2,plot_a_dependant_4,plot_a_dependant_8,plot_a_dependant_16,plot_a_dependant_24]


# plot_b_independant=[row[1] for row in plot_b]
# plot_b_dependant=[row[2] for row in plot_b]

z = np.polyfit(plot_a_independant, plot_a_dependant, 1)
p = np.poly1d(z)
plt.plot(plot_a_independant, p(plot_a_independant), color="red")

# z_2 = np.polyfit(plot_b_independant, plot_b_dependant, 1)
# p_2 = np.poly1d(z_2)
# plt.plot(plot_b_independant, p_2(plot_b_independant), color="purple")

coefficient_of_determination = r2_score(plot_a_dependant, p(plot_a_independant))
# coefficient_of_determination_b = r2_score(plot_b_dependant, p_2(plot_b_independant))
print("A: "+str(coefficient_of_determination))
# print("B: "+str(coefficient_of_determination_b))

plt.boxplot(plot_a_dependant_boxplot,positions=[1,2,4,8,16,24])
# plt.scatter(plot_b_independant,plot_b_dependant, color="pink")

plt.xlabel("Species Richness")
plt.ylabel("Carbon Sequestration Amount")
plt.show()