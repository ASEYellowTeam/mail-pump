from time import time
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    runner_id = db.Column(db.Integer)
    timestamp = db.Column(db.Float)
    frequency = db.Column(db.Float)

    def set_user(self, id_usr):
        self.runner_id = id_usr

    # timestamp from previous report, in seconds
    def set_timestamp(self):
        self.timestamp = time()

    # frequency preference stored in seconds
    def set_frequency(self, choice):
        self.frequency = (float(choice)*3600.0)

    def to_json(self):
        res = {}
        for attr in ('id', 'runner_id', 'timestamp', 'frequency'):
            res[attr] = getattr(self, attr)
        return res
