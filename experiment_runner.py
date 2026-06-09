import csv
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


EXPERIMENTS = 30

NODES = 15
BATTERY = 5
VEHICLES = 3

agent = EVRoutingAgent()

with open(
    "results.csv",
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "Experiment",

        "MemeticDistance",
        "MemeticTime",
        "MemeticEnergy",

        "LeBaronDistance",
        "LeBaronTime",
        "LeBaronEnergy",

        "Winner"

    ])

    for exp in range(EXPERIMENTS):

        print(
            f"\nRunning Experiment {exp+1}"
        )

        pts, dist, time, chargers = map.generate_map(
            NODES,
            int(NODES / 5),
            type="real"
        )

        cities = [i for i in range(NODES)]

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

        leb_routes, leb_cost = lebaron_vrp(
            dist,
            time,
            chargers,
            BATTERY,
            vehicles=VEHICLES,
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

        writer.writerow([

            exp + 1,

            mem_distance,
            mem_time,
            mem_energy,

            leb_distance,
            leb_time,
            leb_energy,

            decision["algorithm"]

        ])

print(
    "\nResults saved to results.csv"
)
