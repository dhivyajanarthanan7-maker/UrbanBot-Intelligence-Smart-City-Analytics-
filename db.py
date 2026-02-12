import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")),
            connection_timeout=10
        )
        return conn

    except Exception as e:
        print("DATABASE CONNECTION FAILED:", e)
        return None


