import requests
import os
from datetime import timedelta
from time import time
from celery import Celery
from celery.task import periodic_task
from flask_mail import Mail, Message
from .database import db, Report
from .app import app


BACKEND = BROKER = os.getenv('BROKER', 'redis://localhost:6379')
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

DATASERVICE=os.environ['DATA_SERVICE']


def send_all_mail():  # pragma: no cover
    print('Sending mails...')

    mail = Mail(app)
    mail.init_app(app=app)

    users = requests.get(DATASERVICE + '/users').json().users

    for user in users:
        # check if this user wants to receives mail
        report = db.session.query(Report).filter(Report.runner_id == user.id).first()
        if report is not None and time() - report.timestamp >= report.frequency:
            body = prepare_body(user)
            if body:  # can be None if there are no runs to be shown
                # send the mail
                print('Sending email to %s' % user.email)
                msg = Message('Your BeepBeep Report', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
                msg.body = body
                mail.send(msg)
                # update the latest report timestamp
                report.set_timestamp()
                db.session.merge(report)
                db.session.commit()
    print('All mails are sent')


def prepare_body(user):
    body = ""
    runs = requests.get(DATASERVICE + '/users/' + user.id).json()
    if len(runs) == 0:
        return None
    # TODO: should send only the new runs from the latest report, not all the runs.
    for run in runs:
        body += "name: " + run.name + "\ndistance: " + str(run.distance) + "\nstart_date: " + str(run.start_date) + \
                "\naverage_speed: " + str(run.average_speed) + "\nelapsed_time: " + str(run.elapsed_time) + \
                "\naverage_heartrate: " + str(run.average_heartrate) + "\ntotal_elevation_gain: " + \
                str(run.total_elevation_gain) + "\n\n\n"
    return body


@periodic_task(run_every=timedelta(seconds=60))
def periodic_send():
    send_all_mail()


if __name__ == '__main__':
    periodic_send()
