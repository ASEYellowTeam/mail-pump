import os
import requests_mock
from mailservice.mailpump import prepare_body
from mailservice.tests.utility import client


DATASERVICE = os.environ['DATA_SERVICE']


def test_prepare_body(client):
    tested_app, app = client

    with requests_mock.mock() as m:
        user1 = {
            "id": 1,
            "email": "test1@example.com",
            "firstname": "Test1",
            "lastname": "Tester",
            "age": 1,
            "max_hr": 1,
            "rest_hr": 1,
            "vo2max": 1,
            "weight": 1,
        }
        user2 = {
            "id": 2,
            "email": "test2@example.com",
            "firstname": "Test1",
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

        # Test the prepare body
        m.get(DATASERVICE + '/runs?user_id=1', json=[run])
        assert prepare_body(user1) == "name: Test Run\ndistance: 50000.0\nstart_date: 1500000000.0\n" \
            "average_speed: 10.0\nelapsed_time: 5000.0\naverage_heartrate: None\ntotal_elevation_gain: 3.0\n\n\n"

        # Test the prepare body with a non existing user
        m.get(DATASERVICE + '/runs?user_id=2', json=[])
        assert prepare_body(user2) is None


def test_mail_config(client):
    tested_app, app = client

    assert app.config['MAIL_SERVER'] == 'smtp.gmail.com'
    assert app.config['MAIL_PORT'] == 465
    assert app.config['MAIL_USERNAME'] == 'yt.beepbeep'
    assert app.config['MAIL_PASSWORD'] == 'TestYellowTeam7'
    assert app.config['MAIL_USE_TLS'] is False
    assert app.config['MAIL_USE_SSL'] is True
