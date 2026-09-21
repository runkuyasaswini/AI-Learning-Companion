import sqlite3
from database.db import get_connection
from pathlib import Path
import shutil

# ==========================================================
# ADD COURSE
# ==========================================================

def add_course(
    course_name,
    description,
    icon,
):
    """
    Add a new course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO courses
            (
                course_name,
                description,
                icon
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                course_name.strip(),
                description.strip(),
                icon.strip(),
            ),
        )

        conn.commit()

        return True, "Course added successfully."

    except sqlite3.IntegrityError:

        return False, "Course already exists."

    except Exception as e:

        return False, f"Failed to add course: {str(e)}"

    finally:

        conn.close()

# ==========================================================
# COURSE EXISTS
# ==========================================================

def course_exists(
    course_name,
):
    """
    Check whether a course already exists.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM courses
        WHERE LOWER(course_name) = LOWER(?)
        """,
        (
            course_name.strip(),
        ),
    )

    course = cursor.fetchone()

    conn.close()

    return course is not None


# ==========================================================
# GET ALL COURSES
# ==========================================================

def get_all_courses():
    """
    Return all active courses.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM courses
        WHERE is_active = 1
        ORDER BY course_name
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==========================================================
# GET INACTIVE COURSES
# ==========================================================

def get_inactive_courses():
    """
    Return all disabled courses.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM courses
        WHERE is_active = 0
        ORDER BY course_name
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# GET COURSE BY ID
# ==========================================================

def get_course(
    course_id,
):
    """
    Return one course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM courses
        WHERE id = ?
        """,
        (
            course_id,
        ),
    )

    row = cursor.fetchone()

    conn.close()

    return row

# ==========================================================
# UPDATE COURSE
# ==========================================================

def update_course(
    course_id,
    course_name,
    description,
    icon,
):
    """
    Update course details and rename the
    uploaded materials folder if required.
    """

    conn = get_connection()

    cursor = conn.cursor()

    # ------------------------------------------
    # Get existing course name
    # ------------------------------------------

    cursor.execute(
        """
        SELECT course_name
        FROM courses
        WHERE id = ?
        """,
        (course_id,),
    )

    row = cursor.fetchone()

    if row is None:

        conn.close()

        return False

    old_course_name = row["course_name"]

    new_course_name = course_name.strip()

    # ------------------------------------------
    # Rename uploads folder
    # ------------------------------------------

    if old_course_name != new_course_name:

        uploads_root = Path("uploads/courses")

        old_folder = uploads_root / old_course_name

        new_folder = uploads_root / new_course_name

        if old_folder.exists():

            # If destination doesn't exist,
            # simply rename.

            if not new_folder.exists():

                old_folder.rename(new_folder)

            else:

                # Merge files if destination exists.

                for file in old_folder.iterdir():

                    shutil.move(
                        str(file),
                        str(new_folder / file.name),
                    )

                old_folder.rmdir()

    # ------------------------------------------
    # Update database
    # ------------------------------------------

    cursor.execute(
        """
        UPDATE courses
        SET
            course_name = ?,
            description = ?,
            icon = ?
        WHERE id = ?
        """,
        (
            new_course_name,
            description.strip(),
            icon.strip(),
            course_id,
        ),
    )

    conn.commit()

    conn.close()

    return True

# ==========================================================
# DELETE COURSE
# ==========================================================

def disable_course(
    course_id,
):
    """
    Soft delete a course.Disabling
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE courses
        SET is_active = 0
        WHERE id = ?
        """,
        (
            course_id,
        ),
    )

    conn.commit()

    conn.close()

    return True

# ==========================================================
# ENABLE COURSE
# ==========================================================

def enable_course(
    course_id,
):
    """
    Enable a previously disabled course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE courses
        SET is_active = 1
        WHERE id = ?
        """,
        (
            course_id,
        ),
    )

    conn.commit()

    conn.close()

    return True

if __name__ == "__main__":

    success, message = add_course(
        "Python",
        "Python Programming",
        "🐍",
    )

    print(success, message)

    print()

    courses = get_all_courses()

    for course in courses:

        print(dict(course))