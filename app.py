import streamlit as st

from database.init_db import initialize_database

from ui.auth import show_auth
from ui.dashboard import show_dashboard
from ui.learn import show_learn
from ui.coach import show_coach
from ui.quiz import show_quiz
from ui.progress import show_progress
from ui.prediction import show_prediction
from ui.profile import show_profile
from ui.about import show_about
from ui.admin_dashboard import show_admin_dashboard
from ui.admin_courses import show_admin_courses
from ui.admin_topics import show_admin_topics
from ui.admin_materials import show_admin_materials
from ui.admin_analytics import show_admin_analytics
from ui.learning_summary import show_learning_summary

initialize_database()

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Learning Companion",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# SESSION INITIALIZATION
# ==========================================================

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

if "admin_page" not in st.session_state:
    st.session_state["admin_page"] = "dashboard"

# ==========================================================
# ROUTER
# ==========================================================

if not st.session_state.get("logged_in", False):

    show_auth()
    st.stop()

else:

    user = st.session_state["user"]

    # ------------------------------------------------------
    # Admin Routing
    # ------------------------------------------------------

    if user["role"] == "admin":

        admin_routes = {

            "dashboard": show_admin_dashboard,

            "courses": show_admin_courses,

            "topics": show_admin_topics,

            "materials": show_admin_materials,

            "analytics": show_admin_analytics,

        }

        admin_page = st.session_state["admin_page"]

        admin_routes.get(
            admin_page,
            show_admin_dashboard,
        )()

    # ------------------------------------------------------
    # Learner Routing
    # ------------------------------------------------------

    else:

        routes = {

            "dashboard": show_dashboard,

            "learn": show_learn,

            "coach": show_coach,

            "quiz": show_quiz,

            "summary": show_learning_summary,

            "progress": show_progress,

            "prediction": show_prediction,

            "profile": show_profile,

            "about": show_about,

        }

        page = st.session_state["page"]

        routes.get(
            page,
            show_dashboard,
        )()