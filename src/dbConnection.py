import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv('DATABASE_URL')

async def initialize_database():
    global conn
    conn = await asyncpg.connect(connection_string)
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Messages table
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
        message_id SERIAL PRIMARY KEY,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES Users(user_id),
        FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
    )
    ''')

async def register_user(username, password_hash):
    await conn.execute('''
    INSERT INTO users(username, password_hash) VALUES($1, $2)
    ''', username, password_hash)


# async def get_user(username):
#     await conn.fetchrow('SELECT * FROM users WHERE username = $1', username)
