from database.db import get_connection

from ml.predictor import predict_performance


# ==========================================================
# BUILD USER FEATURES
# ==========================================================

def get_user_prediction_features(
    user_id,
):
    """
    Build ML features from application data.
    """


    conn = get_connection()

    cursor = conn.cursor()


    # ------------------------------------------------------
    # Learning History
    # ------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM learning_history
        WHERE user_id = ?
        """,
        (user_id,),
    )

    completed_topics = cursor.fetchone()[0]


    # ------------------------------------------------------
    # Quiz Statistics
    # ------------------------------------------------------

    cursor.execute(
        """
        SELECT
            COUNT(*),
            AVG(percentage)
        FROM quiz_history
        WHERE user_id = ?
        """,
        (user_id,),
    )

    quiz_data = cursor.fetchone()


    quizzes_attempted = quiz_data[0] or 0

    average_quiz_score = (
        round(
            quiz_data[1],
            2,
        )
        if quiz_data[1]
        else 50
    )


    conn.close()


    # ------------------------------------------------------
    # Derived Features
    # ------------------------------------------------------

    completion_percentage = min(
        completed_topics / 60 * 100,
        100,
    )


    # Current defaults
    # Will be replaced when activity tracking is added

    study_hours = max(
        completed_topics * 0.5,
        1,
    )


    revision_sessions = quizzes_attempted


    coach_interactions = 0


    learning_streak = min(
        completed_topics,
        30,
    )


    if average_quiz_score >= 75:

        improvement_trend = "Improving"

    elif average_quiz_score >= 50:

        improvement_trend = "Stable"

    else:

        improvement_trend = "Declining"


    return {

        "completed_topics":
            completed_topics,

        "quizzes_attempted":
            quizzes_attempted,

        "average_quiz_score":
            average_quiz_score,

        "learning_streak":
            learning_streak,

        "study_hours":
            study_hours,

        "completion_percentage":
            completion_percentage,

        "revision_sessions":
            revision_sessions,

        "coach_interactions":
            coach_interactions,

        "improvement_trend":
            improvement_trend,

        "current_domain":
            "Machine Learning",

        "quiz_difficulty":
            "Medium",

    }



# ==========================================================
# GENERATE PREDICTION
# ==========================================================

def get_learning_prediction(
    user_id,
):

    features = get_user_prediction_features(
        user_id
    )


    prediction = predict_performance(
        features
    )


    return prediction