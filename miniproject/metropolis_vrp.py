import numpy as np
import random
from copy import deepcopy

def metropolis_vrp(paths, dist, iterations=300):

    def pathlen(path):
        return sum(dist[path[i], path[i+1]] for i in range(len(path)-1))

    def total_cost(paths):
        return sum(pathlen(p) for p in paths)

    def mutate_route(route):
        if len(route) <= 3:
            return route
        a, b = random.sample(range(1, len(route)-1), 2)
        nr = deepcopy(route)
        nr[a], nr[b] = nr[b], nr[a]
        return nr

    current = deepcopy(paths)
    current_cost = total_cost(current)

    for _ in range(iterations):
        candidate = deepcopy(current)

        r = random.randint(0, len(candidate)-1)
        candidate[r] = mutate_route(candidate[r])

        cand_cost = total_cost(candidate)
        delta = cand_cost - current_cost

        if delta < 0 or random.random() < np.exp(-delta / max(current_cost, 1)):
            current = candidate
            current_cost = cand_cost

    return current, current_cost
