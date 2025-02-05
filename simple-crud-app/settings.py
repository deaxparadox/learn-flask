import os
from dotenv import load_dotenv

SECRET_KEY = os.environ.get("SECRET_KEY")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
DBNAME = os.environ.get("DBNAME")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

DATABASE_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

print(DATABASE_URL)