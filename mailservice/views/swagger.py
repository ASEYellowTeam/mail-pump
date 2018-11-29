import os
import json
from time import time
from flask import request, jsonify, make_response, abort
from flakon import SwaggerBlueprint
from mailservice.database import db, Report


swagger_spec = os.path.join(os.path.dirname(__file__), '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=swagger_spec)


@api.operation('setFrequency')
def set_frequency(user_id):
    if not request.get_json() or not request.get_json()['frequency']:
        abort(400)

    frequency = float(request.get_json()['frequency'])

    report = db.session.query(Report).filter(Report.user_id == user_id).first()
    if not report:
        report = Report()
        report.user_id = user_id
        report.timestamp = time()

    report.set_frequency(frequency)
    db.session.merge(report)
    db.session.commit()

    return jsonify(1)


@api.operation('getFrequency')
def get_frequency(user_id):
    report = db.session.query(Report).filter(Report.user_id == user_id).first()
    if not report:
        abort(404)
    return jsonify({'frequency': report.get_frequency()})


@api.operation('deleteFrequency')
def delete_frequency():
    user_id = request.args.get('user_id')
    if not user_id:
        abort(400)
    reports = db.session.query(Report).filter(Report.user_id == user_id).all()
    if not reports:
        return abort(404)

    for rep in reports:
        db.session.delete(rep)
    db.session.commit()
    return make_response('OK')