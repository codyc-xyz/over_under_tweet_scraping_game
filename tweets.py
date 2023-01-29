import tweepy
import configparser
import pandas as pd
import json

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
        self.columns = ['Time', 'Tweet']
        self.data = []
    
    def on_data(self, data):
        json_data = json.loads(data)
        self.data.append((json_data['created_at'], json_data['text']))

    def on_error(self, status):
        print(status)


printer = TweetPrinter(bearer_token)
printer.add_rules(tweepy.StreamRule('#'))
printer.filter()
time.sleep(5) 
printer.disconnect()

df = pd.DataFrame(printer.data, columns=printer.columns)
df.to_csv('tweets.csv')
