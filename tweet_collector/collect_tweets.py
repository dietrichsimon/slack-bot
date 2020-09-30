'''
This script downloads tweets from twitter that contain certain specified keywords.
'''

import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pymongo

conn = 'mongodb'
client = pymongo.MongoClient(conn)
db = client.tweets
collection = db.tweetcollection

def authenticate():
    """Function for handling Twitter Authentication"""
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) 

        text = t['''text'''].replace("'", " ")
        if 'extended_tweet' in t:
            text = t['extended_tweet']['full_text'].replace("'", " ")
        if 'retweeted_status' in t:
            r = t['retweeted_status']
            if 'extended_tweet' in r:
                text =  r['extended_tweet']['full_text'].replace("'", " ")
        tweet = {
        'text':text,
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }
        collection.insert_one(tweet)
        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')

    def on_error(self, status):

        if status == 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['berlin'], languages=['en'])
