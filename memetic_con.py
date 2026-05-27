import numpy as np
import random
from copy import deepcopy
import map

# replicating https://ieeexplore.ieee.org/abstract/document/9194245
#fitness
def fit(path, dist):    #for single vehile
    r=0
    for a in range(len(path)-1):
        r+=dist[path[a],path[a+1]]
    return r

def fits(paths,dist):   #for solution (multiple vehicle)
    r = 0
    for p in paths:
        r+=fit(p,dist)
    return r

def feasible(path, dist, chargers, battery):
    left = battery
    for i in range(1,len(path)):
        left-= dist[path[i-1]][path[i]]
        if left<0:
            return False
        if path[i] in chargers:
            left=battery
    return True

def feasibles(sol, dist, chargers, battery):
    left = battery
    for path in sol:
        for i in range(1,len(path)):
            left-= dist[path[i-1]][path[i]]
            if left<0:
                return False
            if path[i] in chargers:
                left=battery
    return True
            

def PopGen(size,pts,cars,dist):
    pop = []

    for j in range(size):
        indiv = ([[pts[0]] for i in cars])

        for place in pts[1:]:
            c = random.choice(cars)
            indiv[c].append(place)

        for c in indiv:
            #print("ini",c)
            for i in range(5):
                arr = deepcopy(c)
                a = random.randint(1,len(pts)-2)
                b = random.randint(a,len(pts)-1)
                arr[a:b+1] = arr[a:b+1][::-1]
                if fit(arr,dist)<=fit(c,dist):
                    c = arr
            #print("fin",c)
            
        for c in cars:
            indiv[c].append(pts[0])
        pop.append(indiv)
    return pop

def shake(sol, Dsol, n, k, chargers=[]): 
    TV = deepcopy(sol)
    dcars = []
    for d in Dsol:
        if len(d) >=k+2:
            dcars.append(d)
    if len(dcars) == 0:
        return TV
    for i in range(n):
        car = random.choice(dcars)
        #print("car:",car)
        a = random.randint(1,len(car)-k-1)
        seg = car[a:a+k]
        if 0 in seg:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        #print("seg", seg)

        # chargers
        delseg = deepcopy(seg)
        if chargers !=[]:
            for b in chargers:
                delseg = [x for x in delseg if x != b]
        #print("delseg",delseg)

        # delete from TV
        for b in delseg:
            TV = [[x for x in car if x != b] for car in TV]
            #print("b:", b)
        #print("TVcut:",TV)
        # add to TV
        Tcar = random.randint(0, len(TV) - 1)
        pos = random.randint(1, len(TV[Tcar])-1)
        TV[Tcar][pos:pos] = seg
    return TV

def decharge(sol,chargers,dist,batt):
    for path in sol:
        for i in range(2*len(path)):   #num of iterations
            temp = deepcopy(path)
            point = random.choice(temp)
            if point in chargers:
                del point
                if feasible(temp,dist,chargers,batt):
                    path = deepcopy(temp)
    return sol

def mutate(path):
    l = len(path)-2
    if l>1:
        a = random.randint(1,l-1)
        b = random.randint(a+1,l)
        c = deepcopy(path[a])
        path[a] = path[b]
        path[b] = c
    return path

def mutatecharge(path,chargers):
    i = random.randint(1,len(path)-1)
    path.insert(i,random.choice(chargers))
    return path

def tabu(path0, dist, tabu_size=5, max_iter=3):

    path = path0
    cost = fit(path, dist)

    bpath = deepcopy(path)
    bcost = deepcopy(cost)

    TL = []

    for k in range(max_iter):

        neibors = []

        for i in range(1,len(path)-1):
            for j in range(i+1, len(path)-1):
                n = path
                n[i], n[j] = n[j], n[i]

                if n not in TL:
                    neibors.append([n, fit(n, dist)])
                    #print("+")

        if not neibors:
            #print("break: ",k)
            break
        path, cost = min(neibors, key=lambda x: x[1])
        if cost < bcost:
            bpath = deepcopy(path)
            bcost = deepcopy(cost)
        
        TL.append(deepcopy(path))
        #print(TL)

        if len(TL) > tabu_size:
            TL.pop(0)

    return bpath, bcost


