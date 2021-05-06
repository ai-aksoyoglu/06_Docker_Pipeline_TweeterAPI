Build a Dockerized Data Pipeline that analyzes the sentiment of tweets.

<img src="structure.svg">

In this project, you will build a data pippeline that collect tweets and stores them in a database. Next, the sentiment of tweets is analyzed and the annotated tweets are stored in a second database. Finally, the best or worst sentiment for a given is published on Slack every 10 minutes.

Challenges:

Install Docker

Build a data pipeline with docker-compose

Collect Tweets

Store Tweets in Mongo DB

Create an ETL job transporting data from MongoDB to PostgreSQL

Run sentiment analysis on the tweets

Build a Slack bot that publishes selected tweets

Upload your code to GitHub

This is a Data Engineering project. We could get the same done with less machinery, but this is a good opportunity to learn Docker and ETL.
