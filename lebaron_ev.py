import numpy as np
import random
from copy import deepcopy

from memetic_karny import feasible, feasibles, tabucharge


def lebaron_vrp(
    dist,
    chargers,
    battery,
    vehicles=3,
    agents=20,
    iterations=300,
    learning_rate=0.1,
    exploration=0.2,
    decay=0.99
):

    cities = len(dist)

    # Learned transition memory
    memory = np.ones((cities, cities))

    customers = [i for i in range(1, cities)]

    feasible_memory = []
    infeasible_memory = []

    def split_routes(path):

        chunks = np.array_split(path, vehicles)

        routes = []

        for chunk in chunks:
            routes.append([0] + list(chunk) + [0])

        return routes

    best_routes = None
    best_cost = float("inf")

    for iteration in range(iterations):

        for agent in range(agents):

            # ==================================
            # BUILD SOLUTION
            # ==================================

            unvisited = customers[:]
            current = 0
            path = []

            while len(unvisited) > 0:

                scores = []

                for nxt in unvisited:

                    mem = memory[current][nxt]

                    heuristic = 1.0 / (
                        dist[current][nxt] + 1e-6
                    )

                    scores.append(mem * heuristic)

                scores = np.array(scores)

                if scores.sum() == 0:
                    probs = np.ones(len(scores)) / len(scores)
                else:
                    probs = scores / scores.sum()

                if random.random() < exploration:

                    nxt = random.choice(unvisited)

                else:

                    nxt = np.random.choice(
                        unvisited,
                        p=probs
                    )

                path.append(nxt)

                unvisited.remove(nxt)

                current = nxt

            routes = split_routes(path)

            # ==================================
            # REPAIR PHASE
            # ==================================

            repaired_routes = []

            solution_feasible = True

            for route in routes:

                score, ok = feasible(
                    route,
                    dist,
                    chargers,
                    battery,
                    details=True
                )

                if not ok:

                    solution_feasible = False

                    route, score = tabucharge(
                        route,
                        dist,
                        chargers,
                        battery,
                        max_iter=20
                    )

                    score, ok = feasible(
                        route,
                        dist,
                        chargers,
                        battery,
                        details=True
                    )

                    if ok:
                        solution_feasible = True

                repaired_routes.append(route)

            routes = repaired_routes

            # ==================================
            # EVRP FITNESS
            # ==================================

            cost, solution_feasible = feasibles(
                routes,
                dist,
                chargers,
                battery,
                details=True
            )

            # ==================================
            # DUAL MEMORY
            # ==================================

            if solution_feasible:

                feasible_memory.append(
                    (
                        deepcopy(routes),
                        cost
                    )
                )

                feasible_memory.sort(
                    key=lambda x: x[1]
                )

                feasible_memory = feasible_memory[:20]

            else:

                infeasible_memory.append(
                    (
                        deepcopy(routes),
                        cost
                    )
                )

                infeasible_memory.sort(
                    key=lambda x: x[1]
                )

                infeasible_memory = infeasible_memory[:20]

            # ==================================
            # BEST SOLUTION
            # ==================================

            if solution_feasible and cost < best_cost:

                best_cost = cost
                best_routes = deepcopy(routes)

            # ==================================
            # LEARNING UPDATE
            # ==================================

            reward = (
                2.0
                if solution_feasible
                else 0.5
            )

            for route in routes:

                for i in range(len(route) - 1):

                    a = route[i]
                    b = route[i + 1]

                    memory[a][b] += (
                        reward
                        * learning_rate
                        / (cost + 1e-6)
                    )

                    memory[b][a] = memory[a][b]

        # ==================================
        # FORGETTING
        # ==================================

        memory *= decay

    return best_routes, best_cost


if __name__ == "__main__":

    import map

    N = 12
    batt = 15

    pts, dist, chargers = map.carte(
        N,
        5,
        chargers=int(N / 5)
    )

    routes, cost = lebaron_vrp(
        dist,
        chargers,
        batt,
        vehicles=3,
        agents=30,
        iterations=300
    )

    print("\nChargers:")
    print(chargers)

    print("\nRoutes:")
    print(routes)

    print("\nCost:")
    print(cost)

    print(
        "\nFeasible:",
        feasibles(
            routes,
            dist,
            chargers,
            batt,
            details=True
        )
    )

    map.drawVRP(
        routes,
        pts,
        chargers
    )
