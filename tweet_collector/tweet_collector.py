import config
from tweepy import OAuthHandler, Cursor, API, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pymongo
import time
from datetime import datetime

def authenticate():
    '''Function for handling Twitter Authentication. See config.py and docker-compose.yml for details.'''
    
    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

# Collect incoming tweets in real-time, using the Twitter Stream with Object Oriented Programming.

class MaxTweetsListener(StreamListener):

    def __init__(self, max_tweets, *args, **kwargs):
        # initialize the StreamListener
        super().__init__(*args, **kwargs)
        # set the instance attributes
        self.max_tweets = max_tweets
        self.counter = 0
        
    def on_connect(self):
        print('connected. listening for incoming tweets. streamer start.')

    '''
    def on_status(self, status):
        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""
        
        # increase the counter
        self.counter += 1        

        tweet = {
            'text': status.text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count
        }

        print(f'New tweet arrived: {tweet["text"]}')

        # check if we have enough tweets collected
        if self.max_tweets == self.counter:
            # reset the counter
            self.counter=0
            # return False to stop the listener
            return False
    '''

    def on_data(self, data):
        """Whatever we put in this method defines what is done with every single tweet as it is intercepted in real-time"""

        # Create a connection to the MongoDB database server
        client = pymongo.MongoClient(host='mongodb') # hostname = servicename for docker-compose pipeline

        # Create/use a database
        db = client.tweets #equivalent of CREATE DATABASE tweets;

        # Define the collection
        collection = db.tweet_data #equivalent of CREATE TABLE tweet_data;

        t = json.loads(data) #t is just a regular python dictionary.

        tweet = {
        'username': t['user']['screen_name'],
        'text': t['text'],
        'timestamp': t['created_at']
        }

        # What we actually want to do is to insert the tweet into MongoDB
        # Insert the tweet into the collection

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')
        logging.critical('-----Tweet written into MongoDB-----')
        collection.insert_one(tweet) #equivalent of INSERT INTO tweet_data VALUES (....);
        logging.critical(str(datetime.now()))
        logging.critical('----------\n')

        time.sleep(3)

    def on_error(self, status):
        if status == 420:
            print(f'Rate limit applies. Stop the stream.')
            return False


if __name__ == '__main__':

    times_to_repeat = 3

    while times_to_repeat >= 0:

        auth = authenticate()
        listener = MaxTweetsListener(max_tweets=5)
        stream = Stream(auth, listener)
        stream.filter(track=['Berlin'], languages=['en'], is_async=False)

        times_to_repeat -= 1  
        time.sleep(30)

logging.critical('streamer shutdown')        