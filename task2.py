# db_helpers.py
import psycopg2

DB_HOST = "localhost"
DB_NAME = "snake_game"
DB_USER = "postgres"
DB_PASS = "Sherlok123"
DB_PORT = 5432

def get_connection():
    """
    Returns a new PostgreSQL connection using psycopg2.
    Adjust host, port, DB name, user, and password as needed.
    """
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def create_tables():
    """
    Creates user and user_score tables if they do not already exist.
    """
    # Connect and create a cursor
    conn = get_connection()
    cursor = conn.cursor()

    # Create 'user' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "user" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL
        );
    """)

    # Create 'user_score' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
            level INTEGER NOT NULL,
            score INTEGER NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

def get_or_create_user(username):
    """
    Returns the user's ID from the user table.
    If the user does not exist, creates a new entry.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1) Try to fetch the user
    cursor.execute('SELECT id FROM "user" WHERE username = %s;', (username,))
    row = cursor.fetchone()

    # 2) If user is found, return that ID
    if row is not None:
        user_id = row[0]
    else:
        # 3) Otherwise, insert a new user
        cursor.execute('INSERT INTO "user" (username) VALUES (%s) RETURNING id;', (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()

    cursor.close()
    conn.close()
    return user_id

def get_latest_user_score(user_id):
    """
    Returns the most recent (level, score) for the given user_id,
    or (1, 0) if no record exists.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT level, score
        FROM user_score
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 1;
    """, (user_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return (row[0], row[1])  # (level, score)
    else:
        return (1, 0)  # Default to level 1, score 0 if none saved

def save_user_score(user_id, level, score):
    """
    Saves the current level and score for the user in the user_score table.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_score (user_id, level, score)
        VALUES (%s, %s, %s);
    """, (user_id, level, score))
    conn.commit()

    cursor.close()
    conn.close()
