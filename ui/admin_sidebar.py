import streamlit as st

from services.auth_service import AuthService


def navigate(page):

    st.session_state["admin_page"] = page

    st.rerun()


def logout():

    AuthService.logout()

    keys = list(st.session_state.keys())

    for key in keys:

        del st.session_state[key]

    st.rerun()


def show_admin_sidebar():

    with st.sidebar:

        st.title("🛠️ Admin Panel")

        user = st.session_state["user"]

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
            "📚 Courses",
            use_container_width=True,
        ):
            navigate("courses")

        if st.button(
            "📖 Topics",
            use_container_width=True,
        ):
            navigate("topics")

        if st.button(
            "📄 Learning Materials",
            use_container_width=True,
        ):
            navigate("materials")

        if st.button(
            "📊 Analytics",
            use_container_width=True,
        ):
            navigate("analytics")

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            logout()