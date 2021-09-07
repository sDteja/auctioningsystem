FROM python:3.7
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV FLASK_ENV="docker"
ENV AUCTION_URL="http://auctioner:5000/register"