def Memetic (PopSize, pts, dist, Ncars, chargers, battery, DmSize=2, Kmax=3, Smin=1, Smax=2, Mprob=0.5, Vini=0, Vlim=3,iter = 30, tab=True):
    lastbest = 9999999999999999999
    lbk = 0
    #__initialising population
    pop = PopGen(PopSize,pts,[i for i in range(Ncars)],dist)
    fitnes = [fits(p,dist) for p in pop]

    #__Dynamic memo initialisation
    Dm = deepcopy(pop)
    Dmf = deepcopy(fitnes)
    while(len(Dm)>DmSize):
        l = Dmf.index(max(Dmf))
        Dm = Dm[:l] + Dm[l+1:]
        Dmf = Dmf[:l] + Dmf[l+1:]
    Dmv = [Vini for d in Dmf]
    #print (pop,"\n",Dm)

    #__________________     
    #__ACTUAL PROGRAM__

    iterator = 1
    while(iterator<=iter):
        print("========= ITERATION: ",iterator)
        #print(pop)
        #print("\n",Dm)
        for i in range(len(pop)):
            #print("====== i: ",i)
            T1 = pop[i]
            for k in range(1,Kmax+1):
                #print("=== k: ",k)
                ii = random.randint(0,DmSize-1)
                D = Dm[ii]
                T2 = shake(T1, D, random.randint(Smin,Smax), k)
                if not feasibles(T2,dist,chargers,battery):
                    #print("--not feasible")
                    T2 = shake(T1, D, random.randint(Smin,Smax), k,chargers)

                T3 = deepcopy(T2)
                if tab:
                    for path in T3:
                        path = tabu(path,dist)
                    if fits(T2,dist)<fits(T3,dist) and feasibles(T3,dist,chargers,battery):
                        T3=T2

                T3 = decharge(T3,chargers,dist,battery)

                # Dm update
                Tfit = fits(T3,dist)
                #print("Dmv: ",Dmv)
                if Tfit>=fitnes[i]:    #not sure about =
                    Dmv[ii]-=1
                    #print("--worse found")
                    if Dmv[ii] <= Vini-Vlim:     #new solution enters Dm
                        mx = max(fitnes)
                        fcopy = deepcopy(fitnes)
                        j = fcopy.index(min(fcopy))
                        thesame = 0
                        while(pop[j] in Dm and thesame<=PopSize):
                            fcopy[j] = mx
                            j = fcopy.index(min(fcopy))
                            thesame+=1
                        Dm[ii] = deepcopy(pop[j])
                        Dmf[ii] = fits(Dm[ii],dist)
                        Dmv[ii] = Vini
                        #print("Dm updated")
                else:
                    #print("++better found")
                    if Dmv[ii]< Vini+Vlim:
                        Dmv[ii]+=1
                # pop update
                    pop[i] = deepcopy(T3)
                    fitnes[i] = deepcopy(Tfit)
                    break

                """# pop update
                if Tfit<=fitnes[i]:
                    pop[i] = deepcopy(T3)
                    fitnes[i] = deepcopy(Tfit)
                    break"""
        # mutation
        best = fitnes.index(min(fitnes))
        for a in range(len(pop)):
            if a!=best:
                for b in pop[a]:
                    if random.randint(0,100) <= 100*Mprob:
                        b = mutate(b)
                    if random.randint(0,100) <= 100*Mprob:
                        b = mutatecharge(b,chargers)
                    pop[a] = decharge(pop[a],chargers,dist,battery)

        print("best",min(fitnes))
        iterator+=1

        if min(fitnes) < lastbest:
            lastbest = deepcopy(min(fitnes))
            lbk = iterator

    l = fitnes.index(min(fitnes))
    #print(fits(pop[l],dist))
    print("last best:", lbk)
    return pop[l], fitnes[l],



if __name__ == "__main__":
    N = 10
    pts,dist,chargers = map.carte(N,5,chargers=int(N/5))
    cities = [a for a in range(N)]
    D = [0,7,3,5,1,8,2,0],[0,4,6,0]
    P = [0,4,3,2,1,0],[0,7,8,6,5,0]

    posize = 8
    iter = 30
    batt = 15
    
    #print(PopGen(2,cities,[0,1,2],dist))
    #print(shake(P,D,1,3,[1,2]))

    paths, cos = Memetic(posize,cities,dist,3,chargers,batt,DmSize=5,iter=iter,Mprob=0.8)
    print(paths, cos )
    print(feasibles(paths,dist,chargers,batt))
    map.drawVRP(paths,pts,chargers)

    """paths, cos = Memetic(posize,cities,dist,DmSize=5,Ncars=3,iter=iter,tab=False)
    print(paths, cos )
    map.drawVRP(paths,pts)"""

    """a,b = tabu_search([0,1,2,3,4,0],dist)
    print(a)
    map.drawVRP([a],pts)"""

