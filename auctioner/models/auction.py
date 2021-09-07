import sqlite3
from db import db


class AuctionModel(db.Model):
    __tablename__ = 'auction'

    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.String(80))
    status = db.Column(db.String(80))

    def __init__(self, auction_id):
        self.auction_id = auction_id
        self.status = 'INPROGRESS'
        self.winner_url = ''
        self.winner_bid_id = ''
        self.winner_bid_amount = ''

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(auction_id=name).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()
