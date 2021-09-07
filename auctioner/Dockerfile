FROM python:3.7
RUN apt-get update
RUN mkdir /auctionapp
WORKDIR /auctionapp
COPY . /auctionapp
RUN pip install -r requirements.txt
ENV FLASK_ENV="auctionappdocker"
