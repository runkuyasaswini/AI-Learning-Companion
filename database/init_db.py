from database.db import get_connection

import bcrypt


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # ======================================================
    # USERS
    # ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ------------------------------------------------------
    # Add role column if it does not exist
    # ------------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(users)"
    )

    columns = [
        column["name"]
        for column in cursor.fetchall()
    ]

    if "role" not in columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN role TEXT NOT NULL
        DEFAULT 'learner'
        """)

    # ------------------------------------------------------
    # Create default admin account
    # ------------------------------------------------------

    cursor.execute("""
    SELECT id
    FROM users
    WHERE username = ?
    """, ("admin",))

    admin = cursor.fetchone()

    if admin is None:

        hashed_password = bcrypt.hashpw(
            "admin123".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute("""
        INSERT INTO users
        (
            username,
            full_name,
            email,
            password,
            role
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """,
       (
            "admin",
            "System Administrator",
            "admin@learningcompanion.com",
            hashed_password,
            "admin",
        ))

    # ======================================================
    # LEARNING HISTORY
    # ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        domain TEXT NOT NULL,
        topic TEXT NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    # ======================================================
    # QUIZ HISTORY
    # ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        domain TEXT NOT NULL,
        topic TEXT NOT NULL,

        difficulty TEXT NOT NULL,

        score INTEGER NOT NULL,

        total_questions INTEGER NOT NULL,

        percentage REAL NOT NULL,

        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

        # ======================================================
    # COURSES
    # ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        course_name TEXT UNIQUE NOT NULL,

        description TEXT,

        icon TEXT,

        is_active INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)
    
        # ======================================================
    # TOPICS
    # ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        course_id INTEGER NOT NULL,

        topic_name TEXT NOT NULL,

        description TEXT,

        display_order INTEGER DEFAULT 0,

        is_active INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(course_id)
        REFERENCES courses(id)
    )
    """)

        # ======================================================
    # LEARNING MATERIALS
    # ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_materials(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        course_id INTEGER NOT NULL,

        title TEXT NOT NULL,

        file_name TEXT NOT NULL,

        file_path TEXT NOT NULL,

        file_size INTEGER DEFAULT 0,

        indexed INTEGER DEFAULT 0,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(course_id)
        REFERENCES courses(id)

    )
    """)

    conn.commit()

    conn.close()