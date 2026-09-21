from pathlib import Path
import pickle

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

from ml.preprocess import preprocess_data


# ==========================================================
# PATH
# ==========================================================

MODEL_PATH = Path(
    "ml/models/random_forest.pkl"
)


# ==========================================================
# LOAD MODEL
# ==========================================================

def load_model():

    with open(
        MODEL_PATH,
        "rb",
    ) as file:

        model = pickle.load(
            file
        )

    return model


# ==========================================================
# EVALUATE MODEL
# ==========================================================

def evaluate_model():

    print("\nLoading test data...")

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = preprocess_data()


    print("\nLoading model...")

    model = load_model()


    print("\nGenerating predictions...")

    predictions = model.predict(
        X_test
    )


    probabilities = model.predict_proba(
        X_test
    )[:, 1]


    # ------------------------------------------------------
    # Metrics
    # ------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
    )

    recall = recall_score(
        y_test,
        predictions,
    )

    f1 = f1_score(
        y_test,
        predictions,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )


    print("\n")
    print("=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(
        f"Accuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1 Score  : {f1:.4f}"
    )

    print(
        f"ROC AUC   : {roc_auc:.4f}"
    )


    # ------------------------------------------------------
    # Classification Report
    # ------------------------------------------------------

    print("\nClassification Report\n")

    print(
        classification_report(
            y_test,
            predictions,
        )
    )


    # ------------------------------------------------------
    # Confusion Matrix
    # ------------------------------------------------------

    print("\nConfusion Matrix\n")

    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )


    # ------------------------------------------------------
    # Feature Importance
    # ------------------------------------------------------

    print("\nFeature Importance\n")


    importance = model.feature_importances_

    for feature, score in sorted(
        zip(
            X_test.columns,
            importance,
        ),
        key=lambda x: x[1],
        reverse=True,
    ):

        print(
            f"{feature:30} {score:.4f}"
        )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    evaluate_model()