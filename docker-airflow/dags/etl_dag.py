"""
ETL DAG
"""
##### 1. Import modules #####
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import time
import pymongo
from sqlalchemy import create_engine
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import config

##### 2. Define default arguments #####
default_args = {
    "owner": "airflow",
    # depends_on_past determines whether we run a DAG if a past DAG has failed
    "depends_on_past": False,
    "start_date": datetime(2020, 4, 6),
    "email": [config.EMAIL],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

##### 3. Instantiate DAG #####
dag = DAG("etl", default_args=default_args, schedule_interval=timedelta(minutes=1))

##### 4. Create Tasks #####
# Establish connection to mongo #db
conn = 'mongodb'
client = pymongo.MongoClient(conn)
db = client.tweets
collection = db.tweetcollection

# Define the extract function
def extract():
    tweets = collection.find().sort("_id", pymongo.DESCENDING).limit(5)
    logging.critical('\n\nTWEET EXTRACTED!')
    if tweets:
        return tweets[0]
    return ""

# instantiate analyzer
sa = SentimentIntensityAnalyzer()

def transform(**context):
    extract_connection = context['task_instance']
    tweet = extract_connection.xcom_pull(task_ids="extract")
    tweet['score'] = sa.polarity_scores(tweet['text'])['compound']
    return tweet

# Establish connection to Postgres
engine = None
while not engine:
    try:
        engine = create_engine("postgres://postgres:1234@postgresdb:5432")
    except:
        continue

engine.execute('''CREATE TABLE IF NOT EXISTS tweets (
    username TEXT,
    tweet TEXT,
    score NUMERIC
);
''')

# define load function
def load(**context):
    extract_connection = context['task_instance']
    tweet = extract_connection.xcom_pull(task_ids="transform")
    logging.critical('\n\nTWEET LOADED!')
    engine.execute(f"""INSERT INTO tweets VALUES ('{tweet["username"]}', '{tweet["text"]}', '{tweet["score"]}');""")

# create extract task
extract = PythonOperator(task_id='extract', python_callable=extract, dag=dag)

# create transform task
transform = PythonOperator(task_id='transform', python_callable=transform,
                            provide_context=True, dag=dag)

#create load task
load = PythonOperator(task_id='load', python_callable=load,
                        provide_context=True, dag=dag)

##### 5. Set up dependencies #####
extract >> transform >> load
