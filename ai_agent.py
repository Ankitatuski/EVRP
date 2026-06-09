class EVRoutingAgent:

    def __init__(self):

        pass

    def normalize(
        self,
        value,
        max_value
    ):

        if max_value == 0:
            return 0

        return value / max_value

    def choose(

        self,

        memetic,

        lebaron

    ):

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

            self.normalize(
                memetic["distance"],
                max_distance
            )

            +

            self.normalize(
                memetic["time"],
                max_time
            )

            +

            self.normalize(
                memetic["energy"],
                max_energy
            )

        )

        lebaron_score = (

            self.normalize(
                lebaron["distance"],
                max_distance
            )

            +

            self.normalize(
                lebaron["time"],
                max_time
            )

            +

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
