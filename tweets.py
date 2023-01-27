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

client = tweepy.Client(bearer_token)
auth = tweepy.OAuth2AppHandler(api_key, api_key_secret)
api = tweepy.API(auth)

response = client.search_recent_tweets("Tweepy")

print(response.meta)

tweets = response.data

for tweet in tweets:
    print(tweet.id)
    print(tweet.text)

response = client.search_recent_tweets('tweepy')