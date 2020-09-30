import time
import pymongo
from sqlalchemy import create_engine
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

conn = 'mongodb'
client = pymongo.MongoClient(conn)
db = client.tweets
collection = db.tweetcollection

engine = None
while not engine:
    try:
        engine = create_engine("postgres://postgres:1234@postgresdb:5432")
    except:
        continue

engine.execute('''CREATE TABLE IF NOT EXISTS tweets (
    username TEXT,
    tweet TEXT,
    address TEXT
);
''')

def extract():
    tweets = collection.find().sort("_id", pymongo.DESCENDING).limit(1)
    if tweets:
        return tweets[0]
    return ""

sa = SentimentIntensityAnalyzer()

def transform(text):
    score = sa.polarity_scores(text)['compound']
    return score

def load(tweet, score):
    engine.execute(f"""INSERT INTO tweets VALUES ('{tweet["username"]}', '{tweet["text"]}', '{score}');""")

while True:
    tweet = extract()
    score = transform(tweet["text"])
    load(tweet,score)
    logging.critical('\n\nTRANSFORMED TWEET LOADED!')
    logging.critical(tweet,score)

    time.sleep(10)
