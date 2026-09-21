import httpx
from langchain_openai import ChatOpenAI

from rag.retriever import retrieve
from utils.config import (
    GENAI_API_KEY,
    GENAI_BASE_URL,
    GENAI_MODEL,
)

# --------------------------------------------------
# HTTP Client
# --------------------------------------------------

http_client = httpx.Client(
    verify=False
)

# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatOpenAI(
    base_url=GENAI_BASE_URL,
    model=GENAI_MODEL,
    api_key=GENAI_API_KEY,
    http_client=http_client,
)

# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are an expert AI Learning Companion, Senior Technical Trainer, and Interview Mentor.

Your responsibility is to teach students in a structured, educational manner rather than simply answering questions.

STRICT RULES

1. Use ONLY the provided learning material.
2. Never invent facts or use outside knowledge.
3. If the answer is not present in the provided context, reply exactly:
   "This topic is not available in the current learning material."
4. Never mention the existence of the provided context.
5. Explain concepts progressively from beginner to intermediate level.
6. Use Markdown formatting.
7. Use headings, bullet points, and short paragraphs.
8. Be educational rather than conversational.
9. If multiple concepts are related, connect them naturally.
10. Avoid repeating the same information.

Always try to structure your response as follows (omit sections that are not applicable):

## 🎯 Learning Objectives
Briefly explain what the learner will understand.

## 📘 Concept Overview
Give a concise definition.

## 🧠 Detailed Explanation
Explain step-by-step in simple language.

## 💡 Real-world Analogy
Relate the concept to a real-life example whenever possible.

## 💻 Practical Example
Provide a simple example based only on the learning material.

## ⚠ Common Mistakes
Mention beginner mistakes or misconceptions.

## 🎤 Interview Perspective
Mention one or two interview questions that could be asked on this concept.

## 📝 Quick Revision
Summarize the concept in 4–6 concise bullet points.

## ➡ Recommended Next Topics
Recommend related topics that naturally follow from the learning material.
"""

# --------------------------------------------------
# Context Builder
# --------------------------------------------------


def build_context(documents):
    """
    Convert retrieved documents into a structured context.
    """

    context = []

    for doc in documents:

        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")

        context.append(
            f"[Source: {source} | Page: {page}]\n"
            f"{doc.page_content.strip()}"
        )

    return "\n\n".join(context)


# --------------------------------------------------
# Main RAG Function
# --------------------------------------------------


def ask_ai(
    question: str,
    course: str | None = None,
):
    """
    Retrieve relevant documents and generate an educational response.
    """

    question = question.strip()

    if not question:
        return {
            "question": "",
            "answer": "Please enter a question.",
            "documents": [],
            "sources": [],
        }

    documents = retrieve(
            question,
            course,
        )

    if not documents:
        return {
            "question": question,
            "answer": "This topic is not available in the current learning material.",
            "documents": [],
            "sources": [],
        }

    context = build_context(documents)

    user_prompt = f"""
    Learning Material

    {context}

    Student Question

    {question}

    Prepare a complete lesson using only the learning material.

    The explanation should be accurate, educational, beginner-friendly, and well structured.

    If the learning material does not contain sufficient information, clearly state that instead of guessing.
    """

    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", user_prompt),
        ]
    )

    return {
        "question": question,
        "answer": response.content,
        "documents": documents,
        "sources": [
            {
                "domain": doc.metadata.get("domain"),
                "source": doc.metadata.get("source"),
                "file_type": doc.metadata.get("file_type"),
                "page": doc.metadata.get("page"),
            }
            for doc in documents
        ],
    }


# --------------------------------------------------
# Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("AI Learning Companion")
    print("Type 'exit' to quit.")
    print("=" * 70)

    while True:

        question = input("\nAsk: ").strip()

        if question.lower() == "exit":
            break

        result = ask_ai(question)

        print("\n")
        print("=" * 70)
        print("ANSWER")
        print("=" * 70)
        print(result["answer"])

        print("\n")
        print("=" * 70)
        print("SOURCES")
        print("=" * 70)

        for source in result["sources"]:

            print(
                f"{source['source']} | "
                f"Page: {source['page']} | "
                f"Domain: {source['domain']}"
            )