from flask import Flask, request
import os
import psycopg2
from datetime import datetime
import socket
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'postgres'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitors (
                id SERIAL PRIMARY KEY,
                name TEXT,
                timestamp TIMESTAMP,
                instance_name TEXT
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

@app.route('/')
def home():
    instance_name = os.getenv('INSTANCE_NAME', 'unknown')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    conn = get_db_connection()
    if conn is None:
        return "Database connection error", 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO visitors (name, timestamp, instance_name) VALUES (%s, %s, %s) RETURNING id", 
                       ('Guest', datetime.utcnow(), instance_name))
        visit_id = cursor.fetchone()[0]
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM visitors")
        visit_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"New visit logged: ID={visit_id}, Instance={instance_name}, IP={ip_address}, User-Agent={user_agent}")
        
        return f"Entry ID: {visit_count}"
    except Exception as e:
        logger.error(f"Database write/read error: {e}")
        return "Database error", 500

@app.route('/<int:entry_id>')
def get_entry(entry_id):
    conn = get_db_connection()
    if conn is None:
        return "Database connection error", 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM visitors WHERE id = %s", (entry_id,))
        entry = cursor.fetchone()
        cursor.close()
        conn.close()
        if entry:
            return f"Entry ID: {entry[0]}, Name: {entry[1]}, Timestamp: {entry[2]}, Instance: {entry[3]}"
        else:
            return "Entry not found", 404
    except Exception as e:
        logger.error(f"Database read error: {e}")
        return "Database error", 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
