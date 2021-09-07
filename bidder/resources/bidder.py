import os
import random
import time
import uuid

from flask_restful import Resource

bidder_id = uuid.uuid4()


class Bidder(Resource):

    def post(self):
        delay_time = os.environ.get('DELAY')
        time.sleep(int(delay_time)/1000)
        return {'bid': random.randint(100, 1000), 'bidder_id': str(bidder_id)}
