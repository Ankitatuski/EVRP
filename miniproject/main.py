import map
import numpy as np
from copy import deepcopy
from ant import mrówkowojażer
import random
import math

cities = 16
pts,dist = map.carte(cities,5)#,plot=True)
#print (dist)

def pathlen(p):
    r=0
    for a in range(len(p)-1):
        r+=dist[p[a],p[a+1]]
    return r

def mutate(path):
    a,b = random.sample(range(1,len(path)), 2)
    npath = deepcopy(path)
    temp = npath[a]
    npath[a] = npath[b]
    npath[b] = temp
    return npath


#initial solution (greedy)
path = [0]
cost = 0
while len(path)<cities:
    potential = dist[path[-1]]
    a = path[-1]
    #shortest
    sd=9999
    for b in range(cities):
        if dist[a][b]<=sd and b!=a and b not in path:
            si = b
            sd = dist[a][b]
    if si==a:
        print("aaaaaaaaa")
    else:
        path.append(si)
        cost+=sd

print ("initial: ",path,cost)
#print(pathlen(path))
path0,cost0 = deepcopy(path),deepcopy(cost)

#                                  _____
#________Metropolis__________   \\|* m *|//
k = 0
coverg=100

while k<=300 and coverg >=0.01:
    #print("___ineration_metro:",k, cost)
    #new solution
    npath = mutate(path)

    mi = 1
    de = pathlen(npath) - cost
    if de<0 or np.exp(-de/cost)>mi:
        path = deepcopy(npath)
        coverg = deepcopy(cost)
        cost = pathlen(path)
        coverg-=cost
    k+=1
print ("metropolis: ",path,cost)

#_________Tabu__________
    
LT = []     #lisste tabu
k=0
path, cost = path0,cost0
converg = 99

while k<300 and converg>=0.01:
    #print("___ineration_tabu:",k, cost)
    npath = mutate(path)
    ncost = pathlen(npath)

    if ncost<cost and npath not in path:
        LT.append(path)
        path = npath
        converg = cost-ncost
        cost = ncost
    k+=1
    if len(LT)>=25:
        LT = LT[5:]
print ("tabu: ",path,cost)

#_______ant_________
path = mrówkowojażer(pts,dist,ants=20,iter=30,evaporation=0.3)
print ("ants: ",path,pathlen(path))

#________VRP______________________________________________________________________________________
num_of_vehicles = 3

def inrand(a, n):
    k, m = divmod(len(a), n)
    chunks = [
        a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
        for i in range(n)
    ]
    return np.stack([
        np.concatenate(([0], chunk, [0])) if chunk.size > 0 else np.array([0, 0])
        for chunk in chunks
    ])

def pathlens(paths):
    r = 0
    for p in paths:
        r+=pathlen(p)
    return r

def crois(paths):
    for i in range(len(paths)-1):
        #print(paths)
        r1 = random.randint(1,len(paths[i])-2)
        r2 = random.randint(1,len(paths[i+1])-2)
        #print(r1,r2)
        p = deepcopy(paths[i][r1])
        paths[i][r1] = paths[i+1][r2]
        paths[i+1][r2] = p
    #print("aaaaaaaa")
    return paths

paths0 = np.random.permutation([i for i in range(1,cities)])
paths0 = inrand(paths0,num_of_vehicles)
print("\n_______VRP_____________",pathlens(paths0))
print(paths0)



paths = []

#_________Tabu__________

LT = []    #lisste tabu
k=0
converg = 99
d=int(cities/3)
paths = deepcopy(paths0)
#LT.append(paths)
costs = pathlens(paths)

while k<300 and converg>=0.01:
    npaths = deepcopy(paths)
    ncosts = deepcopy(costs)
    #print("___ineration_tabu:",k)
    for i in paths:
        i = mutate(i)
    for i in range(2):
        npaths = crois(npaths)  
    ncosts = pathlens(npaths)
    #print(costs, ncosts)

    #print(LT)
    if ncosts<costs and npaths not in LT:
        #LT.append(np.array(paths))
        paths = deepcopy(npaths)
        converg = costs-ncosts
        costs = deepcopy(ncosts)
    k+=1
    if len(LT)>=25:
        LT = LT[5:]

print ("\nTabu: ",pathlens(paths),"\n",paths)


#__________genetic____________
print("\n----genetic-----")
def evolve(paths):
    npaths = deepcopy(paths)
    ncosts = deepcopy(costs)
    for i in paths:
        i = mutate(i)
    for i in range(3):
        npaths = crois(npaths)  
    ncosts = pathlens(npaths)
    return npaths,ncosts

pop_size = 30
pop = [deepcopy(paths0) for i in range(pop_size)]
#print(pop)
costs = [pathlens(i) for i in pop]
best = paths0
bestc = pathlens(paths0)
best_counter = 0
k=0

while k<300:
    #print("________Genetic iteration ",k)
    #selection
    pop = np.random.permutation(pop)
    costs = [pathlens(i) for i in pop]
    #mutation
    for i in range(int(pop_size/5),len(pop)):
        pop[i],costs[i] = evolve(pop[i])
    #evaluations
    Z = sum(costs)
    fitness = np.array([(i/Z)**2 for i in costs])   #chance of not continuing
    

    #print("pop",pop)
    #print("cost",costs)
    #print("fitness",fitness)

    #new pop
    npop = []
    """for i in range(len(fitness)):
        #n = math.floor((fitness[i]*pop_size))
        n = int(np.round(fitness[i]*pop_size,0))
        print("n: ",n)
        #print(i,pop[i])
        for j in range(n):
            npop.append(pop[i])
        #print(npop)"""
    #roulette
    for i in range(len(fitness)):
        r = random.randint(0,100)
        if r >= fitness[i]*100:
            npop.append(pop[i])

    #best
    nbest = pop[np.argmin(fitness)]
    nbestc = pathlens(nbest)
    #print(nbest,nbestc,bestc)
    if nbestc<bestc:
        best_counter += 1
        #print("bbbbbbbbbbbbbbbbbbbbbb")
        best = deepcopy(nbest)
        bestc = deepcopy(nbestc)
    while(len(npop)<len(pop)):
        #print ("a")
        npop.append(best)
    for i in range(int(pop_size/5)):
        n = np.argmin(fitness)
        npop[n] = best
    
    pop = deepcopy(npop)
    k+=1
    #print(npop)
    #print("popsize",len(pop))
print("\tbest\t",pathlens(best),"act =",best_counter)
print(best)


#print(pathlens(paths0))
##____notes
#   for interface
#   map box
#   open street map

