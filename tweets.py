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

streaming_client = tweepy.StreamingClient(bearer_token)
auth = tweepy.OAuth2AppHandler(api_key, api_key_secret)
api = tweepy.API(auth)

class TweetPrinter(tweepy.StreamingClient):
  columns = ['Time', 'Tweet']
  data = []
  
  def on_tweet(self, tweet):
    self.data.append(tweet.created_at, tweet.text)
  df = pd.DataFrame(data, columns=columns)
  df.to_csv('tweets.csv')

printer = TweetPrinter(bearer_token)
printer.sample()
