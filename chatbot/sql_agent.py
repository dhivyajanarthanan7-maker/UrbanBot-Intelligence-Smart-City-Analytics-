from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()   

engine = create_engine(os.getenv("DB_URL"))

def run_query(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()
