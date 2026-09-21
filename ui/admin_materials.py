import streamlit as st

from ui.admin_sidebar import (
    show_admin_sidebar,
)

from services.course_service import (
    get_all_courses,
)

from services.material_service import (
    add_material,
    get_materials_by_course,
    delete_material,
)

from services.knowledge_base_service import (
    build_course_knowledge_base,
)

# ==========================================================
# SESSION
# ==========================================================

def initialize_session():

    if "selected_material_course" not in st.session_state:

        st.session_state[
            "selected_material_course"
        ] = None

    if "selected_course_name" not in st.session_state:

        st.session_state[
            "selected_course_name"
        ] = None
        
# ==========================================================
# COURSE SELECTOR
# ==========================================================

def select_course():

    courses = get_all_courses()

    if not courses:

        st.warning(
            "Please create a course first."
        )

        return None

    names = [

        f"{course['icon']} {course['course_name']}"

        for course in courses

    ]

    selected = st.selectbox(

        "Select Course",

        names,

    )

    index = names.index(selected)

    course = courses[index]

    st.session_state[
        "selected_material_course"
    ] = course["id"]

    st.session_state[
        "selected_course_name"
    ] = course["course_name"]

    return course

# ==========================================================
# UPLOAD FORM
# ==========================================================

def show_upload_form():

    st.subheader(
        "📄 Upload Learning Material"
    )

    with st.form(
        "upload_material_form",
        clear_on_submit=True,
    ):

        title = st.text_input(
            "Material Title"
        )

        uploaded_file = st.file_uploader(

            "Choose PDF",

            type=["pdf"],

        )

        submitted = st.form_submit_button(

            "Upload PDF",

            use_container_width=True,

        )

        if submitted:

            if uploaded_file is None:

                st.error(
                    "Please choose a PDF."
                )

                return

            success, message = add_material(

                    st.session_state[
                        "selected_material_course"
                    ],

                    st.session_state[
                        "selected_course_name"
                    ],

                    title,

                    uploaded_file,

                )

            if success:

                st.success(message)

                st.rerun()

            else:

                st.error(message)

# ==========================================================
# BUILD KNOWLEDGE BASE
# ==========================================================

def show_build_knowledge_base():

    st.subheader("🧠 Knowledge Base")

    st.caption(
        "Generate embeddings and rebuild the AI knowledge base for this course."
    )

    if st.button(
        "🧠 Build Knowledge Base",
        use_container_width=True,
    ):

        with st.spinner(
            "Building knowledge base..."
        ):

            success, message = build_course_knowledge_base(

                st.session_state[
                    "selected_material_course"
                ]

            )

        if success:

            st.success(message)

            st.rerun()

        else:

            st.error(message)

# ==========================================================
# MATERIAL LIST
# ==========================================================

def show_materials():

    materials = get_materials_by_course(

        st.session_state[
            "selected_material_course"
        ]

    )

    st.subheader(
        "📚 Uploaded Materials"
    )

    if not materials:

        st.info(
            "No learning materials uploaded."
        )

        return

    for material in materials:

        left, right = st.columns([5, 1])

        status = (
            "🟢 Indexed"
            if material["indexed"]
            else "🟡 Pending"
        )

        file_size = round(
            material["file_size"] / 1024,
            2,
        )

        with left:

            st.markdown(
                f"""
### {material["title"]}

**File:** {material["file_name"]}

**Size:** {file_size} KB

**Status:** {status}

**Uploaded:** {material["uploaded_at"]}
"""
            )

        with right:

            st.button(
                "🧠",
                key=f"index_{material['id']}",
                disabled=True,
                use_container_width=True,
            )

            if st.button(
                "🗑️",
                key=f"delete_material_{material['id']}",
                use_container_width=True,
            ):

                delete_material(
                    material["id"]
                )

                st.success(
                    "Material deleted successfully."
                )

                st.rerun()

        st.divider()

# ==========================================================
# PAGE
# ==========================================================

def show_admin_materials():

    initialize_session()

    show_admin_sidebar()

    st.title(
        "📄 Learning Materials"
    )

    st.caption(
        "Manage course PDFs."
    )

    st.divider()

    course = select_course()

    if course is None:

        return

    show_upload_form()

    st.divider()

    show_build_knowledge_base()

    st.divider()

    show_materials()