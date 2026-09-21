import sqlite3

from database.db import get_connection


# ==========================================================
# ADD TOPIC
# ==========================================================

def add_topic(
    course_id,
    topic_name,
    description,
    display_order,
):
    """
    Add a new topic to a course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO topics
            (
                course_id,
                topic_name,
                description,
                display_order
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                course_id,
                topic_name.strip(),
                description.strip(),
                display_order,
            ),
        )

        conn.commit()

        return True, "Topic added successfully."

    except sqlite3.IntegrityError:

        return False, "Topic already exists."

    except Exception as e:

        return False, f"Failed to add topic: {str(e)}"

    finally:

        conn.close()


# ==========================================================
# TOPIC EXISTS
# ==========================================================

def topic_exists(
    course_id,
    topic_name,
):
    """
    Check whether a topic already exists
    within the same course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM topics
        WHERE
            course_id = ?
        AND LOWER(topic_name) = LOWER(?)
        """,
        (
            course_id,
            topic_name.strip(),
        ),
    )

    topic = cursor.fetchone()

    conn.close()

    return topic is not None


# ==========================================================
# GET ACTIVE TOPICS
# ==========================================================

def get_topics_by_course(
    course_id,
):
    """
    Return active topics
    for a course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM topics
        WHERE
            course_id = ?
        AND
            is_active = 1
        ORDER BY
            display_order,
            topic_name
        """,
        (
            course_id,
        ),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# GET INACTIVE TOPICS
# ==========================================================

def get_inactive_topics(
    course_id,
):
    """
    Return disabled topics
    for a course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM topics
        WHERE
            course_id = ?
        AND
            is_active = 0
        ORDER BY
            display_order,
            topic_name
        """,
        (
            course_id,
        ),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==========================================================
# GET TOPIC BY ID
# ==========================================================

def get_topic(
    topic_id,
):
    """
    Return a single topic.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM topics
        WHERE id = ?
        """,
        (
            topic_id,
        ),
    )

    topic = cursor.fetchone()

    conn.close()

    return topic

# ==========================================================
# UPDATE TOPIC
# ==========================================================

def update_topic(
    topic_id,
    topic_name,
    description,
    display_order,
):
    """
    Update topic details.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE topics
        SET
            topic_name = ?,
            description = ?,
            display_order = ?
        WHERE id = ?
        """,
        (
            topic_name.strip(),
            description.strip(),
            display_order,
            topic_id,
        ),
    )

    conn.commit()

    conn.close()

    return True

# ==========================================================
# DISABLE TOPIC
# ==========================================================

def disable_topic(
    topic_id,
):
    """
    Disable a topic.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE topics
        SET is_active = 0
        WHERE id = ?
        """,
        (
            topic_id,
        ),
    )

    conn.commit()

    conn.close()

    return True

# ==========================================================
# ENABLE TOPIC
# ==========================================================

def enable_topic(
    topic_id,
):
    """
    Enable a previously disabled topic.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE topics
        SET is_active = 1
        WHERE id = ?
        """,
        (
            topic_id,
        ),
    )

    conn.commit()

    conn.close()

    return True

def get_topics_by_course(course_id):
    """
    Return all active topics for a course.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM topics
        WHERE course_id = ?
        AND is_active = 1
        ORDER BY topic_name
        """,
        (course_id,),
    )

    topics = cursor.fetchall()

    conn.close()

    return topics