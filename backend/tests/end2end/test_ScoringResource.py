import json
import unittest
import requests

ANY_MAP_ID = 1
ANY_PATH = [[1.0, 1.0], [2.0, 2.0]]
ANY_SCORE_REQUEST = {
    "map_id": ANY_MAP_ID,
    "path": ANY_PATH
}
HTTP_OK = 200
HEALTH_OK_RESPONSE = {"health": 'OK'}

class TestScoringResource(unittest.TestCase):
    def test__when_get_health__then_return_OK(self):
        response = requests.get('http://localhost:5000/health')
        actual_response = json.loads(response.text)
        self.assertEqual(HTTP_OK, response.status_code)
        self.assertEqual(HEALTH_OK_RESPONSE, actual_response)

    def test__when_get_score__then_return_score(self):
        response = requests.post('http://localhost:5000/score', json=ANY_SCORE_REQUEST)
        print(response.text)
        json_data = json.loads(response.text)
        self.assertEqual(HTTP_OK, response.status_code)
        self.assertTrue("score" in json_data)
        self.assertTrue(type(json_data["score"]) is float)

