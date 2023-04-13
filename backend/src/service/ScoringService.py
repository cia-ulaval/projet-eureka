from backend.src.domain.Scorer import Scorer


class ScoringService:
    def __init__(self, scorer: Scorer = Scorer()):
        self.__scorer: Scorer = scorer

    def get_score(self, scoring_request: dict[str, list[tuple[float, float]] | int]) -> float:
        return self.__scorer.get_score(scoring_request["map_id"], scoring_request["path"])
