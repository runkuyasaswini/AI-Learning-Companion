from rag.summary_generator import (
    generate_summary,
    generate_uploaded_pdf_summary,
)


# ==========================================================
# COURSE SUMMARY
# ==========================================================

def generate_course_summary(
    topic: str,
    course: str | None = None,
):
    """
    Generate a summary for a topic
    from the course knowledge base.
    """

    result = generate_summary(
        topic=topic,
        course=course,
    )

    if isinstance(result, dict) and "error" in result:

        return result

    if (
        not isinstance(result, dict)
        or "summary" not in result
    ):

        return {
            "error":
            "Unable to generate summary."
        }

    return result

# ==========================================================
# PDF SUMMARY
# ==========================================================

def summarize_uploaded_pdf(
    pdf_path,
):
    """
    Generate a summary from an uploaded PDF.
    """

    result = generate_uploaded_pdf_summary(
        pdf_path,
    )

    if (
        not isinstance(result, dict)
        or "summary" not in result
    ):

        return {
            "error":
            "Unable to summarize the uploaded PDF."
        }

    return result