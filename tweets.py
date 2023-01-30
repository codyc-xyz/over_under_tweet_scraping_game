import tweepy
import configparser
import pandas as pd
import json

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        'api_key': config['twitter']['api_key'],
        'api_key_secret': config['twitter']['api_key_secret'],
        'access_token': config['twitter']['access_token'],
        'access_token_secret': config['twitter']['access_token_secret'],
        'bearer_token': config['twitter']['bearer_token']
    }

def stream_tweets(bearer_token):
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

        def on_disconnect(self):
            df = pd.DataFrame(self.data, columns=self.columns)
            df.to_csv('tweets.csv', index=False)
            return super().on_disconnect()

    printer = TweetPrinter(bearer_token)
    printer.sample()

def analyze_tweets(file):
    df = pd.read_csv(file)
    hashtags = []
    for tweet in df['Tweet']:
        hashtags_in_tweet = [i for i in tweet.split() if i.startswith('#')]
        hashtags.extend(hashtags_in_tweet)

    hashtag_counts = pd.Series(hashtags).value_counts()
    sorted_hashtags = hashtag_counts.sort_values(ascending=False)
    top_1000_hashtags = sorted_hashtags[:1000]
    return top_1000_hashtags


def main():
    
    choice = input("Enter 'S' to stream tweets, 'A' to analyze tweets, or 'V' to view top 1000 hashtags: ")
    if choice == 'S' or choice == 's':
        config = read_config('config.ini')
        stream_tweets(config['bearer_token'])
    elif choice == 'A' or choice == 'a':
        top_1000_hashtags = analyze_tweets('tweets.csv')
        df = pd.DataFrame(top_1000_hashtags, columns=['Hashtag'])
        df.to_csv('top_1000_hashtags.csv')
    elif choice == 'V' or choice == 'v':
        df = pd.read_csv('top_1000_hashtags.csv')
        for hashtag in df['Hashtag']:
            print(hashtag)
    else:
        print("Invalid option. Try again.")
main()