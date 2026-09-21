import streamlit as st

from ui.sidebar import show_sidebar

from services.coach_service import (
    get_coach_response,
)

# ==========================================================
# SESSION INITIALIZATION
# ==========================================================

def initialize_coach_session():

    defaults = {
        "coach_messages": [],
        "coach_topic": None,
        "coach_initialized": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

# ==========================================================
# SEND MESSAGE
# ==========================================================

def process_message(question):
    """
    Send a user question to the AI Coach
    and store the conversation.
    """

    user = st.session_state["user"]

    # ------------------------------------------------------
    # Store User Message
    # ------------------------------------------------------

    st.session_state["coach_messages"].append(
        {
            "role": "user",
            "content": question,
        }
    )

    # ------------------------------------------------------
    # Generate AI Response
    # ------------------------------------------------------

    with st.spinner("AI Coach is thinking..."):

        response = get_coach_response(
            user_id=user["id"],
            question=question,
            course=st.session_state.get("coach_domain"),
        )

    # ------------------------------------------------------
    # Store Assistant Message
    # ------------------------------------------------------

    st.session_state["coach_messages"].append(
        {
            "role": "assistant",
            "content": response["answer"],
        }
    )


# ==========================================================
# INITIALIZE COACH CONTEXT
# ==========================================================

def initialize_coach_context():

    if st.session_state.get("coach_initialized", False):
        return

    topic = st.session_state.get("coach_topic")

    if topic:

        welcome = (
            f"Let's discuss **{topic}**.\n\n"
            "Ask me anything about this topic, "
            "or I'll help you revise it step by step."
        )

    else:

        welcome = (
            "Hello! 👋\n\n"
            "I'm your AI Learning Mentor.\n\n"
            "Ask me anything about your learning journey."
        )

    st.session_state["coach_messages"].append(
        {
            "role": "assistant",
            "content": welcome,
        }
    )

    st.session_state["coach_initialized"] = True

# ==========================================================
# MAIN PAGE
# ==========================================================

def show_coach():

    show_sidebar()

    initialize_coach_session()

    initialize_coach_context()

    user = st.session_state["user"]

    st.title("💬 AI Learning Mentor")

    st.info(
        f"""
    ### Welcome back, {user['full_name']} 👋

    I'm your personal AI Learning Mentor.

    I can help you:

    - 📚 Explain difficult concepts
    - 📝 Prepare for quizzes
    - 🎯 Recommend what to study next
    - 📈 Help improve your learning journey
    """
    )

    st.divider()

    col1, col2 = st.columns([5, 1])
    
    with col2:

        if st.button(
            "🗑 Clear Chat",
            use_container_width=True,
        ):

            st.session_state["coach_messages"] = []
            st.session_state["coach_initialized"] = False
            st.session_state["coach_topic"] = None
            st.session_state["coach_domain"] = None

            st.rerun()

    st.divider()

    st.subheader("🚀 Suggested Questions")

    suggestions = [
        "What should I learn next?",
        "Revise my recent topics.",
        "Help me prepare for my next quiz.",
        "Explain my weakest concepts.",
    ]

    cols = st.columns(2)

    for index, suggestion in enumerate(suggestions):

        with cols[index % 2]:

            if st.button(
                suggestion,
                key=f"suggestion_{index}",
                use_container_width=True,
            ):

                process_message(suggestion)

                st.rerun()

    st.divider()

    st.subheader("💬 Conversation")

    if not st.session_state["coach_messages"]:

        st.info(
            "Start a conversation with your AI Learning Mentor."
        )

    else:

        for message in st.session_state["coach_messages"]:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

    question = st.chat_input(
        "Ask your AI Learning Mentor..."
    )

    if question:

        process_message(question)

        st.rerun()