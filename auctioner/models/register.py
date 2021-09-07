import sqlite3
from db import db


class RegisterModel(db.Model):
    __tablename__ = 'register'

    id = db.Column(db.Integer, primary_key=True)
    bidder = db.Column(db.String(80))
    bidder_end_point = db.Column(db.String(80))

    def __init__(self, bidder, end_point):
        self.bidder = bidder
        self.bidder_end_point = end_point

    def json(self):
        return {'id': self.id, 'bidder': self.bidder, 'endpoint': self.bidder_end_point}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, bidder):
        return cls.query.filter_by(bidder=bidder).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()
