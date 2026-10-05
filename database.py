from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def get_connection():
    connection = psycopg.connect(
        host=os.getenv("AZURE_DB_HOST"),
        port=os.getenv("AZURE_DB_PORT"),
        user=os.getenv("AZURE_DB_USER"),
        password=os.getenv("AZURE_DB_PASSWORD"),
        dbname=os.getenv("AZURE_DB_NAME"),
        # sslmode=os.getenv("AZURE_DB_SSLMODE"),
        row_factory=dict_row,
    )
    return connection

if __name__ == "__main__":
    connection = get_connection()
    print("PostgreSQL connected successfully!")
    connection.close()

