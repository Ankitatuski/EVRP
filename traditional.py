import numpy as np
import random
from copy import deepcopy

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
    
    def to_hashable(sol):
        return tuple(tuple(arr) for arr in sol)

    current = deepcopy(paths)
    current_cost = pathlens(current, dist)
    tabu = []

    for _ in range(iterations):
        candidate = crois(current)
        #print("candidate:",candidate,"\ntabu:",tabu)
        cand_cost = pathlens(candidate, dist)

        if (cand_cost < current_cost) and (to_hashable(candidate) not in [to_hashable(t) for t in tabu]):
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
            #print("pop = ",pop)
            p = deepcopy(random.choice(pop))
            child, _ = evolve(p)
            pop.append(child)

        candidate = pop[0]
        cand_cost = pathlens(candidate, dist)

        if cand_cost < best_cost:
            best = deepcopy(candidate)
            best_cost = cand_cost

    return best, best_cost

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


