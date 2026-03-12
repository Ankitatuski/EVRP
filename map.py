import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def carte(n, size, demand=0, plot = False):
    pts = points(n,abs(size))
    m = distanceMatrix(pts)

    if demand>0:
        for a in pts:
            a.append(random.randrange(0,demand))
    else:
        for a in pts:
            a.append(0)

    if plot:
        x = [point[0] for point in pts]
        y = [point[1] for point in pts]
        plt.scatter(x, y)
        plt.scatter(pts[0][0],pts[0][1], color = 'red')
        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        plt.grid(True)
        plt.show()
    return pts,m
    

def points(x,d):
    r = []
    for a in range (x):
        r.append([random.randint(-d, d),random.randint(-d, d)])
    return r

def distanceMatrix(p):
    n = len(p)
    m = (np.zeros((n,n)))
    for a in range (n):
        for b in range (a,n):
            m[a,b] = abs(p[a][0]-p[b][0])+abs(p[a][1]-p[b][1])
    return m


if __name__=="__main__":
    print(carte(50,20,plot = True))