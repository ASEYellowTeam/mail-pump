import os
import requests_mock
from flask import jsonify
from mailservice.tests.utility import client
from mailservice.mailpump import prepare_body


DATASERVICE = os.environ['DATA_SERVICE']


def test_prepare_body(client):
    tested_app, app = client

    with requests_mock.mock() as m:
        user = {
            "id": 1,
            "email": "test@example.com",
            "firstname": "Test",
            "lastname": "Tester",
            "age": 1,
            "max_hr": 1,
            "rest_hr": 1,
            "vo2max": 1,
            "weight": 1,
        }
        run = {
            "id": 16,
            "user_id": 1,
            "strava_id": 1936220842,
            "title": "Test Run",
            "distance": 50000.0,
            "description": None,
            "average_speed": 10.0,
            "elapsed_time": 5000.0,
            "total_elevation_gain": 3.0,
            "average_heartrate": None,
            "start_date": 1500000000.0,
        }
        m.get(DATASERVICE + '/runs?user_id=1', json=[run])
        assert prepare_body(user) == "name: Test Run\ndistance: 50000.0\nstart_date: 1500000000.0\n" \
            "average_speed: 10.0\nelapsed_time: 5000.0\naverage_heartrate: None\ntotal_elevation_gain: 3.0\n\n\n"


def test_mail_config(client):
    tested_app, app = client

    assert app.config['MAIL_SERVER'] == 'smtp.gmail.com'
    assert app.config['MAIL_PORT'] == 465
    assert app.config['MAIL_USERNAME'] == 'yt.beepbeep'
    assert app.config['MAIL_PASSWORD'] == 'TestYellowTeam7'
    assert app.config['MAIL_USE_TLS'] is False
    assert app.config['MAIL_USE_SSL'] is True
