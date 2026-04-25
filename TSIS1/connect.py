# connect.py
import psycopg2
import os
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def run_sql_file(filename):
    """Executes SQL commands from a file located in the same folder[cite: 1]"""
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        with open(file_path, 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully executed {filename}")
    except Exception as e:
        print(f"Error executing {filename}: {e}")

def init_database():
    """Initializes schema and procedures[cite: 1]"""
    run_sql_file('schema.sql')
    run_sql_file('procedures.sql')