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

def feasible(path, dist, chargers, battery, penalty_multiplier = 3, details = False):
    left = battery
    score = 0
    f = True
    #print("w feasible; path: ", path)
    for i in range(1,len(path)):
        d = dist[path[i-1]][path[i]]
        left-=d
        score+=d
        if left<0:
            f = False
            score += penalty_multiplier*(-1*left+left**2)
        if path[i] in chargers:
            left=battery
    if not f:
        score*=2
    if details:
        return score, f
    return score

def feasibles(sol, dist, chargers, battery, details = False):
    rscore = 0
    rf  = True
    for path in sol:
        score, f = feasible(path, dist, chargers, battery, details=True)
        rscore+=score
        #print(f)
        if not f:
            rf = False
    if details:
        return rscore, rf
    return rscore

def PopGen(size,pts,cars,dist, chargers, battery, feasibility = True):
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
                #if fit(arr,dist)<=fit(c,dist):
                if feasible(arr,dist,chargers,battery)<=feasible(c,dist,chargers,battery):
                    c = arr
            #print("fin",c)
            
        for c in cars:
            indiv[c].append(pts[0])
        pop.append(indiv)

        
    if feasibility:
        for a, individual in enumerate(pop):
            for b, path in enumerate(individual):
                pn,pt = feasible(path,dist,chargers,battery,details=True)
                i=0
                while(not pt) and i<100:
                    path, pn = tabucharge(path,dist,chargers,battery, max_iter=3+i)
                    pn,pt = feasible(path,dist,chargers,battery,details=True)
                    i+=1
                #print(i, path)
                pop[a][b] = path

        """for ind in pop:
            for path in ind:
                pn,pt = feasible(path,dist,chargers,battery,details=True)
                i=0
                while(not pt) and i<100:
                    path, pn = tabucharge(path,dist,chargers,battery, max_iter=3+i)
                    pn,pt = feasible(path,dist,chargers,battery,details=True)
                    i+=1
                #print(i, path)"""

    return pop

def shake(sol, Dsol, n, k): 
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

        # delete from TV
        for b in seg:
            TV = [[x for x in car if x != b] for car in TV]
            #print("b:", b)
        #print("TVcut:",TV)
        # add to TV
        Tcar = random.randint(0, len(TV) - 1)
        pos = random.randint(1, len(TV[Tcar])-1)
        TV[Tcar][pos:pos] = seg
    return TV

def decharge(sol,chargers):
    for i in range(len(sol)):
        for c in chargers:
            sol[i] = ([x for x in sol[i] if x!=c])

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

def tabu(path0, dist, tabu_size=5, max_iter=3, chargers=[], battery=0):

    path = path0
    cost = fit(path, dist)

    bpath = deepcopy(path)
    bcost = deepcopy(cost)

    TL = []

    for k in range(max_iter):

        neibors = []

        for i in range(1,len(path)-1):
            #if path[i] not in chargers:
                for j in range(i+1, len(path)-1):
                    #if path[j] not in chargers:
                        n = path
                        n[i], n[j] = n[j], n[i]

                        if n not in TL and feasible(n,dist,chargers,battery,details=True)[1]:
                            #print("n:", feasible(n,dist,chargers,battery,details=True))
                            neibors.append([n, fit(n, dist)])
                            #print("+")

        if not neibors:
            #print("break: ",k)
            return bpath, bcost
            break
        path, cost = min(neibors, key=lambda x: x[1])
        if cost < bcost:
            #print("\t\ttabu found", feasible(path,dist,chargers,battery,details=True))
            bpath = deepcopy(path)
            bcost = deepcopy(cost)
        
        TL.append(deepcopy(path))
        #print(TL)

        if len(TL) > tabu_size:
            TL.pop(0)

    return bpath, bcost

