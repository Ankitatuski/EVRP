import numpy as np
import random
from copy import deepcopy

def genetic_tsp(dist, pop_size=30, generations=300):

    cities = len(dist)

    def pathlen(path):
        return sum(dist[path[i], path[i+1]] for i in range(len(path)-1))

    def mutate(path):
        a, b = random.sample(range(1, len(path)), 2)
        npath = deepcopy(path)
        npath[a], npath[b] = npath[b], npath[a]
        return npath

    def crossover(p1, p2):
        a, b = sorted(random.sample(range(1, len(p1)), 2))
        child = [-1] * len(p1)
        child[a:b] = p1[a:b]

        fill = [x for x in p2 if x not in child]
        ptr = 0
        for i in range(len(child)):
            if child[i] == -1:
                child[i] = fill[ptr]
                ptr += 1
        return child

    # initial population
    base = list(range(cities))
    pop = []
    for _ in range(pop_size):
        p = [0] + random.sample(range(1, cities), cities-1)
        pop.append(p)

    best = None
    best_cost = float("inf")

    for _ in range(generations):
        costs = [pathlen(p) for p in pop]
        ranked = [x for _, x in sorted(zip(costs, pop), key=lambda z: z[0])]

        if min(costs) < best_cost:
            best = deepcopy(ranked[0])
            best_cost = min(costs)

        survivors = ranked[:pop_size//2]
        new_pop = deepcopy(survivors)

        while len(new_pop) < pop_size:
            p1, p2 = random.sample(survivors, 2)
            child = crossover(p1, p2)
            if random.random() < 0.3:
                child = mutate(child)
            new_pop.append(child)

        pop = new_pop

    return best, best_cost
