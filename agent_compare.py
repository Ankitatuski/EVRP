import map

from memetic_karny import Memetic
from lebaron_ev import lebaron_vrp

from ai_agent import EVRoutingAgent


def total_distance(routes, dist):

    total = 0

    for route in routes:

        for i in range(len(route) - 1):

            total += dist[
                route[i]
            ][
                route[i + 1]
            ]

    return total


def total_time(routes, time_matrix):

    total = 0

    for route in routes:

        for i in range(len(route) - 1):

            total += time_matrix[
                route[i]
            ][
                route[i + 1]
            ]

    return total


N = 15
BATTERY = 5

pts, dist, time, chargers = map.generate_map(
    N,
    int(N / 5),
    type="real"
)

cities = [i for i in range(N)]


print("\nRunning Memetic...")

mem_routes, mem_cost = Memetic(
    8,
    cities,
    dist,
    time,
    3,
    chargers,
    BATTERY,
    iter=50
)


print("\nRunning LeBaron...")

leb_routes, leb_cost = lebaron_vrp(
    dist,
    time,
    chargers,
    BATTERY,
    vehicles=3,
    iterations=100
)


mem_distance = total_distance(
    mem_routes,
    dist
)

mem_time = total_time(
    mem_routes,
    time
)

mem_energy = mem_cost


leb_distance = total_distance(
    leb_routes,
    dist
)

leb_time = total_time(
    leb_routes,
    time
)

leb_energy = leb_cost


agent = EVRoutingAgent()


decision = agent.choose(

    {
        "distance": mem_distance,
        "time": mem_time,
        "energy": mem_energy
    },

    {
        "distance": leb_distance,
        "time": leb_time,
        "energy": leb_energy
    }

)


print("\n==============================")
print("MEMETIC")
print("==============================")

print("Distance:", mem_distance)
print("Time:", mem_time)
print("Energy:", mem_energy)


print("\n==============================")
print("LEBARON")
print("==============================")

print("Distance:", leb_distance)
print("Time:", leb_time)
print("Energy:", leb_energy)


print("\n==============================")
print("AI AGENT DECISION")
print("==============================")

print(decision)
