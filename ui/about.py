import streamlit as st

from ui.sidebar import show_sidebar


def show_about():

    show_sidebar()

    st.title("🚀 About AI Learning Companion")

    st.caption(
        "An AI-powered personalized learning platform for adaptive education."
    )

    st.divider()

    # ==================================================
    # PLATFORM OVERVIEW
    # ==================================================

    st.subheader("🌟 Platform Overview")

    st.write(
        """
AI Learning Companion is an intelligent learning platform that combines
Artificial Intelligence, Retrieval-Augmented Generation (RAG), and
Machine Learning to deliver personalized learning experiences.

Instead of simply displaying learning material, the platform guides
learners through courses, quizzes, AI mentoring, progress tracking,
and personalized recommendations.
"""
    )

    st.divider()

    # ==================================================
    # FEATURES
    # ==================================================

    st.subheader("✨ Key Features")

    col1, col2 = st.columns(2)

    with col1:

        st.success("📚 Dynamic Course Management")

        st.success("📖 AI-Powered Learning")

        st.success("💬 Personalized AI Coach")

        st.success("📝 Adaptive Quiz Generation")

        st.success("📈 Progress Tracking")

    with col2:

        st.success("🤖 Learning Prediction")

        st.success("📊 Learner Analytics")

        st.success("🗂 Knowledge Base Builder")

        st.success("🔍 RAG-based Retrieval")

        st.success("👨‍💼 Admin Management Portal")

    st.divider()

    # ==================================================
    # LEARNING WORKFLOW
    # ==================================================

    st.subheader("🧠 Learning Workflow")

    st.info(
        """
Course

⬇

Topic

⬇

Learn with AI

⬇

Take Quiz

⬇

Ask AI Coach

⬇

Track Progress

⬇

Predict Performance
"""
    )

    st.divider()

    # ==================================================
    # AI CAPABILITIES
    # ==================================================

    st.subheader("🤖 AI Capabilities")

    st.write(
        """
• Retrieval-Augmented Generation (RAG)

• Context-aware AI tutoring

• Personalized mentoring

• Dynamic quiz generation

• Learning recommendations

• Course-specific knowledge retrieval
"""
    )

    st.divider()

    # ==================================================
    # TECHNOLOGY STACK
    # ==================================================

    st.subheader("🛠 Technology Stack")

    tech1, tech2, tech3 = st.columns(3)

    with tech1:

        st.markdown("""
### Backend

- Python
- Streamlit
- SQLite
- Pandas
""")

    with tech2:

        st.markdown("""
### AI & ML

- LangChain
- FAISS
- Sentence Transformers
- OpenAI Compatible LLM
""")

    with tech3:

        st.markdown("""
### Features

- RAG
- Personalized AI Coach
- Adaptive Learning
- Quiz Generator
""")

    st.divider()

    # ==================================================
    # FUTURE ROADMAP
    # ==================================================

    st.subheader("🚀 Future Roadmap")

    roadmap = [

        "🎯 Adaptive Learning Paths",

        "🎙 Voice-based AI Tutor",

        "🏆 Certificates & Badges",

        "🃏 AI Flashcards",

        "💻 Coding Practice Playground",

        "📱 Mobile Responsive Interface",

        "📚 Multi-language Learning Support",

        "🤝 Collaborative Learning",

    ]

    for item in roadmap:

        st.write(item)

    st.divider()

    # ==================================================
    # FOOTER
    # ==================================================

    st.caption(
        "AI Learning Companion • Built using Artificial Intelligence, Retrieval-Augmented Generation (RAG), and Machine Learning."
    )