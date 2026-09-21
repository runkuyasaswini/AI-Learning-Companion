import sqlite3
from pathlib import Path
import shutil

from database.db import get_connection


# ==========================================================
# UPLOAD DIRECTORY
# ==========================================================

UPLOAD_DIR = Path("uploads/courses")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==========================================================
# SAVE FILE
# ==========================================================

def save_material_file(
    course_name: str,
    uploaded_file,
):
    """
    Save uploaded PDF inside the selected course folder.

    uploads/
        courses/
            Python/
                python.pdf
    """

    course_folder = (
        UPLOAD_DIR /
        course_name.strip()
    )

    course_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        course_folder /
        uploaded_file.name
    )

    with open(
        destination,
        "wb",
    ) as file:

        shutil.copyfileobj(
            uploaded_file,
            file,
        )

    return destination

# ==========================================================
# ADD MATERIAL
# ==========================================================

def add_material(
    course_id,
    course_name,
    title,
    uploaded_file,
):
    """
    Save uploaded PDF and register it.
    """

    try:

        saved_path = save_material_file(
            course_name,
            uploaded_file,
        )

        file_size = (
            saved_path
            .stat()
            .st_size
        )

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO learning_materials
            (
                course_id,
                title,
                file_name,
                file_path,
                file_size
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
                course_id,
                title.strip(),
                uploaded_file.name,
                str(saved_path),
                file_size,
            ),
        )

        conn.commit()

        conn.close()

        return True, "Learning material uploaded successfully."

    except sqlite3.IntegrityError:

        return False, "Material already exists."

    except Exception as e:

        return False, f"Upload failed: {str(e)}"
    
# ==========================================================
# GET MATERIALS
# ==========================================================

def get_materials_by_course(
    course_id,
):
    """
    Return all materials
    belonging to a course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM learning_materials
        WHERE course_id = ?
        ORDER BY uploaded_at DESC
        """,
        (
            course_id,
        ),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==========================================================
# GET MATERIAL BY ID
# ==========================================================

def get_material(
    material_id,
):
    """
    Return a single learning material.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM learning_materials
        WHERE id = ?
        """,
        (
            material_id,
        ),
    )

    row = cursor.fetchone()

    conn.close()

    return row

# ==========================================================
# MATERIAL EXISTS
# ==========================================================

def material_exists(
    course_id,
    file_name,
):
    """
    Check whether a file already exists
    for the selected course.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM learning_materials
        WHERE
            course_id = ?
        AND
            LOWER(file_name) = LOWER(?)
        """,
        (
            course_id,
            file_name,
        ),
    )

    row = cursor.fetchone()

    conn.close()

    return row is not None

# ==========================================================
# MARK AS INDEXED
# ==========================================================

def mark_as_indexed(
    material_id,
):
    """
    Mark a learning material as indexed.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE learning_materials
        SET indexed = 1
        WHERE id = ?
        """,
        (
            material_id,
        ),
    )

    conn.commit()

    conn.close()

    return True

# ==========================================================
# DELETE MATERIAL
# ==========================================================

def delete_material(
    material_id,
):
    """
    Delete a learning material.
    """

    material = get_material(
        material_id
    )

    if material is None:

        return False

    try:

        file_path = Path(
            material["file_path"]
        )

        if file_path.exists():

            file_path.unlink()

    except Exception:

        pass

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE
        FROM learning_materials
        WHERE id = ?
        """,
        (
            material_id,
        ),
    )

    conn.commit()

    conn.close()

    return True