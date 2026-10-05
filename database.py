from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def get_connection():
    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        sslmode=os.getenv("DB_SSLMODE") or "disable",
        row_factory=dict_row,
    )
    return connection

if __name__ == "__main__":
    connection = get_connection()
    print("PostgreSQL connected successfully!")
    connection.close()

