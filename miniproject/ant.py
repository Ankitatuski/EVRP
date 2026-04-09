import map
import numpy as np
from copy import deepcopy
import random

def mrówkowojażer(pts,dist,alfa=1,beta=1,evaporation = 0.5,display = False,iter=3,ants=3):
    cities = len(pts)
    #print (dist)

    def pathlen(p):
        r=0
        for a in range(len(p)-1):
            r+=dist[p[a],p[a+1]]
        return r

    phrm = deepcopy(dist)**0     #pheromons matrix
    def t(k):
        r = evaporation

    k=0
    while k<iter:
        if display:
            print("---k=",k)
        for j in range(ants):
            path = [0,]
            set = [i for i in range(1,cities)]    #not yet visited
            while len(set)>0:
                #print("set",set)
                #print("path",path)
                set2 = deepcopy((set))  #potential to visit
                for i in set2:
                    #print("set2",set2)
                    if len(set2) == 1:
                        path.append(i)
                        set.remove(i)
                        set2.clear
                        #break
                    r = random.randint(0,100)
                    p = (phrm[path[-1]][i])**alfa * (dist[path[-1]][i])**beta
                    Z = sum( (phrm[path[-1]][l])**alfa * (dist[path[-1]][l])**beta for l in set)
                    #print("p z",p,Z)
                    p/=Z
                    #print("p r",p,r)
                    if (r<= p*100):
                        path.append(i)
                        set.remove(i)
                        set2.clear
                        #break
                    else:
                        set2.remove(i)
            for i in range(1,len(path)):
                a = path[i-1]
                b = path[i]
                phrm[a][b] += 1/(pathlen(path))
                phrm[b][a] = phrm[a][b]
            if display:
                print(k,j,path,pathlen(path))
            phrm*=evaporation
        k+=1
    if display:
        print(np.round(phrm,2))
    return path
                    
if __name__=="__main__":
    cities=8
    pts,dist = map.carte(cities,5)#,plot=True)
    mrówkowojażer(pts,dist,display=True)