import os
from flask import Flask, jsonify
from flask_restful import Api

from resources.auction import Auction
from resources.register import Register, RegisterList
from db import db

app = Flask('__name__')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'test'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()



api.add_resource(Register, "/register")
api.add_resource(RegisterList, '/bidderslist')
api.add_resource(Auction, '/auction')

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0', debug=True)
