from backend.src.domain.Map import Map
from backend.src.domain.Mission import Mission


class MapService:
    def __init__(self, map: Map, mission: Mission):
        self.__map = map
        self.__mission = mission

    def get_traffic(self) -> list[list[float]]:
        return self.__map.generate_traffic()

    def get_start_and_end(self) -> ([int, int], [int, int]):
        return self.__mission.generate_mission()
