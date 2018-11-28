from time import time
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.Float)
    frequency = db.Column(db.Float)

    def set_user(self, user_id):
        self.user_id = user_id

    # timestamp from previous report, in seconds
    def set_timestamp(self):
        self.timestamp = time()

    # frequency preference stored in seconds
    def set_frequency(self, choice):
        self.frequency = (float(choice)*3600.0)

    # frequency preference stored in seconds
    def get_frequency(self,):
        return self.frequency/3600.0
