import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the connection string from the environment variable
connection_string = os.getenv('DATABASE_URL')

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    1,  # Minimum number of connections in the pool
    10,  # Maximum number of connections in the pool
    connection_string
)

# Check if the pool was created successfully
if connection_pool:
    print("Connection pool created successfully")
else:
    print("Something went wrong")

def connect_on_db():
    conn = connection_pool.getconn()
    if conn:
        print("Successfully received the connection from the pool")
        return conn
    else:
        print("Unable to receive connection from the connection pool")
        return None

def close_db_connection(conn):
    if conn:
        connection_pool.putconn(conn)
