from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

# ==========================================================
# EXPORT SUMMARY TO PDF
# ==========================================================

def generate_summary_pdf(
    title: str,
    content: str,
):
    """
    Generate a PDF from the summary text.

    Returns:
        BytesIO
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
    )

    styles = getSampleStyleSheet()

    story = []

    # ------------------------------------------------------
    # Title
    # ------------------------------------------------------

    story.append(
        Paragraph(
            title,
            styles["Title"],
        )
    )

    story.append(
        Spacer(
            1,
            18,
        )
    )

    # ------------------------------------------------------
    # Content
    # ------------------------------------------------------

    for line in content.split("\n"):

        line = line.strip()

        if not line:

            story.append(
                Spacer(
                    1,
                    8,
                )
            )

            continue

        # Markdown headings

        if line.startswith("# "):

            story.append(
                Paragraph(
                    line[2:],
                    styles["Heading1"],
                )
            )

            continue

        if line.startswith("## "):

            story.append(
                Paragraph(
                    line[3:],
                    styles["Heading2"],
                )
            )

            continue

        if line.startswith("### "):

            story.append(
                Paragraph(
                    line[4:],
                    styles["Heading3"],
                )
            )

            continue

        # Bullet points

        if line.startswith("- "):

            story.append(
                Paragraph(
                    f"• {line[2:]}",
                    styles["BodyText"],
                )
            )

            continue

        # Normal paragraph

        story.append(
            Paragraph(
                line,
                styles["BodyText"],
            )
        )

    document.build(
        story,
    )

    buffer.seek(0)

    return buffer