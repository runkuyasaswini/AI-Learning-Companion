import streamlit as st
import pandas as pd
import plotly.express as px

from ui.sidebar import show_sidebar
from services.progress_service import ProgressService
from utils.streak_calendar import render_streak_calendar
from datetime import date, timedelta


# ==========================================================
# LEARNING PROGRESS
# ==========================================================

def show_progress():

    show_sidebar()

    st.title("📈 Learning Progress Dashboard")

    st.caption(
        "Track your learning journey, quiz performance and overall progress."
    )

    st.divider()

    user = st.session_state["user"]

    stats = ProgressService.get_learning_statistics(
        user["id"]
    )

    streak = stats["learning_streak"]

    st.subheader("🔥 Learning Streak")

    streak = stats["learning_streak"]

    left, right = st.columns(2)

    with left:

        st.metric(
            "🔥 Current Streak",
            f"{streak['current_streak']} Days",
        )

    with right:

        st.metric(
            "🏆 Longest Streak",
            f"{streak['longest_streak']} Days",
        )

    st.caption("Learning Activity (Last 4 Weeks)")

    active_dates = {
        d.strftime("%Y-%m-%d")
        for d in streak["dates"]
    }

    today = date.today()

    start = today - timedelta(days=27)

    weekdays = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    header = st.columns(8)

    header[0].markdown("**Week**")

    for i, day in enumerate(weekdays):

        header[i + 1].markdown(f"**{day}**")

    for week in range(4):

        cols = st.columns(8)

        cols[0].markdown(f"**{week + 1}**")

        for day in range(7):

            current = start + timedelta(days=week * 7 + day)

            if current.strftime("%Y-%m-%d") in active_dates:

                cols[day + 1].success(" ")

            else:

                cols[day + 1].info(" ")

    st.info(
        "💡 Complete at least one lesson every day to maintain your learning streak."
    )

    st.divider()
    # ======================================================
    # KPI CARDS
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Topics Completed",
            stats["completed_topics"],
        )

    with col2:

        st.metric(
            "📝 Quiz Average",
            f"{stats['average_quiz_score']}%",
        )

    with col3:

        st.metric(
            "🎯 Quiz Attempts",
            stats["quiz_attempts"],
        )

    with col4:

        st.metric(
            "📖 Courses Covered",
            len(stats["domain_progress"]),
        )

    st.divider()

    # ======================================================
    # CHARTS
    # ======================================================

    left, right = st.columns(2)

    # ------------------------------------------------------

    with left:

        st.subheader("📚 Course Progress")

        if stats["domain_progress"]:

            df = pd.DataFrame(
                [
                    dict(row)
                    for row in stats["domain_progress"]
                ]
            )

            fig = px.bar(
                df,
                x="completed",
                y="domain",
                orientation="h",
                text="completed",
            )

            fig.update_layout(
                height=420,
                xaxis_title="Topics Completed",
                yaxis_title="Course",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No learning progress yet."
            )

    # ------------------------------------------------------

    with right:

        st.subheader("📈 Quiz Performance Trend")

        history = stats["quiz_history"]

        if history:

            df = pd.DataFrame(
                [
                    dict(row)
                    for row in history
                ]
            )

            df["Attempt"] = range(
                1,
                len(df) + 1,
            )

            fig = px.line(
                df,
                x="Attempt",
                y="percentage",
                markers=True,
            )

            fig.update_layout(
                height=420,
                xaxis_title="Quiz Attempt",
                yaxis_title="Score (%)",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No quiz attempts yet."
            )

    st.divider()

    # ======================================================
    # DISTRIBUTION + INSIGHTS
    # ======================================================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🥧 Learning Distribution"
        )

        distribution = stats[
            "learning_distribution"
        ]

        if distribution:

            df = pd.DataFrame(
                [
                    dict(row)
                    for row in distribution
                ]
            )

            fig = px.pie(
                df,
                names="domain",
                values="completed",
                hole=0.55,
            )

            fig.update_layout(
                height=420,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No completed topics."
            )

    # ------------------------------------------------------

    with right:

        st.subheader(
            "🏆 Learning Insights"
        )

        insights = stats[
            "learning_insights"
        ]

        with st.container(border=True):

            st.metric(
                "🏅 Strongest Course",
                insights["strongest"],
            )

            st.metric(
                "🎯 Needs More Practice",
                insights["needs_focus"],
            )

            st.info(
                "Keep practicing consistently to improve your overall learning performance."
            )

    st.divider()

    # ======================================================
    # RECENT ACTIVITY
    # ======================================================

    st.subheader(
        "🕒 Recent Learning Activity"
    )

    if stats["recent_learning"]:

        history = []

        for row in stats["recent_learning"]:

            history.append(

                {

                    "Course": row["domain"],

                    "Topic": row["topic"],

                    "Completed At": row["completed_at"],

                }

            )

        st.dataframe(

            history,

            hide_index=True,

            use_container_width=True,

        )

    else:

        st.info(
            "No learning activity yet."
        )