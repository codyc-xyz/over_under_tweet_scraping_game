import tweepy
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
bearer_token = config['twitter']['bearer_token']

auth = tweepy.OAuth2AppHandler(api_key, api_key_secret)
api = tweepy.API(auth)

class Listener(tweepy.StreamingClient):

  tweets = []
  limit = 10
  def on_status(self, status):
    while limit > 0:
      print(status.text)
      limit -= 1

stream_tweet = Listener(api_key, api_key_secret, access_token, access_token_secret)

keywords = ['2022']
stream_tweet.filter(track=keywords)