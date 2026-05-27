import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def carte(n, size, demand=0, chargers=0, plot = False, full = True):
    pts = points(n,abs(size))   #[x,y,demand/-charging_rate]
    m = distanceMatrix(pts)

    if full:
        for a in range (n):
            for b in range (a,n):
                m[b,a] = m[a,b]

                
    if demand>0:
        for a in pts:
            a.append(random.randrange(0,demand))
    else:
        for a in pts:
            a.append(0)

    chargers_list = []
    indexes = [i for i in range(1,n)]
    for a in range(chargers):
        i = random.choice(indexes)
        pts[i][2] = -1
        chargers_list.append(i)
        indexes.remove(i)

    if plot:
        x = [point[0] for point in pts]
        y = [point[1] for point in pts]
        plt.scatter(x, y)
        plt.scatter(pts[0][0],pts[0][1], color = 'red')
        for a in chargers_list:
            plt.scatter(pts[a][0],pts[a][1], color = 'green')
        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        plt.grid(True)
        plt.show()
    if chargers>0:
        return pts,m,chargers_list
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
            #m[a,b] = abs(p[a][0]-p[b][0])+abs(p[a][1]-p[b][1])             #manhattan
            m[a,b] = np.sqrt((p[a][0]-p[b][0])**2+(p[a][1]-p[b][1])**2)     #euclidean
    return m

def draw(path, cords, chargers=[]):
    x = [cords[p][0] for p in path]
    y = [cords[p][1] for p in path]

    colors = ([
    'tab:blue',
    'tab:orange',
    #'tab:green',
    'tab:red',
    'tab:purple',
    'tab:brown',
    'tab:pink',
    'tab:gray',
    'tab:olive',
    'tab:cyan'
    ])

    plt.plot(x, y, marker='.', linestyle='-', color=random.choice(colors))
    plt.plot(x[0],y[0], marker='o', color="red")
    for a in chargers:
        plt.scatter(cords[a][0],cords[a][1], color = 'green', marker='o')

def drawVRP(paths,cords, chargers = []):
    for path in paths:
        draw(path,cords)
    for a in chargers:
        plt.scatter(cords[a][0],cords[a][1], color = 'green', marker='o')
    plt.show()


if __name__=="__main__":
    print(carte(5,10,chargers=2,plot = True))

    """pts,m = (carte(10,20,plot = True))
    draw([a for a in range(10)],pts)
    plt.show()"""