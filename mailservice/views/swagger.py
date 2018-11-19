import os

from flakon import SwaggerBlueprint
from flask import request
from mailservice.database import db, Report


swagger_spec = os.path.join(os.path.dirname(__file__), '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=swagger_spec)


@api.operation('setFrequency')
def set_frequency(runner_id):
    frequency = int(request.json)
    report = db.session.query(Report).filter(Report.runner_id == runner_id).first()
    report.set_frequency(frequency)
    db.session.merge(report)
    db.session.commit()
    return {'updated': 1}


@api.operation('getFrequency')
def get_frequency(runner_id):
    report = db.session.query(Report).filter(Report.runner_id == runner_id).first()
    return {'updated': report.frequency}
