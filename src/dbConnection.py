import os
import asyncpg
from dotenv import load_dotenv
# Load .env file
load_dotenv()

# Get the connection string from the environment variable
connection_string = os.getenv('DATABASE_URL')
db_pool = None

async def create_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(connection_string)

async def get_db_connection():
    if db_pool is None:
        await create_db_pool()
    return await db_pool.acquire()

async def initialize_database():
    async with await get_db_connection() as conn:
        # Create Users table
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

#async def main():


   #  # Create a connection pool
   #  pool = await asyncpg.create_pool(connection_string)
   #
   #  # Acquire a connection from the pool
   #  async with pool.acquire() as conn:
   #      # Execute SQL commands to retrieve the current time and version from PostgreSQL
   #      time = await conn.fetchval('SELECT NOW();')
   #      version = await conn.fetchval('SELECT version();'
   #
   #  # Close the pool
   # # await pool.close()

    # Print the results
   # print('Current time:', time)
    #print('PostgreSQL version:', version)

# Run the asynchronous main function
#asyncio.run(main())