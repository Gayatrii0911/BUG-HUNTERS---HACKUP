import sqlite3
import os

DB_PATH = "fraud_detection.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            sender_id TEXT,
            receiver_id TEXT,
            amount REAL,
            risk_score REAL,
            action TEXT,
            timestamp TEXT
        );
        CREATE TABLE IF NOT EXISTS alerts (
            alert_id TEXT PRIMARY KEY,
            transaction_id TEXT,
            sender_id TEXT,
            amount REAL,
            action TEXT,
            risk_score REAL,
            reasons TEXT,
            timestamp TEXT
        );
        CREATE TABLE IF NOT EXISTS ml_training_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            features TEXT,
            label INTEGER,
            timestamp TEXT
        );
    """)
    conn.commit()
    conn.close()