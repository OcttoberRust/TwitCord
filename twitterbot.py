import tweepy
import os

consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_KEY_SECRET")

access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

"""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
"""
tclient = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

