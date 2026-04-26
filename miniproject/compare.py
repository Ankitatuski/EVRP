import time
import numpy as np
import pandas as pd
import map

from copy import deepcopy
from ant import mrówkowojażer
from genetic_tsp import genetic_tsp
from metropolis_vrp import metropolis_vrp
from ant_vrp import ant_vrp


# Helpers
def pathlen(path, dist):
    return sum(dist[path[i], path[i+1]] for i in range(len(path)-1))


def pathlens(paths, dist):
    return sum(pathlen(p, dist) for p in paths)


def mutate(path):
    import random
    from copy import deepcopy
    a, b = random.sample(range(1, len(path)), 2)
    npath = deepcopy(path)
    npath[a], npath[b] = npath[b], npath[a]
    return npath


def greedy_tsp(dist):
    cities = len(dist)
    path = [0]
    cost = 0

    while len(path) < cities:
        a = path[-1]
        best = None
        best_d = float("inf")

        for b in range(cities):
            if b != a and b not in path and dist[a][b] < best_d:
                best = b
                best_d = dist[a][b]

        path.append(best)
        cost += best_d

    return path, cost


def split_vrp(cities, num_vehicles=3):
    arr = np.random.permutation([i for i in range(1, cities)])
    chunks = np.array_split(arr, num_vehicles)
    return [np.concatenate(([0], c, [0])) for c in chunks]


# TSP Algorithms
def metropolis_tsp(dist, iterations=300):
    path, cost = greedy_tsp(dist)

    for _ in range(iterations):
        npath = mutate(path)
        ncost = pathlen(npath, dist)
        delta = ncost - cost

        if delta < 0 or np.random.rand() < np.exp(-delta / max(cost, 1)):
            path, cost = npath, ncost

    return path, cost


def tabu_tsp(dist, iterations=300):
    path, cost = greedy_tsp(dist)
    tabu = []

    for _ in range(iterations):
        npath = mutate(path)
        ncost = pathlen(npath, dist)

        if ncost < cost and npath not in tabu:
            tabu.append(deepcopy(path))
            path, cost = npath, ncost

        if len(tabu) > 25:
            tabu = tabu[5:]

    return path, cost


# VRP Algorithms
def tabu_vrp(paths, dist, iterations=300):
    import random

    def crois(paths):
        paths = deepcopy(paths)
        for i in range(len(paths)-1):
            if len(paths[i]) > 2 and len(paths[i+1]) > 2:
                r1 = random.randint(1, len(paths[i])-2)
                r2 = random.randint(1, len(paths[i+1])-2)
                paths[i][r1], paths[i+1][r2] = paths[i+1][r2], paths[i][r1]
        return paths

    current = deepcopy(paths)
    current_cost = pathlens(current, dist)
    tabu = []

    for _ in range(iterations):
        candidate = crois(current)
        cand_cost = pathlens(candidate, dist)

        if cand_cost < current_cost and candidate not in tabu:
            tabu.append(deepcopy(current))
            current, current_cost = candidate, cand_cost

        if len(tabu) > 25:
            tabu = tabu[5:]

    return current, current_cost


def genetic_vrp(paths, dist, iterations=300, pop_size=30):
    import random

    def crois(paths):
        paths = deepcopy(paths)
        for i in range(len(paths)-1):
            if len(paths[i]) > 2 and len(paths[i+1]) > 2:
                r1 = random.randint(1, len(paths[i])-2)
                r2 = random.randint(1, len(paths[i+1])-2)
                paths[i][r1], paths[i+1][r2] = paths[i+1][r2], paths[i][r1]
        return paths

    def evolve(paths):
        npaths = crois(paths)
        return npaths, pathlens(npaths, dist)

    pop = [deepcopy(paths) for _ in range(pop_size)]
    best = deepcopy(paths)
    best_cost = pathlens(paths, dist)

    for _ in range(iterations):
        costs = [pathlens(p, dist) for p in pop]
        ranked = [x for _, x in sorted(zip(costs, pop), key=lambda z: z[0])]
        pop = ranked[:pop_size//2]

        while len(pop) < pop_size:
            p = deepcopy(np.random.choice(pop))
            child, _ = evolve(p)
            pop.append(child)

        candidate = pop[0]
        cand_cost = pathlens(candidate, dist)

        if cand_cost < best_cost:
            best = deepcopy(candidate)
            best_cost = cand_cost

    return best, best_cost


# Runner
def benchmark():
    cities = 16
    pts, dist = map.carte(cities, 5)
    vrp_init = split_vrp(cities, 3)

    tsp_results = []
    vrp_results = []

    # ---------------- TSP ----------------
    tsp_algorithms = {
        "Metropolis": lambda: metropolis_tsp(dist),
        "Tabu": lambda: tabu_tsp(dist),
        "Ant Colony": lambda: (mrówkowojażer(pts, dist, ants=20, iter=30), None),
        "Genetic": lambda: genetic_tsp(dist),
    }

    for name, algo in tsp_algorithms.items():
        start = time.time()
        route, cost = algo()
        runtime = time.time() - start

        if cost is None:
            cost = pathlen(route, dist)

        tsp_results.append([name, round(cost, 2), round(runtime, 4)])

    # ---------------- VRP ----------------
    vrp_algorithms = {
        "Metropolis": lambda: metropolis_vrp(vrp_init, dist),
        "Tabu": lambda: tabu_vrp(vrp_init, dist),
        "Ant Colony": lambda: ant_vrp(dist, vehicles=3),
        "Genetic": lambda: genetic_vrp(vrp_init, dist),
    }

    for name, algo in vrp_algorithms.items():
        start = time.time()
        routes, cost = algo()
        runtime = time.time() - start
        vrp_results.append([name, round(cost, 2), round(runtime, 4)])

    # ---------------- Tables ----------------
    tsp_df = pd.DataFrame(tsp_results, columns=["Algorithm", "Cost", "Time (s)"])
    vrp_df = pd.DataFrame(vrp_results, columns=["Algorithm", "Cost", "Time (s)"])

    print("\n===== TSP Comparison =====")
    print(tsp_df.to_string(index=False))

    print("\n===== VRP Comparison =====")
    print(vrp_df.to_string(index=False))


if __name__ == "__main__":
    benchmark()
