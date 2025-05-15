'''
Database Module for Role Permission Management

This module handles persistent storage of Discord role permissions using SQLite.
It provides CRUD operations for guild-specific role assignments with timestamp tracking.
'''
from pathlib import Path
import sqlite3

# Database file path (stores in same directory as this module)
DB_PATH = Path(__file__).resolve().parent / 'manuel_roles.db'

def get_connection():
    '''
    Establish a new database connection.
    '''
    return sqlite3.connect(DB_PATH)

def init_db():
    '''
    Initialize the database schema if not exists.
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            '''
        )
        conn.commit()

def db_set_role(guild_id: int, role_type: str, role_id: int):
    '''
    Assign or update a role permission for a guild.
    '''
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            DELETE FROM role_permissions
            WHERE guild_id = ? AND role_id = ?
            ''',
            (guild_id, role_id)
        )
        cursor.execute(
            '''
            INSERT INTO role_permissions (guild_id, role_type, role_id)
            VALUES (?, ?, ?)
            ''',
            (guild_id, role_type, role_id)
        )
        conn.commit()

def db_get_role(guild_id: int, role_type: str):
    '''
    Retrieve a role ID for specific permission level in a guild.
    '''
    with get_connection() as coon:
        cursor = coon.cursor()
        cursor.execute(
            '''
            SELECT role_id FROM role_permissions
            WHERE guild_id = ? AND role_type = ?
            ''',
            (guild_id, role_type)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    

def db_list_roles(guild_id: int):
    '''
    "List all registered roles for a specific guild.
    '''
    with get_connection() as coon:
        cursor = coon.cursor()
        cursor.execute(
            '''
            SELECT role_type, role_id FROM role_permissions
            WHERE guild_id = ?
            ''',
            (guild_id)
        )
        return cursor.fetchall()