import json

from flask import Flask, jsonify, request

from backend.src.service.ScoringService import ScoringService


class ScoringResource:
    def __init__(self, app: Flask, scoring_service: ScoringService):
        self.__app = app
        self.__register_routes()

        self.__scoring_service = scoring_service

    def __register_routes(self):
        @self.__app.route("/health", methods=["GET"])
        def health():
            return jsonify({"health": "OK"})

        @self.__app.route("/score", methods=["POST"])
        def get_score():
            score_request = request.get_json()
            human_path: list[(int, int)] = score_request["path"]
            co2_total, wait_total = self.__scoring_service.get_score(human_path)
            ai_co2_total, ai_wait_total, ai_path = self.__scoring_service.get_ai_score()

            return jsonify(
                {"human_stats": {"co2": co2_total, "wait": wait_total},
                 "AI_path": ai_path,
                 "AI_stats": {"co2": ai_co2_total, "wait": ai_wait_total}})
