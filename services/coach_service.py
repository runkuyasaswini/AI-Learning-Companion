from rag.coach_rag import ask_coach

from services.learning_service import (
    get_completed_topics,
)

from services.progress_service import (
    ProgressService,
)

from services.quiz_service import (
    get_average_score,
)


# ==========================================================
# BUILD LEARNER CONTEXT
# ==========================================================

def build_learner_context(
    user_id,
):
    """
    Build a personalized learner profile
    for the AI Coach.
    """

    completed_topics = get_completed_topics(
        user_id
    )

    average_score = get_average_score(
        user_id
    )

    progress = ProgressService.get_learning_statistics(
    user_id
)

    domain_progress = progress["domain_progress"]

    recent_learning = progress["recent_learning"]

    context = []

    # ------------------------------------------------------

    context.append(
        "Learner Profile"
    )

    context.append("")

    context.append(
        f"Completed Topics: {len(completed_topics)}"
    )

    context.append(
        f"Average Quiz Score: {average_score}%"
    )

    context.append("")

    # ------------------------------------------------------
    # Completed Topics
    # ------------------------------------------------------

    if completed_topics:

        context.append(
            "Completed Topic List:"
        )

        for topic in completed_topics:

            context.append(
                f"- {topic}"
            )

    else:

        context.append(
            "No completed topics yet."
        )

    context.append("")

    # ------------------------------------------------------
    # Domain Progress
    # ------------------------------------------------------

    if domain_progress:

        context.append(
            "Domain Progress:"
        )

        for row in domain_progress:

            context.append(
                f"- {row['domain']}: "
                f"{row['completed']} completed"
            )

    context.append("")

    # ------------------------------------------------------
    # Recent Learning
    # ------------------------------------------------------

    if recent_learning:

        context.append(
            "Recently Studied:"
        )

        for row in recent_learning[:5]:

            context.append(
                f"- {row['topic']}"
            )

    return "\n".join(context)


# ==========================================================
# AI COACH
# ==========================================================

def get_coach_response(
    user_id,
    question,
    course=None,
):
    """
    Generate a personalized coaching response.
    """

    learner_context = build_learner_context(
        user_id
    )

    response = ask_coach(
            question=question,
            learner_context=learner_context,
            course=course,
        )

    return response


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    USER_ID = 1

    response = get_coach_response(
        USER_ID,
        "What should I study next?"
    )

    print("\n")

    print(response["answer"])