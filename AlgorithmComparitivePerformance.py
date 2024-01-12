import RepopulationAlgorithm
import random
import csv
import math

filename = "data/EnforCanadaBiomassFinalData_v2007-ENG.csv"

rows = []

with open(filename, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)


forest_rand=[]
forest_algo=[]


# scores
def gleason_diversity_index(S, N): # S is number of species in area, N is total area
    return S/math.log(N)
    
def menhinick_species_richness_index(S, n): # S above, n is total individuals across all species
    return S/math.sqrt(n)

def shannon_wiener_index(arr_species, arr_speciescount, base=2): # base arg so we can use for Pielou species evenness index
    summation=[]
    for species in arr_species:
        p_i = arr_speciescount / sum(arr_speciescount)
        summation.append(p_i * math.log(p_i,base))
    return -sum(summation)

def pielou_species_evenness_index(S, arr_species, arr_speciescount): # could replace s with count(arr_species)
    return shannon_wiener_index(arr_species,arr_speciescount,10)/math.log(S,10)

def test_forest(forest):
    arr_species = forest
    arr_speciescount = [] # TODO: DO THIS
    print()

# province argument ignored for algorithmically based trees
def generate_forest(province, lat=None, long=None):
    return_forest=[]
    if(long==None or lat==None):
        for row in rows:
            if(row[2]==province and random.randint(0,8)==2 and len(return_forest)<50):
                return_forest.append(row[7])

    else:
        for i in range(0,50): # do a better job of generating forest pls
            return_forest.append(RepopulationAlgorithm.best_tree(
                long+random.randint(-i*5,i*5)
                , lat+random.randint(-i*5,i*5))[1])

    
    return return_forest

forest_rand=generate_forest("AB")
forest_algo=[item for item in generate_forest("AB", -120,45) if(item !='')]

scores_random=[RepopulationAlgorithm.repopulation_score(45,-120,tree) for tree in forest_rand]
scores_algo=[RepopulationAlgorithm.repopulation_score(45,-120,tree) for tree in forest_algo]

print("Mean repopulation score random trees: "+str(sum(scores_random)/len(scores_random)))
print("'' '' '' algorithm trees: "+str(sum(scores_algo)/len(scores_algo)))