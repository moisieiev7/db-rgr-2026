import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Створює та повертає з'єднання з базою даних."""
    try:
        conn = psycopg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except psycopg.Error as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None