def tabucharge(path0, dist, chargers, battery, tabu_size=5, max_iter=5):
    path = path0
    cost = feasible(path, dist,chargers,battery)

    bpath = deepcopy(path)
    bcost = deepcopy(cost)
    #print("tabu initial: ",bcost,bpath)

    TL = []
    TLi = []

    for k in range(max_iter):
        neibors = []

        for i in range(1,len(path0)):
            for j in chargers:  #unoptimal, maybe random 
                #print("w tabu; i, j", i, j)
                n = deepcopy(path)
                if n[i]!=j and n[i-1]!=j:
                    n[i:i] = [j]
                    if n not in TL and i not in TLi:
                        #print("po dodaniu", n)
                        neibors.append([n,feasible(n,dist,chargers,battery),i])

        if not neibors:
            #print("break: ",k)
            break
        
        path, cost, index = min(neibors, key=lambda x: x[1])

        if cost < bcost:
            #print("tabu found better")
            bpath = deepcopy(path)
            bcost = deepcopy(cost)

        TL.append(deepcopy(path))
        TLi.append(deepcopy(index))
        #TLi.append(deepcopy(index)+1)

        #print("tabu: ",path,cost)

    #print("tabu final: ",bcost,bpath)
    #print("tabu found feasible - ",feasible(bpath,dist,chargers,battery,details=True)[1])
    return bpath, bcost


def Memetic (PopSize, pts, dist, Ncars, chargers, battery, DmSize=2, Kmax=3, Smin=1, Smax=2, Mprob=0.5, Vini=0, Vlim=3,iter = 30):
    lastbest = 9999999999999999999
    lbk = 0
    #__initialising population
    pop = PopGen(PopSize,pts,[i for i in range(Ncars)],dist, chargers, battery, feasibility = True)
    fitnes = [fits(p,dist) for p in pop]
    #fitnes = [feasibles(p,dist,chargers,battery) for p in pop]

    unfit_count = PopSize
    for a in range(len(pop)):
        t = feasibles(pop[a],dist,chargers,battery,details=True)[1]
        if t:
            unfit_count-=1
        #print(a, feasibles(pop[a],dist,chargers,battery,details=True))
    if unfit_count > 0:
        print("Unfit individuals in initial population (%s) ! !"%unfit_count)

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
        #print("========= ITERATION: ",iterator)
        #print(pop)
        #print("\n",Dm)
        for i in range(len(pop)):
            #print("====== i: ",i)
            pn, pt = feasibles(pop[i],dist,chargers,battery,details=True)
            T1 = deepcopy(pop[i])
            T1 = decharge(T1,chargers)
            for k in range(1,Kmax+1):
                #print("=== k: ",k)
                ii = random.randint(0,DmSize-1)
                D = Dm[ii]
                T2 = shake(T1, D, random.randint(Smin,Smax), k)

                T3 = []

                # Tabu adds the chargers
                for path in T2:
                    T3.append(tabucharge(path,dist, chargers,battery)[0])
                Tfit = fits(T3,dist)
                #print("T3: ",T3)

                T4 = []
                for path in T3: 
                    T4.append(tabu(path,dist,chargers=chargers,battery=battery)[0])
                T4fit = fits(T4,dist)
                #print("T4 feasible?",feasibles(T4,dist,chargers,battery,details=True))
                
                if T4fit< Tfit:
                    #print("xxxxx T4 better", feasibles(T4,dist,chargers,battery,details=True)[1])
                    T3 = deepcopy(T4)
                    Tfit = deepcopy(T4fit)

                tn, tt = feasibles(T3,dist,chargers,battery,details=True)

                # Dm update
                #Tfit = fits(T3,dist)
                #Tfit = tn
                #print("Dmv: ",Dmv)
                #print("pop, T3",pt,tt)
                if tt and pt: #or (not pt):
                    if Tfit>=fitnes[i]:    #not sure about =
                        Dmv[ii]-=1
                        #print("--worse found")
                        if Dmv[ii] <= Vini-Vlim:     #new solution enters Dm
                            mx = max(fitnes)
                            fcopy = deepcopy(fitnes)
                            j = fcopy.index(min(fcopy))
                            thesame = 0
                            while((pop[j] in Dm) and thesame<=PopSize):
                                fcopy[j] = mx
                                j = fcopy.index(min(fcopy))
                                thesame+=1
                            DT = deepcopy(pop[j])
                            DT = decharge(DT,chargers)
                            Dm[ii] = DT
                            Dmf[ii] = fits(Dm[ii],dist)
                            Dmv[ii] = Vini
                            #print("Dm updated")
                    else:
                        #print("++better found")
                        if Dmv[ii]< Vini+Vlim:
                            Dmv[ii]+=1
                    # pop update
                        #print("pop, T3",pt,tt)
                        #print("new:",T3)
                        pop[i] = deepcopy(T3)
                        fitnes[i] = deepcopy(Tfit)
                        #print("\t",feasibles(pop[i],dist,chargers,battery,details=True)[1])
                        #print(pop)
                        break

                # pop update
                #if Tfit<=fitnes[i]:
                #    pop[i] = deepcopy(T3)
                #    fitnes[i] = deepcopy(Tfit)
                #    break
        # mutation
        """best = fitnes.index(min(fitnes))
        for a in range(len(pop)):
            if a!=best:
                for b in pop[a]:
                    if random.randint(0,100) <= 100*Mprob:
                        b = mutate(b)"""

        if min(fitnes) < lastbest:
            lastbest = deepcopy(min(fitnes))
            lbk = iterator

        """for ind in pop:
            print(feasibles(ind,dist,chargers,battery,details=True),fits(ind,dist))"""

        #print("best",min(fitnes))
        iterator+=1
    
    """for ind in pop:
        print(feasibles(ind,dist,chargers,battery,details=True),fits(ind,dist))"""

    l = fitnes.index(min(fitnes))
    #print(fits(pop[l],dist))
    print("last best:", lbk)
    return pop[l], fitnes[l],



