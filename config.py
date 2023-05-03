from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
MODEL_PATH = os.getenv("MODEL_PATH")
DB_IP = os.getenv("DB_IP")


#if not os.environ['env']:
    #raise Exception('need to set env')

env = os.environ['env']

