from backend.src.domain.Scorer import Scorer
from backend.src.domain.AStar import AStar
from backend.src.domain.Map import Map
from backend.src.domain.Mission import Mission


class ScoringService:
    def __init__(self, map: Map, mission: Mission, scorer: Scorer = Scorer(), path_finder: AStar = None):
        self.__map: Map = map
        self.__mission: Mission = mission
        self.__scorer: Scorer = scorer
        self.__path_finder: AStar = path_finder if path_finder is not None \
            else AStar(self.__map.width, self.__map.height)

    def get_score(self, path: list[(int, int)] or None) -> (float, float):
        if path is None:
            return 0, 0

        maps = self.__map.get_map()
        co2_total, wait_total = self.__scorer.get_stats_from_path(path, maps)
        return co2_total, wait_total

    def get_ai_score(self) -> list[[int, int]]:
        maps = self.__map.get_map()
        obstacles: list[[int, int]] = self.__map.get_obstacle_list()
        ai_path: list[[int, int]] = self.__path_finder.run_AStar(obstacles, maps,
                                                                 self.__mission.start, self.__mission.end)
        co2_total, waiting_time_total, final_ai_path = self.__scorer.get_stats_from_AStar(ai_path, self.__mission.end)
        return co2_total, waiting_time_total, final_ai_path
