import streamlit as st

from services.auth_service import AuthService


def show_login():
    """
    Render the login page.
    """

    st.title("🎓 AI Learning Companion")

    st.subheader("Login")

    username = st.text_input(
        "Username",
        placeholder="Enter your username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if not username or not password:

            st.warning("Please enter both username and password.")

            return

        success, result = AuthService.login(
            username=username,
            password=password
        )

        if success:

            st.session_state["logged_in"] = True
            st.session_state["user"] = result

            st.rerun()

        else:

            st.error(result)