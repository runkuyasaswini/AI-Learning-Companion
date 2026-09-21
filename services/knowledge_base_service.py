from pathlib import Path

from database.db import get_connection

from rag.vector_store import build_vector_store

from services.material_service import (
    get_materials_by_course,
)


# BUILD KNOWLEDGE BASE



def build_course_knowledge_base(
    course_id: int,
):
    """
    Build the FAISS knowledge base for all
    uploaded materials of a course.
    """

    materials = get_materials_by_course(
        course_id
    )

    cursor = get_connection().cursor()

    cursor.execute(
        """
        SELECT course_name
        FROM courses
        WHERE id = ?
        """,
        (course_id,)
    )

    row = cursor.fetchone()

    if row is None:

        return False, "Course not found."


    if not materials:

        return (
            False,
            "No learning materials found."
        )
    try:

        build_vector_store(
            documents_folder=Path("uploads/courses")
        )

    except Exception as e:

        return (
            False,
            str(e),
        )
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE learning_materials

        SET indexed = 1

        WHERE

        course_id = ?
        """,
        (
            course_id,
        ),
    )

    conn.commit()

    conn.close()

    return (

        True,

        "Knowledge Base built successfully."

    )