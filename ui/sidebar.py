import streamlit as st


PAGES = {
    "dashboard": "🏠 Dashboard",
    "learn": "📚 Learn",
    "coach": "💬 AI Coach",
    "quiz": "📝 Quiz",
    "summary": "📄 Learning Summaries",
    "progress": "📈 Progress",
    "prediction": "🤖 Prediction",
    "profile": "👤 Profile",
    "about": "ℹ️ About",
}


def navigate(page):

    st.session_state["page"] = page

    st.rerun()


def logout():

    keys = list(st.session_state.keys())

    for key in keys:

        del st.session_state[key]

    st.rerun()


def show_sidebar():
    """
    Render learner sidebar.
    """

    user = st.session_state.get("user")

    if not user:
        return

    with st.sidebar:

        st.title("🎓 AI Learning Companion")

        st.success(
            f"Welcome,\n\n{user['full_name']}"
        )

        st.divider()

        # --------------------------------------------------

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):
            navigate("dashboard")

        if st.button(
            "📚 Learn",
            use_container_width=True,
        ):
            navigate("learn")

        if st.button(
            "💬 AI Coach",
            use_container_width=True,
        ):
            navigate("coach")

        if st.button(
            "📝 Quiz",
            use_container_width=True,
        ):
            navigate("quiz")

        if st.button(
            "📄 Learning Summaries",
            use_container_width=True,
        ):
            navigate("summary")

        if st.button(
            "📈 Progress",
            use_container_width=True,
        ):
            navigate("progress")

        if st.button(
            "🤖 Prediction",
            use_container_width=True,
        ):
            navigate("prediction")

        if st.button(
            "👤 Profile",
            use_container_width=True,
        ):
            navigate("profile")

        if st.button(
            "ℹ️ About",
            use_container_width=True,
        ):
            navigate("about")

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            logout()