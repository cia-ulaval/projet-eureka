from flask import Flask
from flask_cors import CORS
from backend.src.resource.ScoringResource import ScoringResource
from backend.src.resource.MapResource import MapResource
from backend.src.service.MapService import MapService
from backend.src.service.ScoringService import ScoringService
from backend.src.domain.Map import Map
from backend.src.domain.Mission import Mission


def main():
    # Create the Flask app

    app = Flask(__name__)

    map: Map = Map()
    mission: Mission = Mission()
    map_service: MapService = MapService(map, mission)
    scoring_service: ScoringService = ScoringService(map, mission)

    # Create the API
    ScoringResource(app, scoring_service)
    MapResource(app, map_service)
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8080"}})

    app.run(debug=True)


if __name__ == '__main__':
    main()
