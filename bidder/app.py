import os
import time

import requests
from flask import Flask
from flask_restful import Api

from resources.bidder import Bidder


def custom_call():
    auction_url = os.environ.get('AUCTION_URL', 'http://localhost:5000/register')
    try:
        print('trying to register {}'.format(auction_url))
        s = requests.Session()
        config_dict = {'endpoint': '/bid'}
        r = s.post(f'{auction_url}', data=config_dict)
    except:
        print("Exiting due to connection failure")


class MyFlaskApp(Flask):
    def run(self, *args, **kwargs):
        custom_call()
        super(MyFlaskApp, self).run(*args, **kwargs)


app = MyFlaskApp('__name__')
app.secret_key = 'test'
api = Api(app)

api.add_resource(Bidder, "/bid")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
