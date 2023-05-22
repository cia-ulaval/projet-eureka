import json
from flask import Flask, jsonify, request
from backend.src.service.MapService import MapService


class MapResource:
    def __init__(self, app: Flask, mapping_service: MapService):
        self.__app = app
        self.__register_routes()

        self.__mapping_service = mapping_service

    def __register_routes(self):
        @self.__app.route("/map", methods=["GET"])
        def get_map():
            start, end = self.__mapping_service.get_start_and_end()
            traffic: list[list[float]] = self.__mapping_service.get_traffic()
            return jsonify({"start": start, "end": end, "traffic": traffic})
