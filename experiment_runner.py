import csv
import map

from memetic_karny import Memetic
from lebaron_ev import lebaron_vrp
from ai_agent import EVRoutingAgent


EXPERIMENTS = 30

NODES = 15
BATTERY = 5
VEHICLES = 3

agent = EVRoutingAgent()


with open("results.csv", "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "Experiment",
        "MemeticCost",
        "LeBaronCost",
        "Winner"
    ])

    for exp in range(EXPERIMENTS):

        print(f"\nRunning experiment {exp+1}")

        pts, dist, time, chargers = map.generate_map(
            NODES,
            int(NODES/5),
            type="real"
        )

        cities = [i for i in range(NODES)]

        # Memetic
        mem_routes, mem_cost = Memetic(
            8,
            cities,
            dist,
            time,
            VEHICLES,
            chargers,
            BATTERY,
            iter=50
        )

        # LeBaron
        leb_routes, leb_cost = lebaron_vrp(
            dist,
            time,
            chargers,
            BATTERY,
            vehicles=VEHICLES,
            iterations=100
        )

        decision = agent.choose(
            {
                "distance": mem_cost,
                "time": mem_cost,
                "energy": mem_cost
            },
            {
                "distance": leb_cost,
                "time": leb_cost,
                "energy": leb_cost
            }
        )

        writer.writerow([
            exp + 1,
            mem_cost,
            leb_cost,
            decision["algorithm"]
        ])

print("\nResults saved to results.csv")
