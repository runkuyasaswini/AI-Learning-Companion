from database.db import get_connection


# ==========================================================
# SAVE LEARNING HISTORY
# ==========================================================

def save_learning_history(user_id, domain, topic):
    """
    Save a completed topic for the user.

    Returns:
        True  -> Topic saved successfully.
        False -> Topic already exists.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM learning_history
        WHERE user_id = ?
        AND domain = ?
        AND topic = ?
        """,
        (
            user_id,
            domain,
            topic,
        ),
    )

    if cursor.fetchone():

        conn.close()
        return False

    cursor.execute(
        """
        INSERT INTO learning_history
        (
            user_id,
            domain,
            topic
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """,
        (
            user_id,
            domain,
            topic,
        ),
    )

    conn.commit()
    conn.close()

    return True


# ==========================================================
# CHECK COMPLETION
# ==========================================================

def is_topic_completed(
    user_id,
    domain,
    topic,
):
    """
    Check whether a topic has already been completed.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM learning_history
        WHERE user_id = ?
        AND domain = ?
        AND topic = ?
        """,
        (
            user_id,
            domain,
            topic,
        ),
    )

    completed = cursor.fetchone() is not None

    conn.close()

    return completed


# ==========================================================
# GET LEARNING HISTORY
# ==========================================================

def get_learning_history(user_id):
    """
    Return the user's learning history.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            domain,
            topic,
            completed_at
        FROM learning_history
        WHERE user_id = ?
        ORDER BY completed_at DESC
        """,
        (user_id,),
    )

    history = cursor.fetchall()

    conn.close()

    return history


# ==========================================================
# GET COMPLETED TOPICS
# ==========================================================

def get_completed_topics(user_id):
    """
    Return all completed topics.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT topic
        FROM learning_history
        WHERE user_id = ?
        ORDER BY completed_at DESC
        """,
        (user_id,),
    )

    topics = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return topics


# ==========================================================
# GET COMPLETED COUNT
# ==========================================================

def get_completed_count(user_id):
    """
    Return total number of completed topics.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM learning_history
        WHERE user_id = ?
        """,
        (user_id,),
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_completed_count_by_domain(user_id, domain):
    """
    Return the number of completed topics in a specific domain.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM learning_history
        WHERE user_id = ?
        AND domain = ?
        """,
        (
            user_id,
            domain,
        ),
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count