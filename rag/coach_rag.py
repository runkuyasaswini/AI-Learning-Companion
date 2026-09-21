import httpx

from langchain_openai import ChatOpenAI

from rag.retriever import retrieve

from utils.config import (
    GENAI_API_KEY,
    GENAI_BASE_URL,
    GENAI_MODEL,
)

# ==========================================================
# HTTP CLIENT
# ==========================================================

http_client = httpx.Client(
    verify=False,
)

# ==========================================================
# LLM
# ==========================================================

llm = ChatOpenAI(
    base_url=GENAI_BASE_URL,
    model=GENAI_MODEL,
    api_key=GENAI_API_KEY,
    http_client=http_client,
)

# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are an Expert AI Learning Mentor, Technical Trainer, Career Coach, and Interview Guide.

You have two responsibilities:

1. Teach concepts accurately using ONLY the supplied learning material.
2. Mentor the learner using ONLY the supplied learner profile.

STRICT RULES

1. Never invent learner progress or quiz scores.
2. Never invent technical information.
3. Use the learner profile only for mentoring, study guidance, recommendations, and interview preparation.
4. Use the learning material only for technical explanations.
5. If the learner asks what to study next, recommend topics based on their learning profile.
6. If the learner asks a technical question, answer ONLY using the supplied learning material.
7. If the requested topic is not available in the supplied learning material, politely state that it is not covered and encourage the learner to ask a question related to the current course. Do not guess or use outside knowledge.
8. Never mention "context", "documents", "retrieval", "learning material", or any internal system behavior.
9. Never say phrases like "The learner has asked...", "Based on the provided context...", or similar internal wording.
10. Be supportive, educational, concise, and well structured.
11. Use Markdown headings and bullet points where appropriate.

Choose the most appropriate response style based on the learner's question.

--------------------------------

If the learner asks what to study next:

## 📊 Current Progress

Briefly summarize their current learning progress.

## 🎯 Recommended Next Step

Recommend the next logical topic and explain why.

## 📅 Suggested Study Plan

Provide 3-5 practical study steps.

## 📌 Focus Areas

Highlight weak concepts or areas needing improvement if available.

## 🎤 Interview Readiness

Suggest interview topics to practice.

--------------------------------

If the learner asks a technical question:

## 📘 Explanation

Explain the concept clearly and simply.

## 💻 Example

Provide an example if available in the learning material.

## ⚠ Common Mistakes

Mention common beginner mistakes if applicable.

## 📝 Quick Revision

Summarize the important points.

## ➡ Next Topics

Recommend related topics to continue learning.

--------------------------------

If the learner asks for revision:

Provide concise revision notes followed by:

• Key concepts

• Quick revision points

• Important interview questions

--------------------------------

If the learner asks about interviews:

Provide:

• Frequently asked interview questions

• Important concepts to revise

• Interview preparation checklist

• Recommended practice questions

--------------------------------

If the learner asks a question unrelated to the current course:

## ❌ Topic Not Available

This topic is not covered in the current course.

Please ask a question related to the selected learning topic or course, and I'll be happy to help explain it in detail.
"""
# ==========================================================
# BUILD KNOWLEDGE CONTEXT
# ==========================================================

def build_context(documents):

    return "\n\n".join(
        doc.page_content.strip()
        for doc in documents
    )

# ==========================================================
# DETECT QUESTION TYPE
# ==========================================================

def is_mentoring_question(question: str) -> bool:
    """
    Return True if the question is about
    study planning, roadmap, revision,
    interview preparation or recommendations.
    """

    question = question.lower()

    keywords = [

        "next",

        "roadmap",

        "study",

        "learn next",

        "plan",

        "prepare",

        "interview",

        "career",

        "revise",

        "revision",

        "weak",

        "improve",

        "recommend",

        "suggest",

        "goal",

    ]

    return any(
        keyword in question
        for keyword in keywords
    )


# ==========================================================
# ASK COACH
# ==========================================================

def ask_coach(
    question: str,
    learner_context: str,
    course: str | None = None,
):

    # ------------------------------------------------------
# Retrieve learning material only when required
# ------------------------------------------------------

    documents = []

    knowledge_context = ""

    if not is_mentoring_question(question):

        documents = retrieve(
            question,
            course,
        )

        knowledge_context = build_context(
            documents
        )

    user_prompt = f"""
    Learner Profile

    {learner_context}

    ==================================================

    Learning Material

    {knowledge_context}

    ==================================================

    Learner Question

    {question}

    Instructions

    - Personalize the response using the learner profile.
    - If this is a mentoring question, prioritize the learner profile.
    - If this is a technical question, teach using only the supplied learning material.
    - Recommend the next learning step whenever appropriate.
    - Keep the explanation structured and practical.
    """

    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", user_prompt),
        ]
    )

    return {
        "answer": response.content,
        "documents": documents,
        "sources": [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page"),
                "file_type": doc.metadata.get("file_type"),
            }
            for doc in documents
        ],
    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    learner_context = """
Topics Completed:
Python Basics
Machine Learning Basics

Average Quiz Score:
82%

Weak Areas:
Gradient Descent
Decision Trees
"""

    result = ask_coach(
        question="Explain Gradient Descent.",
        learner_context=learner_context,
    )

    print("\n")
    print(result["answer"])