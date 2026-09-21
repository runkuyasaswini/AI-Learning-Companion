import httpx

from langchain_openai import ChatOpenAI

from rag.retriever import retrieve
from langchain_community.document_loaders import PyPDFLoader

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
You are an expert AI Learning Companion and Technical Educator.

Your job is to create high-quality study notes and revision material.

Rules:

- Use ONLY the supplied learning material.
- Never invent facts.
- Never use outside knowledge.
- Keep explanations concise and educational.
- Use Markdown formatting.
- Focus on revision rather than detailed teaching.
- Highlight important concepts.
- Include interview preparation whenever applicable.

Generate the summary using the following structure.

# 📘 Topic Summary

Provide a 2-3 sentence overview.

---

# 🎯 Learning Objectives

List what the learner should understand after studying this topic.

---

# 📌 Key Concepts

Explain the major concepts briefly using bullet points.

---

# 💡 Important Points

Mention the most important facts that should be remembered.

---

# 💻 Practical Notes

Mention practical applications, syntax, workflow or implementation details if available.

---

# ⚠ Common Interview Questions

Provide 3-5 interview questions related to the topic.

---

# 📝 Quick Revision

Provide concise revision bullets suitable for last-minute preparation.

---

# 🚀 Recommended Next Topics

Suggest logical next topics only if they are present or naturally related to the provided learning material.
"""

# ==========================================================
# BUILD CONTEXT
# ==========================================================

def build_context(documents):

    return "\n\n".join(
        doc.page_content
        for doc in documents
    )

# ==========================================================
# GENERATE SUMMARY
# ==========================================================

def generate_summary(
    topic,
    course=None,
):

    documents = retrieve(
        query=topic,
        course=course,
    )

    if not documents:

        return {
            "error":
            "No learning material found for this topic."
        }

    context = build_context(documents)

    prompt = f"""
    Learning Material
    
    {context}

    Prepare professional study notes.

    The notes should help a learner revise the topic quickly before interviews or quizzes.

    Follow the exact structure described in the system prompt.

    Do not use any information outside the provided document.
    """

    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", prompt),
        ]
    )

    return {
        "summary": response.content,
        "sources": documents,
    }

# ==========================================================
# GENERATE SUMMARY FROM PDF
# ==========================================================

def generate_uploaded_pdf_summary(
    pdf_path: str,
):
    """
    Generate a summary directly from an uploaded PDF.
    """

    loader = PyPDFLoader(
        pdf_path,
    )

    documents = loader.load()

    text = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    # Limit context to avoid huge prompts
    text = text[:15000]

    prompt = f"""
Document Content

{text}

Generate concise revision notes using the following format:

# Document Summary

## Overview

## Key Concepts

## Important Points

## Practical Notes

## Interview Tips

## Quick Revision
"""

    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", prompt),
        ]
    )

    return {
        "summary": response.content,
    }