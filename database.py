import os

import psycopg

def get_database_connection():
    connection = psycopg.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        dbname = os.getenv("DB_NAME")
    )
    return connection

if __name__ == "__main__":
    connection = get_database_connection()
    print("PostgreSQL connected successfully!")
    connection.close()
