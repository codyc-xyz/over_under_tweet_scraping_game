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
  def __init__(self):
      self.columns = ['Time', 'Tweet']
      self.data = []
  
  def on_tweet(self, tweet):
      self.data.append(tweet.created_at, tweet.text)

  def on_error(self, status):
      print(status)

printer = TweetPrinter(bearer_token)
printer.sample()

df = pd.DataFrame(printer.data, columns=printer.columns)
df.to_csv('tweets.csv')
