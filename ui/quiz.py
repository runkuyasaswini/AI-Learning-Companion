import streamlit as st

from ui.sidebar import show_sidebar

from services.quiz_service import (
    create_quiz,
    submit_quiz,
    get_quiz_history,
)
from services.course_service import (
    get_all_courses,
)

from services.topic_service import (
    get_topics_by_course,
)

# ==========================================================
# RESET QUIZ STATE
# ==========================================================

def reset_quiz_state():

    keys = [
        "quiz_questions",
        "quiz_answers",
        "current_question",
        "quiz_result",
        "quiz_stage",
        "quiz_submitted",
    ]

    for key in keys:

        st.session_state.pop(
            key,
            None,
        )

# ==========================================================
# SESSION INITIALIZATION
# ==========================================================

def initialize_quiz_session():

    defaults = {
        "quiz_domain": None,
        "quiz_topic": None,
        "quiz_difficulty": "Medium",
        "quiz_question_count": 10,
        "quiz_questions": [],
        "quiz_answers": {},
        "current_question": 0,
        "quiz_submitted": False,
        "quiz_result": None,
        "quiz_stage": "setup",
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==========================================================
# QUIZ SETUP
# ==========================================================

def show_quiz_setup():

    st.title("📝 AI Quiz")

    st.caption(
        "Generate an AI-powered quiz based on your learning."
    )

    st.divider()

    # ------------------------------------------------------

    domain = st.session_state.get("quiz_domain")
    topic = st.session_state.get("quiz_topic")

    # -----------------------------------------
    # Opened from Sidebar
    # -----------------------------------------

    if not domain:

        courses = get_all_courses()

        course_names = [
            course["course_name"]
            for course in courses
        ]

        domain = st.selectbox(
            "Select Course",
            course_names,
        )

        selected_course = next(
            course
            for course in courses
            if course["course_name"] == domain
        )

        topics = get_topics_by_course(
            selected_course["id"]
        )

        topic_names = [
            topic["topic_name"]
            for topic in topics
        ]

        topic = st.selectbox(
            "Select Topic",
            topic_names,
        )

    # -----------------------------------------
    # Opened from Learn Page
    # -----------------------------------------

    else:

        st.success(
            f"📚 Course : {domain}"
        )

        st.success(
            f"📖 Topic : {topic}"
        )
    st.divider()

    # ------------------------------------------------------
    # Difficulty
    # ------------------------------------------------------

    difficulty = st.radio(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard",
        ],
        horizontal=True,
        index=1,
    )

    st.session_state["quiz_difficulty"] = difficulty

    # ------------------------------------------------------
    # Question Count
    # ------------------------------------------------------

    question_count = st.selectbox(
        "Number of Questions",
        [
            5,
            10,
            15,
        ],
        index=1,
    )

    st.session_state["quiz_question_count"] = question_count

    st.divider()

    # ------------------------------------------------------
    # Generate
    # ------------------------------------------------------

    if st.button(
        "🚀 Generate Quiz",
        use_container_width=True,
    ):
        
        reset_quiz_state()

        with st.spinner(
            "Generating quiz..."
        ):

            quiz = create_quiz(
                topic=topic,
                difficulty=difficulty,
                total_questions=question_count,
                course=domain,
            )

        # --------------------------------------------------
        # Handle Quiz Generation Errors
        # --------------------------------------------------

        if isinstance(quiz, dict) and "error" in quiz:

            st.warning(
                quiz["error"]
            )

            return


        if not quiz:

            st.error(
                "Unable to generate quiz."
            )

            return


        st.session_state["quiz_questions"] = quiz
        st.session_state["quiz_answers"] = {}
        st.session_state["current_question"] = 0
        
        st.session_state["quiz_domain"] = domain
        st.session_state["quiz_topic"] = topic

        st.session_state["quiz_stage"] = "questions"

        st.rerun()


# ==========================================================
# QUESTION SCREEN
# ==========================================================

def show_question_screen():

    questions = st.session_state["quiz_questions"]

    current = st.session_state["current_question"]

    question = questions[current]

    total = len(questions)

    st.title("📝 AI Quiz")

    st.progress(
        (current + 1) / total
    )

    st.write(
        f"### Question {current + 1} of {total}"
    )

    st.divider()

    st.markdown(
        f"### {question['question']}"
    )

    options = question["options"]

    previous_answer = st.session_state["quiz_answers"].get(
        current,
        None,
    )

    selected = st.radio(
        "Choose an answer",
        options,
        index=(
            options.index(previous_answer)
            if previous_answer in options
            else None
        ),
        key=f"question_{current}",
    )

    st.session_state["quiz_answers"][current] = selected

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if current > 0:

            if st.button(
                "⬅ Previous",
                use_container_width=True,
            ):

                st.session_state["current_question"] -= 1

                st.rerun()

    with col2:

        if current < total - 1:

            if st.button(
                "Next ➡",
                use_container_width=True,
            ):

                st.session_state["current_question"] += 1

                st.rerun()

        else:

            if st.button(
                "Review Answers",
                use_container_width=True,
            ):

                st.session_state["quiz_stage"] = "review"

                st.rerun()

