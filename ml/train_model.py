from pathlib import Path
import pickle

from sklearn.ensemble import RandomForestClassifier

from ml.preprocess import preprocess_data


# ==========================================================
# PATHS
# ==========================================================

MODEL_PATH = Path(
    "ml/models/random_forest.pkl"
)


# ==========================================================
# TRAIN MODEL
# ==========================================================

def train_model():

    """
    Train Random Forest classifier
    and save the model.
    """

    print("\nLoading processed data...")

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = preprocess_data()


    print("\nTraining Random Forest Model...")


    model = RandomForestClassifier(

        n_estimators=200,

        max_depth=10,

        random_state=42,

        class_weight="balanced",

    )


    model.fit(
        X_train,
        y_train,
    )


    print("\nTraining Completed.")


    # ------------------------------------------------------
    # Save Model
    # ------------------------------------------------------

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    with open(
        MODEL_PATH,
        "wb",
    ) as file:

        pickle.dump(
            model,
            file,
        )


    print(
        "\nModel Saved Successfully."
    )

    print(
        f"Location : {MODEL_PATH}"
    )


    return model


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    train_model()