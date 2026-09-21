import streamlit as st

from services.auth_service import AuthService


def initialize_session():

    defaults = {
        "logged_in": False,
        "user_id": None,
        "username": None,
        "full_name": None,
        "email": None,
        "user": None,
        "auth_mode": "login"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def show_auth():

    initialize_session()

    left, right = st.columns([1.2, 1])

    # ---------------------------------------------------
    # LEFT PANEL
    # ---------------------------------------------------

    with left:

        st.title("🤖 AI Learning Companion")

        st.markdown(
            """
Your Personalized AI Tutor

Learn and master:

- 📚 Machine Learning
- 🧠 Natural Language Processing
- 🤖 Generative AI
- ⚙️ MLOps
- 🚀 Agentic AI

Features:

- AI-powered Learning
- Smart Quizzes
- Progress Tracking
- AI Coach
- Learning Prediction
            """
        )

    # ---------------------------------------------------
    # RIGHT PANEL
    # ---------------------------------------------------

    with right:

        if st.session_state.auth_mode == "login":
            show_login()

        else:
            show_register()

def show_login():

    st.subheader("Login")

    username = st.text_input(
        "Username or Email",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        success, result = AuthService.authenticate_user(
            username,
            password
        )

        if success:

            print("\n========== LOGIN SUCCESS ==========")
            print(result)
            print("===================================\n")

            st.session_state.logged_in = True
            st.session_state.user_id = result["id"]
            st.session_state.username = result["username"]
            st.session_state.full_name = result["full_name"]
            st.session_state.email = result["email"]

            # Backward compatibility
            st.session_state["user"] = result

            # Clear login fields
            st.session_state.pop("login_username", None)
            st.session_state.pop("login_password", None)

            st.success("Login successful!")

            st.rerun()
        else:
            print("\n========== LOGIN FAILED ==========")
            print(result)
            print("=================================\n")

            st.error(result)

    st.markdown("---")

    st.write("New user?")

    if st.button(
        "Create Account",
        use_container_width=True
    ):

        # Clear login fields before switching
        st.session_state.pop("login_username", None)
        st.session_state.pop("login_password", None)

        st.session_state.auth_mode = "register"
        st.rerun()

def show_register():

    st.subheader("Create Account")

    full_name = st.text_input(
        "Full Name",
        key="register_fullname"
    )

    username = st.text_input(
        "Username",
        key="register_username"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="register_confirm_password"
    )

    if st.button(
        "Create Account",
        use_container_width=True
    ):

        if not all([
            full_name,
            username,
            email,
            password,
            confirm_password
        ]):

            st.error("Please fill all fields.")
            return

        if password != confirm_password:

            st.error("Passwords do not match.")
            return

        success, message = AuthService.register_user(
            username=username,
            password=password,
            full_name=full_name,
            email=email
        )

        if success:

            st.success("🎉 Account created successfully!")
            st.info("Please login using your new credentials.")

            # Clear registration fields
            for key in [
                "register_fullname",
                "register_username",
                "register_email",
                "register_password",
                "register_confirm_password",
            ]:
                st.session_state.pop(key, None)

            # Clear login fields
            st.session_state.pop("login_username", None)
            st.session_state.pop("login_password", None)

            st.session_state.auth_mode = "login"

            st.rerun()

        else:

            st.error(message)

    st.markdown("---")

    st.write("Already have an account?")

    if st.button(
        "Back to Login",
        use_container_width=True
    ):

        # Clear registration fields
        for key in [
            "register_fullname",
            "register_username",
            "register_email",
            "register_password",
            "register_confirm_password",
        ]:
            st.session_state.pop(key, None)

        st.session_state.auth_mode = "login"

        st.rerun()