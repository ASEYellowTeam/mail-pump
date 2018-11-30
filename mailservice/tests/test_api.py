from mailservice.tests.utility import client, new_report
from mailservice.database import db, Report


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

    # Update the frequency
    test_frequency = 4.0
    reply = tested_app.post('/frequency/1', json={'frequency': test_frequency})
    assert reply.status_code == 200

    # Test get frequency on the frequency updated before
    reply = tested_app.get('/frequency/1')
    frequency = float(reply.get_json()['frequency'])
    assert reply.status_code == 200
    assert frequency == test_frequency


def test_delete_all_report_by_user(client):
    tested_app, app = client

    # Add a new report in database
    report = new_report()
    with app.app_context():
        db.session.add(report)
        db.session.commit()
        report = db.session.query(Report).first()

    with app.app_context():
        assert db.session.query(Report).filter(Report.user_id == report.user_id).count() == 1

    # Delete all report by the user
    assert tested_app.delete('/reports?user_id='+str(report.user_id)).status_code == 200
    with app.app_context():
        assert db.session.query(Report).filter(Report.user_id == report.user_id).count() == 0

    # Cannot delete them again
    assert tested_app.delete('/reports?user_id='+str(report.user_id)).status_code == 404

    # Non existing user
    assert tested_app.delete('/reports?user_id=-1').status_code == 404

    # Without passing the user_id
    assert tested_app.delete('/reports').status_code == 400
