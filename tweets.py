import tweepy
import configparser
import pandas as pd
import json
import random

# Function to read Twitter API keys from a configuration file
def read_config(config_file):
    # Initializes a config parser
    config = configparser.ConfigParser()
    # Reads the configuration file
    config.read(config_file)
    # Returns a dictionary containing the Twitter API keys
    return {
        'api_key': config['twitter']['api_key'],
        'api_key_secret': config['twitter']['api_key_secret'],
        'access_token': config['twitter']['access_token'],
        'access_token_secret': config['twitter']['access_token_secret'],
        'bearer_token': config['twitter']['bearer_token']
    }

# Function to stream tweets using Tweepy and save them to a CSV file
def stream_tweets(bearer_token):
    # Defining a class to handle the streaming of tweets
    class TweetPrinter(tweepy.StreamingClient):
        # Initializes the streaming client
        def __init__(self, bearer_token):
            super().__init__(bearer_token)
            # Defines the columns for the DataFrame to be saved
            self.columns = ['Tweet']
            # Initializes an empty list to store the streamed tweets
            self.data = []

        # Method to handle new data from the stream
        def on_data(self, data):
            # Parses the data as JSON
            json_data = json.loads(data)
            # Checks if the tweet contains a hashtag and if so, adds it to the data list
            if '#' in json_data['data']['text']:
                self.data.append((json_data['data']['text']))

        # Method to handle stream errors
        def on_error(self, status):
            # Prints the error status
            print(status)        

        # Method to handle disconnection from the stream
        def on_disconnect(self):
            # Converts the data list to a DataFrame and saves it to a CSV file
            df = pd.DataFrame(self.data, columns=self.columns)
            df.to_csv('tweets.csv', index=False)
            return super().on_disconnect()

    # Initializes and starts the streaming client
    printer = TweetPrinter(bearer_token)
    printer.sample()

# Function to analyze the hashtags in the streamed tweets
def analyze_tweets(file):
    # Loads the tweets from the CSV file into a DataFrame
    df = pd.read_csv(file)
    # Initializes an empty list to store the hashtags
    hashtags = []
    # Loops over each tweet and extracts the hashtags
    for tweet in df['Tweet']:
        hashtags_in_tweet = [i for i in tweet.split() if i.startswith('#')]
        hashtags.extend(hashtags_in_tweet)

    # Counts the frequency of each hashtag
    hashtag_counts = pd.Series(hashtags).value_counts()
    # Sorts the hashtags by their count in descending order
    sorted_hashtags = hashtag_counts.sort_values(ascending=False)
    # Returns the top 1000 hashtags
    top_1000_hashtags = sorted_hashtags[:1000]
    return top_1000_hashtags

# Function to play a game where the user guesses which hashtag was tweeted more
def select_answer(df, hashtag1, hashtag2):
    # Prompts the user to guess which hashtag was tweeted more
    print(f"Which of the following hashtags was tweeted more: {hashtag1} or {hashtag2}? Input '1', or '2 to select your answer.")
    user_choice = input()
    # Gets the count of the first hashtag
    count1 = df[df['Hashtag'] == hashtag1]['Count'].values[0]
    # Gets the count of the second hashtag
    count2 = df[df['Hashtag'] == hashtag2]['Count'].values[0]
    # Checks if the user guessed the first hashtag and if it was tweeted more
    if user_choice == '1':
        if count1 > count2:
            print("Correct!")
            return True
        else:
            print(f"Incorrect. {hashtag2} was tweeted more ({count2} vs {count1}).")
            return False
    # Checks if the user guessed the second hashtag and if it was tweeted more
    elif user_choice == '2':
        if count2 > count1:
            print("Correct!")
            return True
        else:
            print(f"Incorrect. {hashtag1} was tweeted more ({count1} vs {count2}).")
            return False
    else:
         # If the user input is invalid, it prompts the user to try again
         print("Invalid option. Try again.")
         select_answer(df, hashtag1, hashtag2)


# Main function to interact with the user
def main():
    # Prompts the user for their choice of operation
    choice = input("Enter 'G' to play the game, 'S' to stream tweets, 'A' to analyze tweets, or 'V' to view top 1000 hashtags: ")
    # If the user chooses to stream tweets
    if choice == 'S' or choice == 's':
        # Reads the Twitter API keys from the configuration file
        config = read_config('config.ini')
        # Streams tweets
        stream_tweets(config['bearer_token'])
    # If the user chooses to analyze tweets
    elif choice == 'A' or choice == 'a':
        # Analyzes the tweets and gets the top 1000 hashtags
        top_1000_hashtags = analyze_tweets('tweets.csv')
        # Saves the top 1000 hashtags to a CSV file
        df = pd.DataFrame({'Hashtag': top_1000_hashtags.index, 'Count': top_1000_hashtags.values})
        df.to_csv('top_1000_hashtags.csv', index=False)
    # If the user chooses to view the top 1000 hashtags
    elif choice == 'V' or choice == 'v':
        # Loads the top 1000 hashtags from the CSV file and prints them
        df = pd.read_csv('top_1000_hashtags.csv')
        print(df)
    # If the user chooses to play the game
    elif choice == 'G' or choice == 'g':
        # Loads the top 1000 hashtags from the CSV file
        df = pd.read_csv('top_1000_hashtags.csv')
        # Initializes an empty set to store the used hashtags
        used_hashtags = set()  
        # Initializes the user's score
        score = 0
        # Loops until all hashtags have been used
        while True:
            # Gets the hashtags that have not been used yet
            available_hashtags = set(df['Hashtag']) - used_hashtags
            # If all hashtags have been used, ends the game and prints the user's score
            if not available_hashtags:
                print(f"You have used all the hashtags. Your score is {score}")
                break
            # Randomly selects two hashtags for the user to guess between
            hashtag1, hashtag2 = random.sample(list(available_hashtags), 2)
            # Adds the selected hashtags to the set of used hashtags
            used_hashtags.update({hashtag1, hashtag2})
            # Asks the user to guess which hashtag was tweeted more
            if select_answer(df, hashtag1, hashtag2):
                # If```python
                # the user's guess is correct, their score is incremented
                score += 1
            else:
                # If the user's guess is incorrect, the game ends
                break
        # Prints the user's final score
        print(f"Thanks for playing! Your final score is {score}")
    else:
        # If the user input is invalid, it prompts the user to try again
        print("Invalid option. Try again.")
        main()

# Calls the main function to start the program
main()
