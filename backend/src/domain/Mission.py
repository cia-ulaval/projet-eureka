import random


class Mission:
    # liste des points de départ et d'arrivée possibles
    MISSIONS: list[list[[int, int], [int, int]]] = [
        [[4, 9], [21, 18]],
        [[20, 18], [9, 9]]
    ]

    def __init__(self):
        self.start: [int, int] = [4, 9]
        self.end: [int, int] = [21, 18]
        self.generate_mission()

    def generate_mission(self) -> ([int, int], [int, int]):
        self.start, self.end = random.choice(Mission.MISSIONS)
        return self.start, self.end
