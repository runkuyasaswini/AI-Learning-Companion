from langchain_core.documents import Document

from rag.vector_store import load_vector_store
from utils.config import FETCH_K, TOP_K


# ==========================================================
# CREATE RETRIEVER
# ==========================================================

def get_retriever():
    """
    Always return a retriever built from the
    latest FAISS index.
    """

    vector_store = load_vector_store()

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": TOP_K,
            "fetch_k": FETCH_K,
        },
    )


def retrieve(
    query: str,
    course: str | None = None,
):
    """
    Retrieve the most relevant document chunks for a user query.

    Args:
        query (str): User's search query.

    Returns:
        List[Document]: Retrieved document chunks.
    """

    query = query.strip()

    if not query:
        return []

    retriever = get_retriever()

    documents = retriever.invoke(query)

       # ------------------------------------------------------
    # Filter by selected course
    # ------------------------------------------------------

    if course:

        documents = [
            doc
            for doc in documents
            if doc.metadata.get("domain") == course
        ]

    # ------------------------------------------------------
    # Remove duplicate chunks
    # ------------------------------------------------------

    unique_documents = []

    seen = set()

    for doc in documents:

        key = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            doc.page_content[:150],
        )

        if key not in seen:

            seen.add(key)

            unique_documents.append(doc)

    # ------------------------------------------------------
    # Keep only the best TOP_K chunks
    # ------------------------------------------------------

    documents = unique_documents[:TOP_K]

    print("\n========== RETRIEVAL DEBUG ==========")
    print("Query:", query)
    print("Course:", course)
    print("Retrieved:", len(documents))

    for doc in documents:
        print(
            "Domain:", doc.metadata.get("domain"),
            "| Source:", doc.metadata.get("source")
        )

    print("=====================================\n")

    return documents



if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("Knowledge Base Retriever")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        query = input("\nAsk Question: ").strip()

        if query.lower() == "exit":
            break

        documents = retrieve(query)

        if not documents:
            print("\nNo relevant documents found.\n")
            continue

        print(f"\nRetrieved {len(documents)} document(s).\n")

        for index, document in enumerate(documents, start=1):

            print("=" * 80)
            print(f"Result {index}")

            print(f"Domain    : {document.metadata.get('domain', 'Unknown')}")
            print(f"Source    : {document.metadata.get('source', 'Unknown')}")
            print(f"File Type : {document.metadata.get('file_type', 'Unknown')}")

            if "page" in document.metadata:
                print(f"Page      : {document.metadata['page']}")

            if "start_index" in document.metadata:
                print(f"Chunk Pos : {document.metadata['start_index']}")

            print("\nContent:\n")
            print(document.page_content[:800])
            print()