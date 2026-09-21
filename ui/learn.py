import streamlit as st

from ui.sidebar import show_sidebar

from services.rag_service import ask_ai

from services.course_service import (
    get_all_courses,
    get_course,
)

from services.topic_service import (
    get_topics_by_course,
)

from services.learning_service import (
    save_learning_history,
    is_topic_completed,
    get_completed_count_by_domain,
)


# ==========================================================
# DOMAIN CARDS
# ==========================================================


def show_domain_cards():

    st.title("📚 Learn")

    st.write("### Choose a Learning Domain")

    cols = st.columns(2)

    courses = get_all_courses()

    for index, course in enumerate(courses):

        with cols[index % 2]:

            st.markdown(
                f"### {course['icon']} {course['course_name']}"
            )

            st.caption(course["description"])

            if st.button(
                "Open",
                key=f"open_{course['id']}",
                use_container_width=True,
            ):

                st.session_state["selected_domain"] = course["course_name"]
                st.session_state["selected_course_id"] = course["id"]
                st.session_state["search_topic"] = ""
                st.session_state["current_topic"] = ""
                st.session_state["learning_result"] = None

                st.rerun()


# ==========================================================
# DOMAIN PAGE
# ==========================================================


def show_domain_page(domain):

    course = get_course(
        st.session_state["selected_course_id"]
    )

    user_id = st.session_state["user"]["id"]

    # ------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("⬅ Back"):

            st.session_state["selected_domain"] = None
            st.session_state["selected_course_id"] = None
            st.session_state["search_topic"] = ""
            st.session_state["current_topic"] = ""
            st.session_state["learning_result"] = None

            st.rerun()

    with col2:

        st.title(f"{course['icon']} {domain}")

    with col3:

        if st.button(
                "💬 Ask AI Coach",
                use_container_width=True,
            ):

                st.session_state["coach_domain"] = domain
                st.session_state["coach_topic"] = st.session_state.get(
                    "current_topic"
                )

                st.session_state["page"] = "coach"

                st.rerun()

    st.caption(course["description"])

    completed_topics = get_completed_count_by_domain(
    user_id,
    domain,
)

    st.info(f"🎯 Topics Completed : **{completed_topics}**")

    st.divider()

    # ======================================================
    # SEARCH SECTION
    # ======================================================

    st.subheader("🔍 What would you like to learn today?")

    st.text_input(
        "Search",
        key="search_topic",
        placeholder="Examples: Logistic Regression, SQL JOIN, Python Functions...",
        label_visibility="collapsed",
    )

    if st.button(
        "📖 Learn",
        use_container_width=True,
    ):

        topic = st.session_state["search_topic"].strip()

        if not topic:

            st.warning("Please enter a topic.")

        else:

            with st.spinner("Preparing your lesson..."):

                result = ask_ai(
                    question=topic,
                    course=domain,
                )

                st.session_state["learning_result"] = result
                st.session_state["current_topic"] = topic

            st.rerun()

    # ======================================================
    # LESSON
    # ======================================================

    result = st.session_state.get("learning_result")

    current_topic = st.session_state.get("current_topic")

    if result:

        st.divider()

        with st.container(border=True):

            st.subheader("📘 Learning Material")

            st.caption(
                f"Current Topic: **{current_topic}**"
            )

            st.markdown(
            result["answer"],
            unsafe_allow_html=False,
        )

        st.divider()

        st.subheader("🎯 What's Next?")

                # --------------------------------------------------
        # ACTION CARDS
        # --------------------------------------------------

        st.write(
            "You have finished reading this lesson. Choose what you'd like to do next."
        )

        # ===========================
        # TAKE QUIZ
        # ===========================

        st.markdown("### 📝 Take Quiz")

        st.caption(
            "Test your understanding of this topic with an AI-generated quiz."
        )

        if st.button(
            "Start Quiz",
            use_container_width=True,
            key="start_quiz",
        ):

            st.session_state["quiz_domain"] = domain
            st.session_state["quiz_topic"] = current_topic

            st.session_state["quiz_questions"] = None
            st.session_state["quiz_answers"] = {}
            st.session_state["quiz_result"] = None
            st.session_state["quiz_stage"] = "setup"

            st.session_state["page"] = "quiz"

            st.rerun()

        st.divider()

        # ===========================
        # MARK COMPLETED
        # ===========================

        completed = is_topic_completed(
            user_id,
            domain,
            current_topic,
        )

        st.markdown("### ✅ Mark as Completed")

        st.caption(
            "Save this lesson to your completed learning history."
        )

        if completed:

            st.success("🎉 You have already completed this topic.")

        else:

            if st.button(
                "Mark as Completed",
                use_container_width=True,
                key="complete_topic",
            ):

                saved = save_learning_history(
                    user_id,
                    domain,
                    current_topic,
                )

                if saved:

                    st.success(
                        "Topic marked as completed successfully!"
                    )

                    st.rerun()

                else:

                    st.info(
                        "This topic is already in your learning history."
                    )

        st.divider()

        # ===========================
        # AI COACH
        # ===========================

        st.markdown("### 💬 Ask AI Coach")

        st.caption(
            "Still have doubts? Continue learning with your AI Coach."
        )

        if st.button(
            "Open AI Coach",
            use_container_width=True,
            key="open_coach",
        ):

            st.session_state["coach_domain"] = domain
            st.session_state["coach_topic"] = current_topic

            st.session_state["page"] = "coach"

            st.rerun()

        st.divider()

        # ===========================
        # LEARN ANOTHER TOPIC
        # ===========================

        st.markdown("### 🔍 Learn Another Topic")

        st.caption(
            "Clear the current lesson and start learning a different topic."
        )

        if st.button(
            "Search Another Topic",
            use_container_width=True,
            key="another_topic",
        ):

            st.session_state["search_topic"] = ""
            st.session_state["current_topic"] = ""
            st.session_state["learning_result"] = None

            st.rerun()
            # ======================================================
    # SUGGESTED TOPICS
    # ======================================================

    st.divider()

    st.subheader("📖 Suggested Topics")

    st.caption(
        "Popular topics you can start learning in this domain."
    )

    topic_cols = st.columns(2)

    topics = get_topics_by_course(
        st.session_state["selected_course_id"]
    )

    for index, topic in enumerate(topics):

        with topic_cols[index % 2]:

            if st.button(
            topic["topic_name"],
            key=f"{domain}_{topic['id']}",
            use_container_width=True,
        ):
                with st.spinner("Preparing your lesson..."):
                    
                    result = ask_ai(
                            question=topic["topic_name"],
                            course=domain,
                        )

                    st.session_state["current_topic"] = topic["topic_name"]
                    st.session_state["learning_result"] = result

                st.rerun()

# ==========================================================
# MAIN PAGE
# ==========================================================


def show_learn():

    show_sidebar()

    # ------------------------------------------------------
    # Session Initialization
    # ------------------------------------------------------

    defaults = {
        "selected_domain": None,
        "search_topic": "",
        "current_topic": "",
        "learning_result": None,
        "quiz_domain": None,
        "quiz_topic": None,
        "coach_domain": None,
        "coach_topic": None,
        "selected_course_id": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

    # ------------------------------------------------------
    # Routing
    # ------------------------------------------------------

    if st.session_state["selected_domain"] is None:

        show_domain_cards()

    else:

        show_domain_page(
            st.session_state["selected_domain"]
        )