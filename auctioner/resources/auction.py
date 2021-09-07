import asyncio
import json
import traceback

import aiohttp
import async_timeout
from flask_restful import Resource, reqparse

from models.auction import AuctionModel
from models.register import RegisterModel


class Wrapper:

    def __init__(self, session):
        self._session = session

    async def auction_to_bidders(self, bidder_url):
        try:
            async with self._session() as client_session, async_timeout.timeout(200/1000):
                async with client_session.post(bidder_url) as response:
                    return await response.text()
        except Exception as e:
            print('Timedout for url {}'.format(bidder_url))


class Auction(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('auction_id', type=str, required=True, help='Mandatory field')

    def post(self):
        request_data = Auction.parser.parse_args()
        auction_id = request_data['auction_id']
        auction = AuctionModel.find_by_name(auction_id)
        if auction and auction.status == 'INPROGRESS':
            return {'message': 'Auction In Progress'}, 400
        auction = AuctionModel(auction_id)
        auction.save_to_db()
        try:
            auction.save_to_db()
            result = RegisterModel.find_all()
            if result is not None:
                bidders = [bidder.json() for bidder in result]
                urls = [bidder_detail['bidder'] + bidder_detail['endpoint'] for bidder_detail in bidders]
                urls = list(set(urls))
                from functools import partial
                wrapper = Wrapper(aiohttp.ClientSession)
                auctions_calls = [partial(wrapper.auction_to_bidders, url) for url in urls]
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                responses = loop.run_until_complete(asyncio.gather(*[func() for func in auctions_calls]))
                mapping_response = dict(zip(urls, responses))
                auction.winner_bid_amount = float('-inf')
                for endpoint, data in mapping_response.items():
                    try:
                        response = json.loads(data)
                        bid_amt = float(response['bid'])
                        if bid_amt > auction.winner_bid_amount:
                            auction.winner_bid_amount = bid_amt
                            auction.winner_url = endpoint
                            auction.winner_bid_id = response['bidder_id']
                    except:
                        pass
                auction.status = 'COMPLETED'
                auction.save_to_db()
                return {'bidder_id': auction.winner_bid_id, 'bid_value': auction.winner_bid_amount}
            else:
                auction.status = 'COMPLETED'
                auction.save_to_db()
                return {'message': 'No registered end points'}, 400
        except:
            print(traceback.format_exc())
            auction.status = 'COMPLETED'
            auction.save_to_db()
            return {'message': 'An error occurred'}, 500
