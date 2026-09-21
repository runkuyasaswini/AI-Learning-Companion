import streamlit as st

from ui.sidebar import show_sidebar

from services.progress_service import ProgressService


def show_profile():

    show_sidebar()

    user = st.session_state["user"]

    stats = ProgressService.get_learning_statistics(
        user["id"]
    )

    st.title("👤 My Profile")

    st.caption(
        "Track your learning journey and achievements."
    )

    st.divider()

    # ==================================================
    # USER INFORMATION
    # ==================================================

    left, right = st.columns([1, 3])

    with left:

        st.markdown("# 👤")

    with right:

        st.subheader(user["full_name"])

        st.write(f"**Email:** {user['email']}")

        st.write(f"**Role:** {user['role'].title()}")

    st.divider()

    # ==================================================
    # LEARNING SUMMARY
    # ==================================================

    st.subheader("📊 Learning Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Topics",
            stats["completed_topics"],
        )

    with col2:

        st.metric(
            "📝 Quizzes",
            stats["quiz_count"],
        )

    with col3:

        st.metric(
            "⭐ Average",
            f"{stats['average_quiz_score']}%",
        )

    with col4:

        st.metric(
            "🔥 Streak",
            f"{stats['learning_streak']} Days",
        )

    st.divider()

    # ==================================================
    # OVERALL PROGRESS
    # ==================================================

    st.subheader("📈 Overall Progress")

    st.progress(
        stats["overall_progress"] / 100
    )

    st.caption(
        f"{stats['overall_progress']}% of your learning journey completed."
    )

    st.divider()

    # ==================================================
    # STARTED COURSES
    # ==================================================

    st.subheader("📚 Started Courses")

    if stats["domain_progress"]:

        for row in stats["domain_progress"]:

            with st.container(border=True):

                st.markdown(
                    f"### 📖 {row['domain']}"
                )

                st.write(
                    f"Topics Completed: **{row['completed']}**"
                )

    else:

        st.info(
            "You haven't started any course yet."
        )

    st.divider()

    # ==================================================
    # ACHIEVEMENTS
    # ==================================================

    left, right = st.columns(2)

    with left:

        st.subheader("🏆 Achievements")

        if stats["achievements"]:

            for achievement in stats["achievements"]:

                st.success(achievement)

        else:

            st.info(
                "No achievements unlocked yet."
            )

    with right:

        st.subheader("🧠 Needs More Practice")

        if stats["weak_topics"]:

            for topic in stats["weak_topics"]:

                st.warning(
                    f"{topic['topic']} ({topic['avg_score']:.1f}%)"
                )

        else:

            st.success(
                "Excellent! No weak topics detected."
            )

    st.divider()

    # ==================================================
    # RECENT LEARNING
    # ==================================================

    st.subheader("🕒 Recent Learning")

    if stats["recent_learning"]:

        for row in stats["recent_learning"]:

            with st.container(border=True):

                st.markdown(
                    f"**{row['topic']}**"
                )

                st.caption(
                    f"{row['domain']} • {row['completed_at'][:10]}"
                )

    else:

        st.info(
            "No recent learning activity."
        )