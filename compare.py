import time
import numpy as np
import pandas as pd
import map

from copy import deepcopy
from traditional import metropolis_vrp, ant_vrp, tabu_vrp, genetic_vrp
from memetic_rep import Memetic
from lebaron import lebaron

def split_vrp(cities, num_vehicles=3):
    arr = np.random.permutation([i for i in range(1, cities)])
    chunks = np.array_split(arr, num_vehicles)
    return [np.concatenate(([0], c, [0])) for c in chunks]

def benchmark(cities = 16):
    pts, dist = map.carte(cities, 5)
    vrp_init = split_vrp(cities, 3)

    tsp_results = []
    vrp_results = []

    # ---------------- VRP ----------------
    vrp_algorithms = {
        "Metropolis": lambda: metropolis_vrp(vrp_init, dist),
        "Tabu": lambda: tabu_vrp(vrp_init, dist),
        "Genetic": lambda: genetic_vrp(vrp_init, dist),
        "Ant Colony": lambda: ant_vrp(dist, vehicles=3),
        "Lebaron": lambda: lebaron(dist),
        "Memetic": lambda: Memetic(10,[a for a in range(cities)],dist,3,5)
    }


    for name, algo in vrp_algorithms.items():
        start = time.time()
        routes, cost = algo()
        runtime = time.time() - start
        vrp_results.append([name, round(cost, 2), round(runtime, 4)])

    # ---------------- Tables ----------------
    tsp_df = pd.DataFrame(tsp_results, columns=["Algorithm", "Cost", "Exec Time (s)"])
    vrp_df = pd.DataFrame(vrp_results, columns=["Algorithm", "Cost", "Exec Time (s)"])

    #print("\n===== TSP Comparison =====")
    #print(tsp_df.to_string(index=False))

    print("\n===== VRP Comparison =====")
    print(vrp_df.to_string(index=False))

    
if __name__ == "__main__":
    benchmark(cities = 20)
