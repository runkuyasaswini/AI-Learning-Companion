import streamlit as st

from ui.admin_sidebar import (
    show_admin_sidebar,
)

from services.course_service import (
    get_all_courses,
)

from services.topic_service import (
    add_topic,
    get_topics_by_course,
    get_inactive_topics,
    update_topic,
    disable_topic,
    enable_topic,
)


# ==========================================================
# SESSION
# ==========================================================

def initialize_session():

    defaults = {

        "selected_course_id": None,

        "editing_topic": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


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

    course_names = [
        f"{course['icon']} {course['course_name']}"
        for course in courses
    ]

    selected = st.selectbox(
        "Select Course",
        course_names,
    )

    index = course_names.index(selected)

    selected_course = courses[index]

    st.session_state[
        "selected_course_id"
    ] = selected_course["id"]

    return selected_course


# ==========================================================
# ADD TOPIC
# ==========================================================

def show_add_topic_form():

    st.subheader("➕ Add Topic")

    with st.form(
        "add_topic_form",
        clear_on_submit=True,
    ):

        topic_name = st.text_input(
            "Topic Name"
        )

        description = st.text_area(
            "Description"
        )

        display_order = st.number_input(
            "Display Order",
            min_value=1,
            value=1,
        )

        submitted = st.form_submit_button(
            "Add Topic",
            use_container_width=True,
        )

        if submitted:

            if not topic_name.strip():

                st.error(
                    "Topic name is required."
                )

                return

            success, message = add_topic(

                st.session_state[
                    "selected_course_id"
                ],

                topic_name,

                description,

                display_order,

            )

            if success:

                st.success(message)

                st.rerun()

            else:

                st.error(message)

# ==========================================================
# EDIT TOPIC
# ==========================================================

def show_edit_topic_form():

    topic = st.session_state["editing_topic"]

    if topic is None:

        return

    with st.expander(
        "✏️ Edit Topic",
        expanded=True,
    ):

        with st.form(
            f"edit_topic_{topic['id']}"
        ):

            topic_name = st.text_input(
                "Topic Name",
                value=topic["topic_name"],
            )

            description = st.text_area(
                "Description",
                value=topic["description"] or "",
            )

            display_order = st.number_input(
                "Display Order",
                min_value=1,
                value=topic["display_order"],
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

                update_topic(

                    topic["id"],

                    topic_name,

                    description,

                    display_order,

                )

                st.success(
                    "Topic updated successfully."
                )

                st.session_state[
                    "editing_topic"
                ] = None

                st.rerun()

            if cancel:

                st.session_state[
                    "editing_topic"
                ] = None

                st.rerun()

# ==========================================================
# ACTIVE TOPICS
# ==========================================================

def show_topics():

    topics = get_topics_by_course(

        st.session_state[
            "selected_course_id"
        ]

    )

    st.subheader("📘 Topics")

    if not topics:

        st.info(
            "No topics available."
        )

        return
    for topic in topics:

        left, right = st.columns([5, 1])

        with left:

            st.markdown(
                f"""
                ### {topic["display_order"]}. {topic["topic_name"]}

                {topic["description"]}
                """
                            )

        with right:

            if st.button(
                "✏️",
                key=f"edit_topic_{topic['id']}",
                use_container_width=True,
            ):

                st.session_state[
                    "editing_topic"
                ] = dict(topic)

                st.rerun()

            if st.button(
                "🚫",
                key=f"disable_topic_{topic['id']}",
                use_container_width=True,
            ):

                disable_topic(
                    topic["id"]
                )

                st.success(
                    "Topic disabled successfully."
                )

                st.rerun()

        st.divider()

# ==========================================================
# INACTIVE TOPICS
# ==========================================================

def show_inactive_topics():

    topics = get_inactive_topics(

        st.session_state[
            "selected_course_id"
        ]

    )

    if not topics:

        return

    st.subheader("⚫ Inactive Topics")

    for topic in topics:

        left, right = st.columns([5, 1])

        with left:

            st.markdown(
                f"""
### {topic["display_order"]}. {topic["topic_name"]}

{topic["description"]}
"""
            )

        with right:

            if st.button(
                "✅",
                key=f"enable_topic_{topic['id']}",
                use_container_width=True,
            ):

                enable_topic(
                    topic["id"]
                )

                st.success(
                    "Topic enabled successfully."
                )

                st.rerun()

        st.divider()

# ==========================================================
# PAGE
# ==========================================================

def show_admin_topics():

    initialize_session()

    show_admin_sidebar()

    st.title("📖 Topic Management")

    st.caption(
        "Create and manage learning topics."
    )

    st.divider()

    selected_course = select_course()

    if selected_course is None:

        return

    show_add_topic_form()

    show_edit_topic_form()

    st.divider()

    show_topics()

    st.divider()

    show_inactive_topics()