# ==========================================================
# REVIEW SCREEN
# ==========================================================

def show_review_screen():

    questions = st.session_state["quiz_questions"]
    answers = st.session_state["quiz_answers"]

    st.title("📝 Review Your Answers")

    st.caption(
        "Review your answers before submitting the quiz."
    )

    st.divider()

    # ------------------------------------------------------

    for index, question in enumerate(questions):

        answered = index in answers

        status = (
            "🟢 Answered"
            if answered
            else "🔴 Not Answered"
        )

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write(
                f"**Question {index + 1}** — {status}"
            )

        with col2:

            if st.button(
                "Open",
                key=f"review_{index}",
            ):

                st.session_state["current_question"] = index
                st.session_state["quiz_stage"] = "questions"

                st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back to Quiz",
            use_container_width=True,
        ):

            st.session_state["quiz_stage"] = "questions"

            st.rerun()

    with col2:

        if st.button(
            "✅ Submit Quiz",
            use_container_width=True,
        ):

            user = st.session_state["user"]

            result = submit_quiz(
                user_id=user["id"],
                domain=st.session_state["quiz_domain"],
                topic=st.session_state["quiz_topic"],
                difficulty=st.session_state["quiz_difficulty"],
                quiz=st.session_state["quiz_questions"],
                user_answers=st.session_state["quiz_answers"],
            )

            st.session_state["quiz_result"] = result
            st.session_state["quiz_stage"] = "result"

            st.rerun()
# ==========================================================
# RESULT SCREEN
# ==========================================================

def show_result_screen():

    result = st.session_state["quiz_result"]

    score = result["score"]
    total = result["total_questions"]
    percentage = result["percentage"]

    st.title("🎉 Quiz Completed")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Score",
            f"{score}/{total}",
        )

    with col2:

        st.metric(
            "Percentage",
            f"{percentage:.1f}%",
        )

    with col3:

        if percentage >= 90:

            performance = (
                "🌟 Excellent!\n\n"
                "Outstanding understanding of this topic."
            )

        elif percentage >= 75:

            performance = (
                "🎉 Great Job!\n\n"
                "You understand most concepts well."
            )

        elif percentage >= 60:

            performance = (
                "👍 Good Effort!\n\n"
                "Review a few concepts and try again."
            )

        elif percentage >= 40:

            performance = (
                "📘 Needs Practice\n\n"
                "Spend more time with the lesson before retrying."
            )

        else:

            performance = (
                "💡 Review the Lesson\n\n"
                "Go through the learning material again before attempting another quiz."
            )
            
        st.success(performance)

    st.divider()

    st.subheader("📋 Question Review")

    for index, question in enumerate(result["results"]):

        icon = "✅" if question["is_correct"] else "❌"

        with st.expander(
            f"{icon} Question {index + 1}"
        ):

            st.write(
                f"**Question**"
            )

            st.write(question["question"])

            st.write(
                f"**Your Answer:** {question['selected']}"
            )

            st.write(
                f"**Correct Answer:** {question['correct']}"
            )

            st.write(
                f"**Explanation:**"
            )

            st.info(
                question["explanation"]
            )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Retake Quiz",
            use_container_width=True,
        ):

            st.session_state["quiz_questions"] = []
            st.session_state["quiz_answers"] = {}
            st.session_state["quiz_result"] = None
            st.session_state["current_question"] = 0
            st.session_state["quiz_stage"] = "setup"

            st.rerun()

    with col2:

        if st.button(
            "📚 Return to Learn",
            use_container_width=True,
        ):

            st.session_state["quiz_questions"] = []
            st.session_state["quiz_answers"] = {}
            st.session_state["quiz_result"] = None
            st.session_state["current_question"] = 0
            st.session_state["quiz_stage"] = "setup"

            st.session_state["page"] = "learn"

            st.rerun()


# ==========================================================
# MAIN PAGE
# ==========================================================

def show_quiz():

    show_sidebar()

    initialize_quiz_session()

    stage = st.session_state.get(
    "quiz_stage",
    "setup",
    )

    if stage == "setup":

        show_quiz_setup()

    elif stage == "questions":

        show_question_screen()

    elif stage == "review":

        show_review_screen()

    elif stage == "result":

        show_result_screen()

    # ==========================================================
    # QUIZ HISTORY
    # ==========================================================

    st.divider()

    st.subheader("📊 Recent Quiz History")

    user_id = st.session_state["user"]["id"]

    history = get_quiz_history(
        user_id,
        limit=10,
    )


    if history:

        history_data = []

        for row in history:

            history_data.append(
                {
                    "Course": row["domain"],
                    "Topic": row["topic"],
                    "Difficulty": row["difficulty"],
                    "Score": (
                        f"{row['score']}/"
                        f"{row['total_questions']}"
                    ),
                    "Percentage": (
                        f"{row['percentage']}%"
                    ),
                    "Date": row["attempted_at"],
                }
            )


        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True,
        )


    else:

        st.info(
            "No quiz attempts yet. Start your first quiz!"
        )