import map

from memetic_karny import Memetic
from lebaron_ev import lebaron_vrp

from ai_agent import EVRoutingAgent


N = 15
BATTERY = 5

pts, dist, time, chargers = map.generate_map(
    N,
    int(N/5),
    type="real"
)

cities = [i for i in range(N)

]

# MEMETIC
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

# LEBARON
leb_routes, leb_cost = lebaron_vrp(
    dist,
    time,
    chargers,
    BATTERY,
    vehicles=3,
    iterations=100
)

agent = EVRoutingAgent()

memetic_result = {
    "distance": mem_cost,
    "time": mem_cost,
    "energy": mem_cost
}

lebaron_result = {
    "distance": leb_cost,
    "time": leb_cost,
    "energy": leb_cost
}

decision = agent.choose(
    memetic_result,
    lebaron_result
)

print("\nAI Agent Decision")
print(decision)
