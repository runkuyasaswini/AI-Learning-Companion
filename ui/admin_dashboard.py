import streamlit as st

from ui.admin_sidebar import show_admin_sidebar

from services.admin_analytics_service import (
    AdminAnalyticsService,
)


def show_admin_dashboard():

    show_admin_sidebar()

    summary = AdminAnalyticsService.get_platform_summary()

    st.title("🛠️ Admin Dashboard")

    st.caption(
        "Manage courses, learning content, learners and platform analytics."
    )

    st.divider()

    # =====================================================
    # WELCOME
    # =====================================================

    st.success(
        """
### Welcome to the AI Learning Companion Administration Panel 👋

From here you can manage the complete learning platform.

Use the quick actions below or navigate using the sidebar.
"""
    )

    st.divider()

    # =====================================================
    # PLATFORM OVERVIEW
    # =====================================================

    st.subheader("📊 Platform Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Learners",
            summary["users"],
        )

    with col2:
        st.metric(
            "📚 Courses",
            summary["courses"],
        )

    with col3:
        st.metric(
            "📖 Topics",
            summary["topics"],
        )

    with col4:
        st.metric(
            "📄 Materials",
            summary["materials"],
        )

    st.divider()

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.subheader("⚡ Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📚 Manage Courses",
            use_container_width=True,
        ):
            st.session_state["admin_page"] = "courses"
            st.rerun()

        if st.button(
            "📖 Manage Topics",
            use_container_width=True,
        ):
            st.session_state["admin_page"] = "topics"
            st.rerun()

    with col2:

        if st.button(
            "📄 Learning Materials",
            use_container_width=True,
        ):
            st.session_state["admin_page"] = "materials"
            st.rerun()

        if st.button(
            "📊 View Analytics",
            use_container_width=True,
        ):
            st.session_state["admin_page"] = "analytics"
            st.rerun()

    st.divider()

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    st.subheader("⚙️ System Status")

    left, right = st.columns(2)

    with left:

        st.success("🟢 Database Connected")

        st.success("🟢 AI Services Available")

        st.success("🟢 Knowledge Base Ready")

    with right:

        st.info(
            f"""
**Quiz Attempts:** {summary["quiz_attempts"]}

**Topics Completed:** {summary["completed_topics"]}

**Average Quiz Score:** {summary["average_score"]}%
"""
        )

    st.divider()

    # =====================================================
    # ADMIN RESPONSIBILITIES
    # =====================================================

    st.subheader("🎯 Administration Modules")

    st.markdown("""
- 📚 Create and manage courses
- 📖 Organize learning topics
- 📄 Upload learning materials
- 🧠 Build course knowledge bases
- 📊 Monitor learner analytics
- 🤖 Maintain AI-powered learning resources
""")