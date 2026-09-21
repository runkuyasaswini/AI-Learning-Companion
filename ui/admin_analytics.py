import streamlit as st
import pandas as pd
import plotly.express as px

from ui.admin_sidebar import show_admin_sidebar

from services.admin_analytics_service import (
    AdminAnalyticsService,
)


def show_admin_analytics():

    show_admin_sidebar()

    summary = AdminAnalyticsService.get_platform_summary()

    st.title("📊 Platform Analytics")

    st.caption(
        "Real-time insights into learner engagement and platform usage."
    )

    st.divider()

    # ======================================================
    # KPI CARDS
    # ======================================================

    row1 = st.columns(4)

    with row1[0]:
        st.metric(
            "👥 Learners",
            summary["users"],
        )

    with row1[1]:
        st.metric(
            "📚 Courses",
            summary["courses"],
        )

    with row1[2]:
        st.metric(
            "📖 Topics",
            summary["topics"],
        )

    with row1[3]:
        st.metric(
            "📄 Materials",
            summary["materials"],
        )

    row2 = st.columns(4)

    with row2[0]:
        st.metric(
            "📝 Quiz Attempts",
            summary["quiz_attempts"],
        )

    with row2[1]:
        st.metric(
            "⭐ Average Score",
            f"{summary['average_score']}%",
        )

    with row2[2]:
        st.metric(
            "🎯 Topics Completed",
            summary["completed_topics"],
        )

    with row2[3]:
        st.metric(
            "🔥 Active Learners",
            summary["users"],
        )

    st.divider()

    # ======================================================
    # CHARTS
    # ======================================================

    left, right = st.columns(2)

    # ------------------------------------------------------

    with left:

        st.subheader("📈 Course Popularity")

        course_data = AdminAnalyticsService.get_course_popularity()

        if course_data:

            df = pd.DataFrame(course_data)

            fig = px.bar(
                df,
                x="domain",
                y="learners",
                text="learners",
                title="Learners by Course",
            )

            fig.update_layout(
                height=420,
                xaxis_title="Course",
                yaxis_title="Learners",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No learning activity available."
            )

    # ------------------------------------------------------

    with right:

        st.subheader("🥧 Quiz Performance")

        distribution = (
            AdminAnalyticsService.get_quiz_distribution()
        )

        pie = pd.DataFrame(
            {
                "Category": list(distribution.keys()),
                "Count": list(distribution.values()),
            }
        )

        fig = px.pie(
            pie,
            names="Category",
            values="Count",
            hole=0.55,
        )

        fig.update_layout(
            height=420,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()

    # ======================================================
    # TOPICS + LEARNERS
    # ======================================================

    left, right = st.columns(2)

    # ------------------------------------------------------

    with left:

        st.subheader("📚 Most Learned Topics")

        topics = (
            AdminAnalyticsService.get_popular_topics()
        )

        if topics:

            df = pd.DataFrame(topics)

            fig = px.bar(
                df,
                x="completed",
                y="topic",
                orientation="h",
                text="completed",
            )

            fig.update_layout(
                height=420,
                xaxis_title="Completions",
                yaxis_title="Topic",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No learning history available."
            )

    # ------------------------------------------------------

    with right:

        st.subheader("🏆 Top Learners")

        learners = (
            AdminAnalyticsService.get_top_learners()
        )

        if learners:

            st.dataframe(
                pd.DataFrame(learners),
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No learner data available."
            )

    st.divider()

    # ======================================================
    # WEAK TOPICS + PLATFORM INSIGHTS
    # ======================================================

    left, right = st.columns(2)

    # ------------------------------------------------------

    with left:

        st.subheader("⚠ Weak Topics")

        weak = (
            AdminAnalyticsService.get_weak_topics()
        )

        if weak:

            st.dataframe(
                pd.DataFrame(weak),
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No quiz history available."
            )

    # ------------------------------------------------------

    with right:

        st.subheader("🤖 Platform Insights")

        st.info(
            f"""
👥 **Learners:** {summary['users']}

📚 **Courses:** {summary['courses']}

📖 **Topics:** {summary['topics']}

📄 **Materials:** {summary['materials']}

📝 **Quiz Attempts:** {summary['quiz_attempts']}

⭐ **Average Quiz Score:** {summary['average_score']}%
"""
        )

        if summary["average_score"] >= 80:

            st.success(
                "Excellent learner performance across the platform."
            )

        elif summary["average_score"] >= 60:

            st.warning(
                "Learner performance is satisfactory with room for improvement."
            )

        else:

            st.error(
                "Average quiz performance is currently low."
            )