from mailservice.tests.utility import client
from flask import json

def test_get_frequency(client):
    tested_app, app = client

    # Test get frequency on a non existing user
    reply = tested_app.get('/frequency/1')
    assert reply.status_code == 404


def test_set_frequency(client):
    tested_app, app = client

    # Set the frequency without the frequency parameter
    reply = tested_app.post('/frequency/1')
    assert reply.status_code == 400
    reply = tested_app.post('/frequency/1', json={})
    assert reply.status_code == 400

    # Set the frequency
    test_frequency = 3.0
    reply = tested_app.post('/frequency/1', json={'frequency': test_frequency})
    assert reply.status_code == 200

    # Test get frequency on the frequency set before
    reply = tested_app.get('/frequency/1')
    frequency = float(reply.get_json()['frequency'])
    assert reply.status_code == 200
    assert frequency == test_frequency
