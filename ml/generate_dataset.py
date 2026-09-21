import random
from pathlib import Path

import pandas as pd


# ==========================================================
# CONFIGURATION
# ==========================================================

random.seed(42)

TOTAL_RECORDS = 5000


DOMAINS = [
    "Python",
    "SQL",
    "Machine Learning",
    "NLP",
    "Generative AI",
    "MLOps",
]


DIFFICULTIES = [
    "Easy",
    "Medium",
    "Hard",
]


LEARNER_PROFILES = [
    "Fast Learner",
    "Consistent Learner",
    "Casual Learner",
    "Struggling Learner",
]


TRENDS = [
    "Improving",
    "Stable",
    "Declining",
]


DATA_PATH = Path(
    "ml/data/learner_performance.csv"
)


# ==========================================================
# GENERATE LEARNER PROFILE
# ==========================================================

def generate_profile():

    return random.choices(
        LEARNER_PROFILES,
        weights=[
            20,
            35,
            30,
            15,
        ],
    )[0]


# ==========================================================
# GENERATE LEARNER
# ==========================================================

def generate_learner(
    learner_number,
):

    profile = generate_profile()


    # ------------------------------------------------------
    # Base Behaviour Based On Profile
    # ------------------------------------------------------

    if profile == "Fast Learner":

        completed_topics = random.randint(
            35,
            60,
        )

        study_hours = random.uniform(
            18,
            35,
        )

        streak = random.randint(
            15,
            30,
        )

        revision = random.randint(
            8,
            20,
        )

        coach = random.randint(
            5,
            15,
        )


    elif profile == "Consistent Learner":

        completed_topics = random.randint(
            20,
            45,
        )

        study_hours = random.uniform(
            10,
            25,
        )

        streak = random.randint(
            10,
            25,
        )

        revision = random.randint(
            5,
            15,
        )

        coach = random.randint(
            3,
            12,
        )


    elif profile == "Casual Learner":

        completed_topics = random.randint(
            5,
            25,
        )

        study_hours = random.uniform(
            3,
            12,
        )

        streak = random.randint(
            0,
            10,
        )

        revision = random.randint(
            0,
            5,
        )

        coach = random.randint(
            0,
            5,
        )


    else:

        completed_topics = random.randint(
            0,
            15,
        )

        study_hours = random.uniform(
            1,
            8,
        )

        streak = random.randint(
            0,
            5,
        )

        revision = random.randint(
            0,
            3,
        )

        coach = random.randint(
            0,
            3,
        )


    completion_percentage = round(
        (completed_topics / 60) * 100,
        2,
    )


    quizzes_attempted = max(
        1,
        int(
            completed_topics *
            random.uniform(
                0.5,
                0.9,
            )
        )
    )


    # ------------------------------------------------------
    # Quiz Score
    # ------------------------------------------------------

    average_score = (
        35
        +
        (study_hours * 1.5)
        +
        (streak * 0.8)
        +
        (revision * 0.9)
    )


    if profile == "Fast Learner":

        average_score += 10


    elif profile == "Struggling Learner":

        average_score -= 10


    average_score += random.uniform(
        -5,
        5,
    )


    average_score = round(
        max(
            30,
            min(
                98,
                average_score,
            )
        ),
        2,
    )


    # ------------------------------------------------------
    # Improvement Trend
    # ------------------------------------------------------

    if profile in [
        "Fast Learner",
        "Consistent Learner",
    ]:

        trend = random.choices(
            TRENDS,
            weights=[
                70,
                25,
                5,
            ],
        )[0]


    elif profile == "Casual Learner":

        trend = random.choices(
            TRENDS,
            weights=[
                30,
                40,
                30,
            ],
        )[0]


    else:

        trend = random.choices(
            TRENDS,
            weights=[
                10,
                30,
                60,
            ],
        )[0]


    return {

        "learner_id":
            f"LRN{learner_number:05}",

        "learner_profile":
            profile,

        "completed_topics":
            completed_topics,

        "quizzes_attempted":
            quizzes_attempted,

        "average_quiz_score":
            average_score,

        "learning_streak":
            streak,

        "study_hours":
            round(
                study_hours,
                2,
            ),

        "completion_percentage":
            completion_percentage,

        "revision_sessions":
            revision,

        "coach_interactions":
            coach,

        "improvement_trend":
            trend,

        "current_domain":
            random.choice(
                DOMAINS
            ),

        "quiz_difficulty":
            random.choices(
                DIFFICULTIES,
                weights=[
                    30,
                    50,
                    20,
                ],
            )[0],
    }


# ==========================================================
# PASS PROBABILITY
# ==========================================================

def calculate_pass_probability(
    learner,
):

    score = 0


    score += (
        learner["average_quiz_score"]
        * 0.45
    )


    score += (
        learner["completion_percentage"]
        * 0.20
    )


    score += (
        min(
            learner["study_hours"],
            30,
        )
        / 30
        * 10
    )


    score += (
        learner["learning_streak"]
        / 30
        * 8
    )


    score += (
        learner["revision_sessions"]
        / 20
        * 5
    )


    if learner["improvement_trend"] == "Improving":

        score += 8


    elif learner["improvement_trend"] == "Declining":

        score -= 8


    if learner["quiz_difficulty"] == "Hard":

        score -= 5


    probability = score / 100


    return round(
        max(
            0,
            min(
                probability,
                1,
            ),
        ),
        3,
    )


# ==========================================================
# TARGET
# ==========================================================

def assign_target(probability):

    adjusted_probability = probability + random.uniform(
        -0.15,
        0.15,
    )

    return int(
        adjusted_probability >= 0.5
    )


# ==========================================================
# DATASET GENERATION
# ==========================================================

def generate_dataset():

    records = []


    for i in range(
        1,
        TOTAL_RECORDS + 1,
    ):

        learner = generate_learner(i)


        probability = calculate_pass_probability(
            learner
        )


        learner["pass_probability"] = probability


        learner["next_quiz_pass"] = assign_target(
            probability
        )


        records.append(
            learner
        )


    return pd.DataFrame(
        records
    )


# ==========================================================
# SAVE DATASET
# ==========================================================

def save_dataset(
    df,
):

    DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    df.to_csv(
        DATA_PATH,
        index=False,
    )


    print("=" * 60)

    print(
        "Dataset Generated Successfully"
    )

    print(
        f"Records: {len(df)}"
    )

    print(
        f"Pass Rate: {df['next_quiz_pass'].mean()*100:.2f}%"
    )

    print(
        f"Average Score: {df['average_quiz_score'].mean():.2f}"
    )

    print("=" * 60)



# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    dataset = generate_dataset()

    save_dataset(
        dataset
    )

    print("\nSample Data\n")

    print(
        dataset.head()
    )