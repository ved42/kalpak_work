import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL")
USE_POSTGRES = DB_URL is not None


def init_db():
    """Initialize database tables for chat history."""
    if USE_POSTGRES:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                session_id TEXT,
                query TEXT,
                timestamp TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    else:
        conn = sqlite3.connect("chat_history.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                session_id TEXT,
                query TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()


def save_message(session_id: str, query: str):
    """Save a message into DB."""
    ts = datetime.now()

    if USE_POSTGRES:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (session_id, query, timestamp) VALUES (%s, %s, %s)",
            (session_id, query, ts)
        )
        conn.commit()
        cur.close()
        conn.close()
    else:
        conn = sqlite3.connect("chat_history.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (session_id, query, timestamp) VALUES (?, ?, ?)",
            (session_id, query, ts.isoformat())
        )
        conn.commit()
        conn.close()


def get_last_messages(session_id: str, n: int = 10):
    """Retrieve last N messages for a session."""
    if USE_POSTGRES:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("""
            SELECT query FROM chat_history 
            WHERE session_id = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        """, (session_id, n))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [r["query"] for r in rows]
    else:
        conn = sqlite3.connect("chat_history.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT query FROM chat_history 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (session_id, n))
        rows = cur.fetchall()
        conn.close()
        return [r[0] for r in rows]
