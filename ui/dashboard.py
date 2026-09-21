import streamlit as st

from ui.sidebar import show_sidebar
from services.progress_service import ProgressService
from datetime import datetime

def get_greeting():

    hour = datetime.now().hour

    if hour < 12:
        return "🌅 Good Morning"

    elif hour < 17:
        return "☀️ Good Afternoon"

    return "🌙 Good Evening"

def show_dashboard():
    """
    Render the application dashboard.
    """

    show_sidebar()

    user = st.session_state["user"]

    stats = ProgressService.get_learning_statistics(user["id"])

    st.title("🎓 AI Learning Companion")

    st.subheader(
        f"{get_greeting()}, {user['full_name']}!"
    )

    st.caption(
        "Your personalized AI-powered learning journey starts here."
    )

    st.info(
        "💡 Stay consistent. Even 20 minutes of learning today is progress."
    )

    st.divider()

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🔥 Streak",
            f"{stats['learning_streak']['current_streak']} Days",
        )

    with col2:

        st.metric(
            "📚 Topics",
            stats["completed_topics"],
        )

    with col3:

        st.metric(
            "📝 Quizzes Taken",
            stats["quiz_attempts"],
        )

    with col4:

        st.metric(
            "⭐ Avg Score",
            f"{stats['average_quiz_score']}%",
        )

    st.divider()

    # --------------------------------------------------
    # Quick Actions
    # --------------------------------------------------

    st.subheader("🚀 Quick Actions")

        # --------------------------------------------------
    # Learning Overview
    # --------------------------------------------------

    left, right = st.columns([2, 3])

    # ==================================================
    # Overall Progress
    # ==================================================

    with left:

        st.subheader("📈 Overall Progress")

        st.progress(
            stats["overall_progress"] / 100
        )

        st.metric(
            "Completion",
            f"{stats['overall_progress']}%",
        )

    # ==================================================
    # Continue Learning
    # ==================================================

    with right:

        st.subheader("📚 Continue Learning")

        current = stats["current_learning"]

        if current:

            st.success(
                f"**Course:** {current['domain']}"
            )

            st.write(
                f"**Last Topic:** {current['topic']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "▶ Resume Learning",
                    use_container_width=True,
                ):

                    st.session_state["selected_domain"] = current["domain"]
                    st.session_state["search_topic"] = current["topic"]
                    st.session_state["page"] = "learn"

                    st.rerun()

            with col2:

                if st.button(
                    "💬 Ask AI Coach",
                    use_container_width=True,
                ):

                    st.session_state["coach_topic"] = current["topic"]
                    st.session_state["page"] = "coach"

                    st.rerun()

        else:

            st.info(
                "Start your first lesson to build your learning journey."
            )

    st.divider()
    st.divider()

    # --------------------------------------------------
    # Course Progress
    # --------------------------------------------------

    st.subheader("📊 Course Progress")

    course_progress = stats["domain_progress"]

    total_topics = stats["total_topics"]

    if course_progress:

        for row in course_progress:

            course = row["domain"]

            completed = row["completed"]

            total = total_topics.get(course, completed)

            percentage = (
                completed / total
                if total
                else 0
            )

            st.write(
                f"**{course}**"
            )

            st.progress(percentage)

            st.caption(
                f"{completed} of {total} topics completed"
            )

    else:

        st.info(
            "No course progress available yet."
        )

    st.divider()

    # --------------------------------------------------
    # AI Recommendation
    # --------------------------------------------------

    st.subheader("🎯 AI Recommended Next")

    current = stats["current_learning"]

    if current:

        st.success(
            f"""
    Continue strengthening **{current['domain']}**.

    Based on your recent activity,
    your next learning session should
    build upon **{current['topic']}**.
    """
        )

    else:

        st.info(
            """
    Start your first course.

    As you learn, personalized
    recommendations will appear here.
    """
        )

    st.divider()

    # --------------------------------------------------
    # Recent Activity & Achievements
    # --------------------------------------------------

    left, right = st.columns([2, 1])

    # ==================================================
    # Recent Activity
    # ==================================================

    with left:

        st.subheader("🕒 Recent Activity")

        if stats["recent_learning"]:

            for row in stats["recent_learning"]:

                with st.container(border=True):

                    col1, col2 = st.columns([4, 1])

                    with col1:

                        st.markdown(
                            f"**{row['topic']}**"
                        )

                        st.caption(
                            f"📚 {row['domain']}"
                        )

                    with col2:

                        st.caption(
                            row["completed_at"][:10]
                        )

        else:

            st.info(
                "No learning activity yet."
            )

    # ==================================================
    # Achievements
    # ==================================================

    with right:

        st.subheader("🏆 Achievements")

        if stats["achievements"]:

            for achievement in stats["achievements"]:

                st.success(achievement)

        else:

            st.info(
                "Complete lessons to unlock achievements."
            )

    st.divider()

    st.subheader("🧠 Learning Insights")

    weak_topics = stats["weak_topics"]

    if weak_topics:

        st.warning(
            "These topics need more practice."
        )

        for topic in weak_topics:

            st.write(
                f"• {topic['topic']} ({topic['avg_score']:.1f}%)"
            )

    else:

        st.success(
            "Excellent! No weak topics detected."
        )




