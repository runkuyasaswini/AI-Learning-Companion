import json

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
    verify=False
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
You are an expert Quiz Generation AI, Senior Assessment Designer, Prompt Engineer, and Subject Matter Expert.

Your responsibility is to generate high-quality multiple-choice questions ONLY from the supplied learning material retrieved from the uploaded PDF.

=========================
STRICT RULES
=========================

1. Use ONLY the provided learning material.
2. Never use external knowledge.
3. Never hallucinate facts.
4. If the answer is not explicitly or logically supported by the provided context, DO NOT generate that question.
5. Never invent information to reach the requested number of questions.
6. It is acceptable to return fewer questions if the context is insufficient.

=========================
QUESTION QUALITY
=========================

Generate meaningful questions that assess understanding instead of memorization.

Prefer questions about:

• Concepts
• Definitions
• Architecture
• Algorithms
• Workflow
• Features
• Advantages
• Disadvantages
• Comparisons
• Applications
• Best practices
• Important observations

Avoid:

• Duplicate questions
• Reworded duplicates
• Trivial facts
• Page numbers
• Formatting details
• Questions copied directly from the document
• Yes/No questions

Each question must focus on a different concept.

=========================
DIFFICULTY
=========================

Easy
- Basic recall
- Definitions
- Fundamental concepts

Medium
- Understanding
- Relationships
- Comparisons
- Applications

Hard
- Analysis
- Scenario based
- Multi-step reasoning
- Decision making
- Problem solving

=========================
OPTIONS
=========================

Each question MUST contain EXACTLY four options.

Rules:

• Exactly one correct answer.
• Three realistic distractors.
• Distractors should belong to the same topic.
• Never create silly or obviously incorrect answers.
• Shuffle option positions naturally.
• The correct answer must appear exactly as one of the options.

=========================
EXPLANATION
=========================

Provide a short explanation explaining WHY the correct answer is correct.

Maximum two sentences.

Use ONLY the supplied learning material.

=========================
OUTPUT
=========================

Return ONLY valid JSON.

No markdown.

No code fences.

No comments.

No introductory text.

The output must exactly follow this schema:

[
    {
        "question": "...",
        "options": [
            "...",
            "...",
            "...",
            "..."
        ],
        "answer": "...",
        "explanation": "..."
    }
]

Return ONLY JSON.
"""

# ==========================================================
# BUILD CONTEXT
# ==========================================================

def build_context(documents):

    return "\n\n".join(
        doc.page_content.strip()
        for doc in documents
    )

# ==========================================================
# GENERATE QUIZ
# ==========================================================

def generate_quiz(
    topic: str,
    difficulty: str = "Medium",
    total_questions: int = 10,
    course: str | None = None,
):

    documents = retrieve(
            topic,
            course,
        )

    context = build_context(documents)

    # ------------------------------------------------------
    # No learning material found
    # ------------------------------------------------------

    if not documents or not context.strip():

        return {
            "error": (
                "No learning material found for this topic. "
                "Please upload the course material and build the knowledge base."
            )
        }

    user_prompt = f"""
    The following text has been extracted from an uploaded PDF using the RAG pipeline.

    Topic:
    {topic}

    Difficulty:
    {difficulty}

    Requested Questions:
    {total_questions}

    =========================
    LEARNING MATERIAL
    =========================

    {context}

    =========================
    TASK
    =========================

    Read the complete learning material carefully before generating questions.

    Generate EXACTLY {total_questions} high-quality multiple-choice questions if sufficient information is available.

    If there is insufficient information, return fewer questions instead of creating unsupported content.

    Requirements:

    1. Cover different concepts from the document.
    2. Do not ask duplicate or similar questions.
    3. Do not copy sentences directly from the learning material.
    4. Test conceptual understanding instead of simple memorization.
    5. Use only the supplied context.
    6. Do not use outside knowledge.
    7. Every question must have exactly four options.
    8. Exactly one option must be correct.
    9. The answer must match one of the options exactly.
    10. Provide a concise explanation based only on the supplied learning material.
    11. Return ONLY valid JSON.

    Remember:

    Quality is more important than quantity.

    Never hallucinate.

    Never fabricate answers.

    Return ONLY JSON.
    """
    
    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", user_prompt),
        ]
    )

    try:

        quiz = json.loads(response.content)

        return quiz

    except Exception as e:

        print("\n========== QUIZ DEBUG ==========")
        print(response.content)
        print(e)
        print("===============================\n")

        return []
        

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    quiz = generate_quiz(
        topic="Logistic Regression",
        difficulty="Easy",
        total_questions=5,
    )

    print(json.dumps(
        quiz,
        indent=4,
    ))