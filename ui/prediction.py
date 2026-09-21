import streamlit as st

from ui.sidebar import show_sidebar

from services.prediction_service import (
    get_learning_prediction,
)


def show_prediction():

    show_sidebar()


    st.title(
        "🤖 Learning Performance Prediction"
    )


    st.caption(
        "AI model predicts your probability of scoring 70%+ in your next quiz."
    )


    user_id = st.session_state["user"]["id"]


    if st.button(
        "🔮 Predict My Performance",
        use_container_width=True,
    ):


        with st.spinner(
            "Analyzing your learning pattern..."
        ):

            result = get_learning_prediction(
                user_id
            )


        st.divider()


        # --------------------------------------------------
        # Probability
        # --------------------------------------------------

        st.metric(
            "Probability of Passing Next Quiz",
            f"{result['probability']}%",
        )


        # --------------------------------------------------
        # Prediction
        # --------------------------------------------------

        if result["prediction"] == "Likely to Pass":

            st.success(
                "✅ Likely to Pass"
            )

        else:

            st.warning(
                "📚 Needs More Practice"
            )


        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        st.info(
            f"Model Confidence: **{result['confidence']}**"
        )


        st.divider()


        st.subheader(
            "💡 Recommendation"
        )


        if result["prediction"] == "Likely to Pass":

            st.write(
                """
You are showing good learning progress.

You can attempt the next quiz and continue to a more advanced topic.
"""
            )

        else:

            st.write(
                """
Consider revising completed topics and practicing more before attempting a difficult quiz.
"""
            )