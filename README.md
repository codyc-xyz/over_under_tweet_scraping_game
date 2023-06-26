# Twitter Hashtag Analyzer
This Python program allows users to stream tweets from Twitter, analyze the frequency of hashtags in those tweets, and even play a 
game where they guess which of two hashtags has been tweeted more. The script uses the Tweepy library to interact with the Twitter 
API and the Pandas library to manage and analyze the data.

## Features
Stream Tweets: The program can stream tweets in real-time from Twitter using the Tweepy library and save them into a CSV file.

Analyze Hashtags: The script analyzes the tweets stored in the CSV file to count the frequency of different hashtags. It then sorts 
these hashtags by their frequency and saves the top 1000 hashtags to a separate CSV file.

Hashtag Guessing Game: Users can play a game where they guess which of two randomly selected hashtags was tweeted more. The game 
continues until the user makes an incorrect guess.

## Dependencies
To run this script, you will need Python 3 and the following libraries installed:

tweepy
configparser
pandas
json
random

## Setup
Before you can use this script, you will need to set up a Twitter Developer account and create an application to get your Twitter API 
keys. Once you have your keys, you need to add them to a configuration file named config.ini.

## Usage
To run the script, use the following command:

python twitter_hashtag_analyzer.py

Once the script is running, it will prompt you to choose an option:

Enter 'G' to play the game
Enter 'S' to stream tweets
Enter 'A' to analyze tweets
Enter 'V' to view the top 1000 hashtags
