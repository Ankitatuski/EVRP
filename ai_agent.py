import numpy as np

class EVRoutingAgent:

    def __init__(
        self,
        distance_weight=0.4,
        time_weight=0.3,
        energy_weight=0.3
    ):

        self.distance_weight = distance_weight
        self.time_weight = time_weight
        self.energy_weight = energy_weight

    def evaluate(
        self,
        distance,
        travel_time,
        energy
    ):

        return (
            self.distance_weight * distance
            + self.time_weight * travel_time
            + self.energy_weight * energy
        )

    def choose(
        self,
        memetic_result,
        lebaron_result
    ):

        memetic_score = self.evaluate(
            memetic_result["distance"],
            memetic_result["time"],
            memetic_result["energy"]
        )

        lebaron_score = self.evaluate(
            lebaron_result["distance"],
            lebaron_result["time"],
            lebaron_result["energy"]
        )

        if memetic_score < lebaron_score:

            return {
                "algorithm": "Memetic",
                "score": memetic_score
            }

        return {
            "algorithm": "LeBaron",
            "score": lebaron_score
        }
