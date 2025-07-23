import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "careercoach")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def insert_job(title, company, location, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobs (title, company, location, description)
        VALUES (%s, %s, %s, %s)
    """, (title, company, location, description))
    conn.commit()
    cur.close()
    conn.close()

def fetch_all_jobs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(""" SELECT id,title,company,location,description from jobs""")
    jobs = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return jobs