from pathlib import Path
import pickle

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = Path(
    "ml/data/learner_performance.csv"
)

MODEL_PATH = Path(
    "ml/models"
)


# ==========================================================
# COLUMNS
# ==========================================================

CATEGORICAL_COLUMNS = [
    "current_domain",
    "quiz_difficulty",
    "improvement_trend",
]


DROP_COLUMNS = [
    "learner_id",
    "pass_probability",
    "learner_profile",
]


TARGET_COLUMN = "next_quiz_pass"


# ==========================================================
# LOAD DATA
# ==========================================================

def load_dataset():

    df = pd.read_csv(
        DATA_PATH
    )

    return df


# ==========================================================
# SAVE ENCODERS
# ==========================================================

def save_encoders(
    encoders,
):

    MODEL_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        MODEL_PATH / "label_encoders.pkl",
        "wb",
    ) as file:

        pickle.dump(
            encoders,
            file,
        )


# ==========================================================
# PREPROCESS DATA
# ==========================================================

def preprocess_data():

    """
    Complete preprocessing pipeline.

    Returns:

    X_train,
    X_test,
    y_train,
    y_test
    """

    df = load_dataset()


    # ------------------------------------------------------
    # Separate Target
    # ------------------------------------------------------

    X = df.drop(
        columns=[
            TARGET_COLUMN
        ]
    )

    y = df[
        TARGET_COLUMN
    ]


    # ------------------------------------------------------
    # Remove Unnecessary Columns
    # ------------------------------------------------------

    X = X.drop(
        columns=DROP_COLUMNS
    )


    # ------------------------------------------------------
    # Encode Categorical Features
    # ------------------------------------------------------

    encoders = {}

    for column in CATEGORICAL_COLUMNS:

        encoder = LabelEncoder()

        X[column] = encoder.fit_transform(
            X[column]
        )

        encoders[column] = encoder


    # ------------------------------------------------------
    # Save Feature Order
    # ------------------------------------------------------

    with open(
        MODEL_PATH / "feature_columns.pkl",
        "wb",
    ) as file:

        pickle.dump(
            list(X.columns),
            file,
        )


    # ------------------------------------------------------
    # Save Encoders
    # ------------------------------------------------------

    save_encoders(
        encoders
    )


    # ------------------------------------------------------
    # Train Test Split
    # ------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42,

        stratify=y,
    )


    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":


    X_train, X_test, y_train, y_test = preprocess_data()


    print("=" * 60)

    print("Preprocessing Completed")

    print("=" * 60)

    print()

    print(
        "Training Features:",
        X_train.shape
    )

    print(
        "Testing Features:",
        X_test.shape
    )

    print()

    print(
        "Training Labels:",
        y_train.shape
    )

    print(
        "Testing Labels:",
        y_test.shape
    )

    print()

    print(
        "Feature Columns:"
    )

    print(
        list(X_train.columns)
    )