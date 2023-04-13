import json
import pytest
from flask import Flask

from backend.src.resource.ScoringResource import ScoringResource

ANY_MAP_ID = 1
ANY_PATH = [[1.0, 1.0], [2.0, 2.0]]
ANY_SCORE_REQUEST = {
    "map_id": ANY_MAP_ID,
    "path": ANY_PATH
}
HTTP_OK = 200
HEALTH_OK_RESPONSE = {"health": 'OK'}


@pytest.fixture
def client():
    app = Flask(__name__)
    ScoringResource(app)
    app.config['TESTING'] = True
    with app.test_request_context():
        with app.test_client() as client:
            yield client


def test__when_get_health__then_OK_is_returned(client):
    response = client.get('http://localhost:5000/health')
    json_response = json.loads(response.data)
    assert response.status_code == HTTP_OK
    assert json_response == HEALTH_OK_RESPONSE


def test__given_any_request__when_post_score__then_float_score_is_returned(client):
    response = client.post('http://localhost:5000/score', json=ANY_SCORE_REQUEST)
    json_response = json.loads(response.data)
    assert response.status_code == HTTP_OK
    assert type(json_response['score']) == float
