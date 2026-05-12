import numpy as np
import random
from copy import deepcopy

def lebaron(
    dist,
    vehicles=3,
    agents=20,
    iterations=300,
    learning_rate=0.1,
    exploration=0.2,
    decay=0.99
):

    cities = len(dist)

    # Adaptive memory matrix
    memory = np.ones((cities, cities))
    customers = list(range(1, cities))

    # Split route into vehicles
    def split_routes(path):

        chunks = np.array_split(path, vehicles)

        routes = []

        for c in chunks:
            route = [0] + list(c) + [0]
            routes.append(route)

        return routes

    # Route cost
    def route_cost(route):

        return sum(
            dist[route[i], route[i+1]]
            for i in range(len(route)-1)
        )

    def total_cost(routes):

        return sum(route_cost(r) for r in routes)

    # Best solution
    best_routes = None
    best_cost = float("inf")

    # Main optimization loop
    for _ in range(iterations):

        for _ in range(agents):

            path = []
            unvisited = customers[:]

            # Construct route adaptively
            current = 0

            while unvisited:

                scores = []

                for nxt in unvisited:

                    # learned preference
                    mem = memory[current][nxt]

                    # heuristic preference
                    heuristic = 1 / (dist[current][nxt] + 1e-6)

                    score = mem * heuristic

                    scores.append(score)

                scores = np.array(scores)

                # normalize probabilities
                probs = scores / scores.sum()

                # exploration vs exploitation
                if random.random() < exploration:
                    next_city = random.choice(unvisited)
                else:
                    next_city = np.random.choice(unvisited, p=probs)

                path.append(next_city)

                unvisited.remove(next_city)

                current = next_city

            # Convert to VRP routes
            routes = split_routes(path)

            cost = total_cost(routes)

            # Update best solution
            if cost < best_cost:
                best_cost = cost
                best_routes = deepcopy(routes)

            # Adaptive learning update
            for route in routes:

                for i in range(len(route)-1):

                    a = route[i]
                    b = route[i+1]

                    # reinforce good decisions
                    memory[a][b] += learning_rate / (cost + 1e-6)
                    memory[b][a] = memory[a][b]

        # Forgetting / adaptation
        memory *= decay

    return best_routes, best_cost

# TEST
if __name__ == "__main__":

    import map2

    pts, dist = map2.carte(16, 5)

    routes, cost = lebaron(dist, vehicles=3)

    print("\nLeBaron Routes:")
    print(routes)

    print("\nCost:")
    print(cost)
