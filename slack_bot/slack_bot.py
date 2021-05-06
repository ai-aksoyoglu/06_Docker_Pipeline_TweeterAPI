import requests
import config
from sqlalchemy import create_engine
import time
import pandas as pd
import logging

# logging criteria:
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S') # filename='debug.log',

# webhook for slackbot:
webhook_url = config.webhook_url  

#postgresdb connection:
time.sleep(5)

# create enginge: 
pg = create_engine('postgres://postgres:postgres@postgresdb:5432/twitterdb', echo=False)

# query for getting the latest entry to postgres db from columns text and sentiment: 
query = """
	SELECT DISTINCT ON (text) text, sentiment
	FROM tweets
	WHERE CTID = (SELECT MAX(CTID) FROM tweets)
	ORDER BY text, sentiment DESC
	"""
	
time.sleep(20)

# while loop to constantly run slackbot, displaying query in two text blocks:
while True: 

	# reading query and write to variable with pandas:
	tweet = pd.read_sql_query(query, con=pg)
	logging.warning('query variable set, query =  \n {}'.format(tweet))

	# get value of text and sentiment
	text_tweet = tweet['text'].iloc[0]

	sentiment_tweet =  tweet['sentiment'].iloc[0]

	data = {
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": text_tweet
				}
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": ("sentiment compound score = " + sentiment_tweet)
				}
			}
		]
	}
	
	requests.post(url=webhook_url, json = data)

	logging.critical('tweet displayed via slackbot')

	time.sleep(120)         # timer