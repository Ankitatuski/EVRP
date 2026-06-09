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

    def normalize(self, value, max_value):

        if max_value == 0:
            return 0

        return value / max_value

    def choose(self, memetic, lebaron):

        max_distance = max(
            memetic["distance"],
            lebaron["distance"]
        )

        max_time = max(
            memetic["time"],
            lebaron["time"]
        )

        max_energy = max(
            memetic["energy"],
            lebaron["energy"]
        )

        memetic_score = (

            self.distance_weight *
            self.normalize(
                memetic["distance"],
                max_distance
            )

            +

            self.time_weight *
            self.normalize(
                memetic["time"],
                max_time
            )

            +

            self.energy_weight *
            self.normalize(
                memetic["energy"],
                max_energy
            )

        )

        lebaron_score = (

            self.distance_weight *
            self.normalize(
                lebaron["distance"],
                max_distance
            )

            +

            self.time_weight *
            self.normalize(
                lebaron["time"],
                max_time
            )

            +

            self.energy_weight *
            self.normalize(
                lebaron["energy"],
                max_energy
            )

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
