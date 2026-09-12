import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def get_database_connection():
    connection = psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME", "ax_demo")
    )
    return connection

if __name__ == "__main__":
    connection = get_database_connection()
    print("PostgreSQL connected successfully!")
    connection.close()