if __name__ == "__main__":
    N = 9
    C = 2
    pts,dist,chargers = map.carte(N,5,chargers=C)
    cities = [a for a in range(N)]
    D = [0,7,3,5,1,8,2,0],[0,4,6,0]
    P = [0,4,3,2,1,0],[0,7,8,6,5,0]

    posize = 8
    iter = 100
    batt = 14

    paths, cos = Memetic(posize,cities,dist,3,chargers,batt,DmSize=3,iter=iter,Mprob=0.8)
    print(chargers)
    print(paths, cos ,)
    #print(PopGen(2,cities,[0,1,2],dist))
    #print(shake(P,D,1,3))

    print(feasibles(paths,dist,chargers,batt,details=True))

    map.drawVRP(paths,pts,chargers)

    """paths, cos = Memetic(posize,cities,dist,DmSize=5,Ncars=3,iter=iter,tab=False)
    print(paths, cos )
    map.drawVRP(paths,pts)"""

    """P=[]
    for p in D:
        for c in chargers:
            p = [x for x in p if x!=c]
        print("\tb4",p)
        p = tabucharge(p,dist,chargers,batt,max_iter=10)[0]
        print("\t\taft",p)
        P.append(p)
    print(chargers)
    print(P)
    print(feasibles(P,dist,chargers,batt,details=True))
    map.drawVRP(P,pts,chargers)"""


    """PopSize = 8
    Ncars = 3

    pop = PopGen(PopSize,[0, 1, 2, 3, 4, 5, 6, 7, 8],[i for i in range(Ncars)],dist, chargers, batt, feasibility = True)
    for i in pop:
        print("===",i)
        print(feasibles(i,dist,chargers,batt,details=True))
    map.drawVRP(random.choice(pop),pts,chargers)"""

    #print([[0, 7, 0], [0, 0], [0, 3, 1, 4, 6, 8, 5, 2, 0]])
    #print(decharge([[0, 7, 0], [0, 0], [0, 3, 1, 4, 6, 8, 5, 2, 0]],[2, 1, 5, 4, 8]))

