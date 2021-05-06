import config
from tweepy import OAuthHandler, Cursor, API


def authenticate():
    '''Function for handling Twitter Authentication. See config.py and docker-compose.yml for details.'''
    
    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth
    
'''
# Option 1: See tweets printed from the user’s timeline.
if __name__ == '__main__':
    auth = authenticate()
    api = API(auth)

    cursor = Cursor(
        api.user_timeline,
        id = 'mental_floss',
        tweet_mode = 'extended'
    )

    for status in cursor.items(2):
        tweet = {
            'text': status.full_text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count
        }
        print(tweet)
'''

# Option 2: Collect incoming tweets in real-time, using the Twitter Stream with Object Oriented Programming.

from tweepy import Stream
from tweepy.streaming import StreamListener
import json

class MaxTweetsListener(StreamListener):

    def __init__(self, max_tweets, *args, **kwargs):
        # initialize the StreamListener
        super().__init__(*args, **kwargs)
        # set the instance attributes
        self.max_tweets = max_tweets
        self.counter = 0
        
    def on_connect(self):
        print('connected. listening for incoming tweets')


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


    def on_error(self, status):
        if status == 420:
            print(f'Rate limit applies. Stop the stream.')
            return False


if __name__ == '__main__':
    auth = authenticate()
    listener = MaxTweetsListener(max_tweets=100)
    stream = Stream(auth, listener)
    stream.filter(track=['berlin'], languages=['en'], is_async=False)
