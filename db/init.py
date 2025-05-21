'''
Database Initialization Module for Manuel Discord Bot

This module handles all database-related operations.
'''
from pathlib import Path
import sqlite3

# Database file path (stores in same directory as this module)
DB_PATH = Path(__file__).resolve().parent / 'manuel.db'

# table init functions
def get_connection():
    '''
    Establish a new database connection.
    '''
    return sqlite3.connect(DB_PATH)

def init_role_table():
    '''
    Establish and return a new SQLite database connection.
    '''
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS role_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                role_type TEXT NOT NULL,
                role_id INTEGER NOT NULL,
                discord_name INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            '''
        )
        conn.commit()

def init_server_config_table():
    '''
    Initialize the server config table schema if not exists.
    '''
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS server_config (
            guild_id INTEGER PRIMARY KEY,
            welcome_channel_id INTEGER,
            is_welcome INTEGER,
            welcome_message TEXT,
            channel_name TEXT,
            updated_at TEXT DEFAULT TIMESTAMP
            )
            '''
        )
        conn.commit()

def init_all_tables():
    '''
    Initialize all necessary database tables.
    '''
    init_role_table()
    init_server_config_table()