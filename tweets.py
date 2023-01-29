import tweepy
import configparser
import pandas as pd
import json
import time

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
    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.columns = ['Tweet']
        self.data = []
    
    def on_data(self, data):
        json_data = json.loads(data)
        if '#' in json_data['data']['text']:
            self.data.append((json_data['data']['text']))

    def on_error(self, status):
        print(status)


printer = TweetPrinter(bearer_token)

rule = tweepy.StreamRule("has:hashtag")
printer.add_rules(rule)
printer.sample()
time.sleep(10) 
printer.disconnect()

df = pd.DataFrame(printer.data, columns=printer.columns)
df.to_csv('tweets.csv')
