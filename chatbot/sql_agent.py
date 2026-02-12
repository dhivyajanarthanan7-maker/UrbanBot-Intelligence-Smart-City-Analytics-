# chatbot/sql_agent.py

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL missing in .env")

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10
)

def run_query(query: str):
    """Main DB query executor used by chatbot"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return result.fetchall()
    except SQLAlchemyError as e:
        return f"Database Error: {str(e)}"

# analytics uses this alias
def execute_query(query: str):
    return run_query(query)
