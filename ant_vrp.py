import numpy as np
import random
from copy import deepcopy

def ant_vrp(dist, vehicles=3, ants=20, iterations=50, alpha=1, beta=2, evaporation=0.5):

    n = len(dist)
    pher = np.ones((n, n))
    customers = list(range(1, n))

    def split_routes(path):
        chunks = np.array_split(path, vehicles)
        routes = []
        for c in chunks:
            route = [0] + list(c) + [0]
            routes.append(route)
        return routes

    def route_cost(route):
        return sum(dist[route[i], route[i+1]] for i in range(len(route)-1))

    def total_cost(routes):
        return sum(route_cost(r) for r in routes)

    best_routes = None
    best_cost = float("inf")

    for _ in range(iterations):
        all_solutions = []

        for _ in range(ants):
            unvisited = customers[:]
            path = [0]

            while unvisited:
                current = path[-1]
                probs = []

                for j in unvisited:
                    tau = pher[current][j] ** alpha
                    eta = (1 / (dist[current][j] + 1e-6)) ** beta
                    probs.append(tau * eta)

                probs = np.array(probs)
                probs = probs / probs.sum()

                nxt = np.random.choice(unvisited, p=probs)
                path.append(nxt)
                unvisited.remove(nxt)

            routes = split_routes(path[1:])
            cost = total_cost(routes)
            all_solutions.append((routes, cost))

            if cost < best_cost:
                best_routes = deepcopy(routes)
                best_cost = cost

        pher *= evaporation

        for routes, cost in all_solutions:
            for route in routes:
                for i in range(len(route)-1):
                    a, b = route[i], route[i+1]
                    pher[a][b] += 1 / cost
                    pher[b][a] += 1 / cost

    return best_routes, best_cost
