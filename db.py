import os
import mysql.connector
from dotenv import load_dotenv
import streamlit as st

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        auth_plugin="mysql_native_password",
        connection_timeout=10
    )
