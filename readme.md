# auctioning system
## DOCKER
* New containers can be duplicated with bidder resource and delay to the bid response in millisec to be customized at "DELAY" in 
  docker-compose.yml
## REST CALLS
* List of Bidders:
    * GET http://127.0.0.1:5000/bidderslist
* List of auction:
    * POST http://127.0.0.1:5000/auction
        * With JSON {"auction_id": "123"}