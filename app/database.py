import psycopg2
from app.config import Config

def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URL)
    return conn
