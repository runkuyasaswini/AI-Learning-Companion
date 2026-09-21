import streamlit as st

import tempfile
from pathlib import Path


from ui.sidebar import show_sidebar

from services.course_service import get_all_courses
from services.topic_service import get_topics_by_course
from services.summary_service import (
    generate_course_summary,
    summarize_uploaded_pdf,
)
from utils.pdf_export import generate_summary_pdf


# ==========================================================
# LEARNING SUMMARIES
# ==========================================================

def show_learning_summary():

    show_sidebar()

    st.title("📄 Learning Summaries")

    st.caption(
        "Generate concise revision notes from your course material or upload your own PDF."
    )

    st.divider()

    tab1, tab2 = st.tabs(
        [
            "📚 Course Catalog",
            "📤 Upload Your PDF",
        ]
    )

    # ======================================================
    # COURSE SUMMARY
    # ======================================================

    with tab1:

        courses = get_all_courses()

        if not courses:

            st.info("No courses available.")

            return

        course_names = [
            course["course_name"]
            for course in courses
        ]

        selected_course = st.selectbox(
            "Select Course",
            course_names,
        )

        course = next(
            c
            for c in courses
            if c["course_name"] == selected_course
        )

        topics = get_topics_by_course(
            course["id"]
        )

        if not topics:

            st.info(
                "No topics available."
            )

            return

        topic_names = [
            topic["topic_name"]
            for topic in topics
        ]

        selected_topic = st.selectbox(
            "Select Topic",
            topic_names,
        )

        st.divider()

        if st.button(
            "✨ Generate Summary",
            use_container_width=True,
        ):

            with st.spinner(
                "Generating summary..."
            ):

                result = generate_course_summary(
                    topic=selected_topic,
                    course=selected_course,
                )

            if "error" in result:

                st.warning(
                    result["error"]
                )

            else:

                st.success(
                    "Summary generated successfully."
                )

                st.markdown(
                    result["summary"]
                )

                pdf = generate_summary_pdf(
                    title=f"{selected_topic} Summary",
                    content=result["summary"],
                )

                st.download_button(
                    "⬇ Download Summary PDF",
                    data=pdf,
                    file_name=f"{selected_topic}_Summary.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

    # ======================================================
    # UPLOAD PDF
    # ======================================================

    with tab2:

        st.subheader("📤 Upload Your PDF")

        st.caption(
            "Upload any study material and generate concise revision notes."
        )

        uploaded_pdf = st.file_uploader(
            "Choose a PDF",
            type=["pdf"],
        )

        if uploaded_pdf:

            if st.button(
                "✨ Summarize PDF",
                use_container_width=True,
                key="summarize_uploaded_pdf",
            ):

                with st.spinner(
                    "Reading and summarizing PDF..."
                ):

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf",
                    ) as temp_file:

                        temp_file.write(
                            uploaded_pdf.getbuffer()
                        )

                        pdf_path = temp_file.name

                    result = summarize_uploaded_pdf(
                        pdf_path
                    )

                    Path(pdf_path).unlink(
                        missing_ok=True
                    )

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        "Summary generated successfully."
                    )

                    st.markdown(
                        result["summary"]
                    )

                    pdf = generate_summary_pdf(
                        title=uploaded_pdf.name,
                        content=result["summary"],
                    )

                    st.download_button(
                        "⬇ Download Summary PDF",
                        data=pdf,
                        file_name="Uploaded_PDF_Summary.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )