import matplotlib.pyplot as plt
import numpy as np
import time
import map

from memetic_final import Memetic
from lebaron_ev import lebaron_vrp

def exec_time(num_nodes,num_char,batt, iter = 100):
    pts,dist,timemtx,chargers = map.generate_map(num_nodes,num_char)
    cities = [a for a in range(num_nodes)]

    start = time.perf_counter()

    Memetic(8,cities,dist, timemtx,3,chargers,batt,DmSize=3,iter=iter)

    stop = time.perf_counter()
    memetic_time = stop-start
    
    start = time.perf_counter()

    lebaron_vrp(
        dist,
        timemtx,
        chargers,
        batt,
        vehicles=3,
        agents=30,
        iterations=iter
    )

    stop = time.perf_counter()
    lebaron_time = stop-start

    return memetic_time,lebaron_time

if __name__ == "__main__":

    ch = 5
    batt = 10

    M = []
    L = []
    X = []

    for n in range(1,10):
        size = 5+(n*3)
        print("=====",size,"nodes =====")
        m,l = exec_time(size,ch,batt)
        M.append(m)
        L.append(l)
        X.append(size)
        print("\tMemetic:",m,"\tLeBaron",l)
    
    plt.plot(X,M, label="Memetic")
    plt.plot(X,L, label="LeBaron")

    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time [s]")
    plt.legend()

    plt.show()
