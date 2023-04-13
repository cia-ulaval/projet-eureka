import json

from flask import Flask, jsonify, request

from backend.src.service.ScoringService import ScoringService


class ScoringResource:
    def __init__(self, app: Flask, scoring_service: ScoringService = ScoringService()):
        self.__app = app
        self.__register_routes()

        self.__scoring_service = scoring_service

    def __register_routes(self):
        @self.__app.route("/health", methods=["GET"])
        def health():
            return jsonify({"health": "OK"})

        @self.__app.route("/score", methods=["POST"])
        def get_score():
            score_request = json.loads(request.data)
            score = self.__scoring_service.get_score(score_request)
            return jsonify({"score": score})







