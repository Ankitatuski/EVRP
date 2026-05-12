import numpy as np
import random
from copy import deepcopy
import map

# replicationg https://ieeexplore.ieee.org/abstract/document/9194245
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


def Memetic (PopSize, pts, dist, Ncars, DmSize=2, Kmax=3, Smin=1, Smax=2, Mprob=1, Vini=0, Vlim=3,iter = 30):
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
    print (pop,"\n",Dm)

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
                T3 = T2 #tbc local

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
                        while( pop[j] in Dm):
                            fcopy[j] = mx
                            j = fcopy.index(min(fcopy))
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
        print(min(fitnes))
        iterator+=1
    l = fitnes.index(min(fitnes))
    print(fits(pop[l],dist))
    return pop[l], fitnes[l],



if __name__ == "__main__":
    N = 10
    pts,dist = map.carte(N,5)
    cities = [a for a in range(N)]
    D = [0,7,3,5,1,8,2,0],[0,4,6,0]
    P = [0,4,3,2,1,0],[0,7,8,6,5,0]

    paths, cos = Memetic(10,cities,dist,DmSize=5,Ncars=3,iter=30)
    print(paths, cos )
    #print(PopGen(2,cities,[0,1,2],dist))
    #print(shake(P,D,1,3))


    map.drawVRP(paths,pts)
