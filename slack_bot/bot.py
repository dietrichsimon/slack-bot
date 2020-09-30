import logging
import sqlalchemy as db
import pandas as pd
from slack import WebClient
import config

# establish connection to postgres database
try:
    engine = db.create_engine("postgres://postgres:1234@postgresdb:5432")
except:
    logging.critical('Could not establish connection to postgres database.')

initialize connection with slack
client = WebClient(token=config.ACCESS_TOKEN_SLACK)

# select most recent tweet from database
query = f"""SELECT * FROM tweets;"""
df = pd.read_sql(query, engine)
tweet = str(df['tweet'].tail(1))

# post tweet on Slack
response = client.chat_postMessage(
    channel="#bot_playground",
    text=f"Time for a tweet: {tweet}")
