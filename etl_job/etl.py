import pymongo
import time
from sqlalchemy import create_engine
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

# analyzser for sentiment analysis:
s = SentimentIntensityAnalyzer()

# mongodb connection: 
time.sleep(10)

client = pymongo.MongoClient(host='mongodb')
db = client.tweets
collection = db.tweet_data

logging.info('mongodb client set')

# postgresdb connection: 
time.sleep(5)

pg = create_engine('postgres://postgres:postgres@postgresdb:5432/twitterdb', echo=False)

logging.info('postgresdb engine set')

# create dataframe of list of tweets (pandas):
def create_df(collection):

    df = pd.DataFrame(list(collection.find()))
    del df['_id']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    logging.warning('data frame created')
    return df

# analyze sentiments and append sentiment compound scores to dataframe column 'sentiment':
def sentiments_to_df(df):

    result = []

    for tweet in df['text'].replace('@',''):
        
        score = s.polarity_scores(tweet)
        result.append(str(score['compound']))

    df["sentiment"] = result
    logging.warning('sentiment compound score appended to df: {}'.format(score['compound']))
    return df

#transform dataframe to postgres table: 
def df_to_sql(df):

    df.to_sql('tweets', pg, if_exists='replace')
    logging.warning('table created')

# function running the above functions with constrainted repetition:
def main_code(): 

    #repeat times =
    times_to_repeat = 3               

    while times_to_repeat >= 0:

        df = create_df(collection)

        df = sentiments_to_df(df)

        df_to_sql(df)

        times_to_repeat -= 1

        logging.critical('times to repeat left = {}'.format(times_to_repeat))

        time.sleep(60) 
        
    client.drop_database('tweets')

time.sleep(10)
main_code()




