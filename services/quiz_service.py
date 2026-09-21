from database.db import get_connection

from rag.quiz_generator import generate_quiz


# ==========================================================
# GET QUIZ HISTORY
# ==========================================================

def get_quiz_history(
    user_id,
    limit=10,
):
    """
    Return recent quiz attempts of a user.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            domain,
            topic,
            difficulty,
            score,
            total_questions,
            percentage,
            attempted_at
        FROM quiz_history
        WHERE user_id = ?
        ORDER BY attempted_at DESC
        LIMIT ?
        """,
        (
            user_id,
            limit,
        ),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==========================================================
# GENERATE QUIZ
# ==========================================================
def create_quiz(
    topic: str,
    difficulty: str = "Medium",
    total_questions: int = 10,
    course: str | None = None,
):
    """
    Generate a quiz using the RAG pipeline.
    """

    quiz = generate_quiz(
        topic=topic,
        difficulty=difficulty,
        total_questions=total_questions,
        course=course,
    )

    # --------------------------------------------------
    # Handle RAG / knowledge errors
    # --------------------------------------------------

    if isinstance(quiz, dict) and "error" in quiz:

        return quiz


    if not isinstance(quiz, list):

        return {
            "error": (
                "Unable to generate quiz. "
                "Please try again."
            )
        }


    validated_quiz = []

    for question in quiz:

        if (
            "question" in question
            and "options" in question
            and "answer" in question
            and "explanation" in question
            and len(question["options"]) == 4
        ):

            validated_quiz.append(question)


    if not validated_quiz:

        return {
            "error": (
                "No valid quiz questions were generated."
            )
        }


    return validated_quiz

# ==========================================================
# EVALUATE QUIZ
# ==========================================================

def evaluate_quiz(
    quiz,
    user_answers,
):
    """
    Evaluate quiz responses.

    user_answers format:

    {
        0: "Option A",
        1: "Option C",
        2: "Option B"
    }

    Returns:
        dict
    """

    score = 0

    results = []

    for index, question in enumerate(quiz):

        user_answer = user_answers.get(index)

        correct_answer = question["answer"]

        is_correct = (
            user_answer == correct_answer
        )

        if is_correct:
            score += 1

        results.append(
            {
                "question": question["question"],
                "selected": user_answer,
                "correct": correct_answer,
                "is_correct": is_correct,
                "explanation": question["explanation"],
            }
        )

    total_questions = len(quiz)

    percentage = (
        score / total_questions * 100
        if total_questions
        else 0
    )

    return {
        "score": score,
        "total_questions": total_questions,
        "percentage": round(
            percentage,
            2,
        ),
        "results": results,
    }

# ==========================================================
# SAVE QUIZ ATTEMPT
# ==========================================================

def save_quiz_attempt(
    user_id,
    domain,
    topic,
    difficulty,
    score,
    total_questions,
    percentage,
):
    """
    Save a quiz attempt.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_history
        (
            user_id,
            domain,
            topic,
            difficulty,
            score,
            total_questions,
            percentage
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """,
        (
            user_id,
            domain,
            topic,
            difficulty,
            score,
            total_questions,
            percentage,
        ),
    )

    conn.commit()

    conn.close()


# ==========================================================
# SUBMIT QUIZ
# ==========================================================

def submit_quiz(
    user_id,
    domain,
    topic,
    difficulty,
    quiz,
    user_answers,
):
    """
    Evaluate the quiz, save the attempt,
    and return the quiz result.
    """

    result = evaluate_quiz(
        quiz,
        user_answers,
    )

    save_quiz_attempt(
        user_id=user_id,
        domain=domain,
        topic=topic,
        difficulty=difficulty,
        score=result["score"],
        total_questions=result["total_questions"],
        percentage=result["percentage"],
    )

    return result


# ==========================================================
# GET LAST QUIZ
# ==========================================================

def get_last_quiz(
    user_id,
    domain,
    topic,
):
    """
    Return the latest quiz attempt
    for a specific topic.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM quiz_history
        WHERE user_id = ?
        AND domain = ?
        AND topic = ?
        ORDER BY attempted_at DESC
        LIMIT 1
        """,
        (
            user_id,
            domain,
            topic,
        ),
    )

    quiz = cursor.fetchone()

    conn.close()

    return quiz


# ==========================================================
# GET AVERAGE SCORE
# ==========================================================

def get_average_score(
    user_id,
):
    """
    Return user's average quiz score.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(percentage)
        FROM quiz_history
        WHERE user_id = ?
        """,
        (user_id,),
    )

    average = cursor.fetchone()[0]

    conn.close()

    if average is None:
        return 0

    return round(
        average,
        2,
    )