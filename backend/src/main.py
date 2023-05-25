from flask import Flask, jsonify
from flask_cors import CORS
from backend.src.resource.ScoringResource import ScoringResource
from backend.src.resource.MapResource import MapResource
from backend.src.service.MapService import MapService
from backend.src.service.ScoringService import ScoringService
from backend.src.domain.Map import Map
from backend.src.domain.Mission import Mission

app = Flask(__name__)

map: Map = Map()
mission: Mission = Mission()
map_service: MapService = MapService(map, mission)
scoring_service: ScoringService = ScoringService(map, mission)

# Create the API
ScoringResource(app, scoring_service)
MapResource(app, map_service)
CORS(app, resources={r"/*": {"origins": "*"}})

#     app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
