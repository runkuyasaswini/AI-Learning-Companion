from pathlib import Path
import pickle

import pandas as pd


# ==========================================================
# PATHS
# ==========================================================

MODEL_PATH = Path(
    "ml/models/random_forest.pkl"
)

ENCODER_PATH = Path(
    "ml/models/label_encoders.pkl"
)

FEATURE_PATH = Path(
    "ml/models/feature_columns.pkl"
)


# ==========================================================
# LOAD ARTIFACTS
# ==========================================================

def load_model():

    with open(
        MODEL_PATH,
        "rb",
    ) as file:

        return pickle.load(file)



def load_encoders():

    with open(
        ENCODER_PATH,
        "rb",
    ) as file:

        return pickle.load(file)



def load_features():

    with open(
        FEATURE_PATH,
        "rb",
    ) as file:

        return pickle.load(file)



# ==========================================================
# PREPARE INPUT
# ==========================================================

def prepare_input(
    learner_data,
):

    """
    Convert raw learner data
    into model-ready format.
    """


    df = pd.DataFrame(
        [learner_data]
    )


    encoders = load_encoders()


    # ------------------------------------------------------
    # Encode categorical columns
    # ------------------------------------------------------

    for column, encoder in encoders.items():

        df[column] = encoder.transform(
            df[column]
        )


    feature_columns = load_features()


    # Ensure same order as training

    df = df[
        feature_columns
    ]


    return df



# ==========================================================
# PREDICT
# ==========================================================

def predict_performance(
    learner_data,
):

    """
    Predict next quiz success probability.
    """


    model = load_model()


    processed_data = prepare_input(
        learner_data
    )


    probability = model.predict_proba(
        processed_data
    )[0][1]


    prediction = (
        "Likely to Pass"
        if probability >= 0.5
        else "Needs More Practice"
    )


    # ------------------------------------------------------
    # Confidence
    # ------------------------------------------------------

    if probability >= 0.85:

        confidence = "High"

    elif probability >= 0.65:

        confidence = "Medium"

    else:

        confidence = "Low"



    return {

        "probability":
            round(
                probability * 100,
                2,
            ),

        "prediction":
            prediction,

        "confidence":
            confidence,

    }



# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":


    sample_learner = {

        "completed_topics": 25,

        "quizzes_attempted": 15,

        "average_quiz_score": 82,

        "learning_streak": 18,

        "study_hours": 20,

        "completion_percentage": 42,

        "revision_sessions": 8,

        "coach_interactions": 5,

        "improvement_trend": "Improving",

        "current_domain": "Machine Learning",

        "quiz_difficulty": "Medium",

    }


    result = predict_performance(
        sample_learner
    )


    print("\nPrediction Result")

    print("=" * 40)

    print(result)