import streamlit as st

from ui.admin_sidebar import (
    show_admin_sidebar,
)

from services.course_service import (
    add_course,
    get_all_courses,
    get_inactive_courses,
    disable_course,
    enable_course,
    update_course,
)


# ==========================================================
# INITIALIZE SESSION
# ==========================================================

def initialize_session():

    defaults = {

        "course_refresh": False,

        "editing_course": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==========================================================
# ADD COURSE FORM
# ==========================================================

def show_add_course_form():

    st.subheader("➕ Add New Course")

    with st.form(
        "add_course_form",
        clear_on_submit=True,
    ):

        course_name = st.text_input(
            "Course Name"
        )

        description = st.text_area(
            "Description"
        )

        icon = st.text_input(
            "Icon",
            placeholder="🐍"
        )

        submitted = st.form_submit_button(
            "Add Course",
            use_container_width=True,
        )

        if submitted:

            if not course_name.strip():

                st.error(
                    "Course name is required."
                )

                return

            success, message = add_course(
                course_name,
                description,
                icon,
            )

            if success:

                st.success(message)

                st.session_state[
                    "course_refresh"
                ] = True

                st.rerun()

            else:

                st.error(message)

# ==========================================================
# EDIT COURSE
# ==========================================================

def show_edit_course_form():

    course = st.session_state["editing_course"]

    if course is None:

        return

    with st.expander(
        "✏️ Edit Course",
        expanded=True,
    ):

        with st.form(
            f"edit_course_{course['id']}"
        ):

            course_name = st.text_input(
                "Course Name",
                value=course["course_name"],
            )

            description = st.text_area(
                "Description",
                value=course["description"] or "",
            )

            icon = st.text_input(
                "Icon",
                value=course["icon"] or "",
            )
            
            left, right = st.columns(2)

            with left:

                save = st.form_submit_button(
                    "💾 Save",
                    use_container_width=True,
                )

            with right:

                cancel = st.form_submit_button(
                    "Cancel",
                    use_container_width=True,
                )

            if save:

                success = update_course(

                    course["id"],

                    course_name,

                    description,

                    icon,

                )

                if success:

                    st.success(
                        "Course updated successfully."
                    )

                    st.session_state[
                        "editing_course"
                    ] = None

                    st.rerun()

            if cancel:

                st.session_state[
                    "editing_course"
                ] = None

                st.rerun()

# ==========================================================
# COURSE LIST
# ==========================================================

def show_courses():

    st.subheader("📚 Available Courses")

    courses = get_all_courses()

    if not courses:

        st.info(
            "No courses available."
        )

        return
    for course in courses:

        left, right = st.columns([5, 1])

        with left:

            st.markdown(
                f"""
                ### {course["icon"]} {course["course_name"]}

                {course["description"]}
                """
                            )

        with right:

            if st.button(
                "✏️",
                key=f"edit_{course['id']}",
                use_container_width=True,
            ):

                st.session_state["editing_course"] = dict(course)

                st.rerun()

            if st.button(
                "🚫",
                key=f"disable_{course['id']}",
                use_container_width=True,
            ):

                disable_course(
                    course["id"]
                )

                st.success(
                    "Course disabled successfully."
                )

                st.rerun()

        st.divider()

# ==========================================================
# INACTIVE COURSES
# ==========================================================

def show_inactive_courses():

    inactive_courses = get_inactive_courses()

    if not inactive_courses:

        return

    st.subheader("⚫ Inactive Courses")

    for course in inactive_courses:

        left, right = st.columns([5, 1])

        with left:

            st.markdown(
                f"""
### {course["icon"]} {course["course_name"]}

{course["description"]}
"""
            )

        with right:

            if st.button(
                "✅",
                key=f"enable_{course['id']}",
                use_container_width=True,
            ):

                enable_course(
                    course["id"]
                )

                st.success(
                    "Course enabled successfully."
                )

                st.rerun()

        st.divider()

# ==========================================================
# PAGE
# ==========================================================

def show_admin_courses():

    initialize_session()

    show_admin_sidebar()

    st.title("📚 Course Management")

    st.caption(
        "Create and manage learning courses."
    )

    st.divider()

    show_add_course_form()

    show_edit_course_form()

    st.divider()

    show_courses()

    st.divider()

    show_inactive_courses()