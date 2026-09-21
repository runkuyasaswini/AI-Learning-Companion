from pathlib import Path

from langchain_community.vectorstores import FAISS

from rag.chunker import split_documents
from rag.embeddings import get_embedding_model


VECTOR_DB_PATH = Path("database/faiss_index")


def build_vector_store(
    documents_folder: Path | None = None,
) -> FAISS:
    """
    Build and save the FAISS vector database.

    Returns:
        FAISS: Newly created vector store.
    """

    print("\n" + "=" * 60)
    print("Building FAISS Vector Store")
    print("=" * 60)

    print("\nLoading and chunking documents...")

    chunks = split_documents(
        documents_folder
    )

    if not chunks:
        raise ValueError(
            "No document chunks found. Cannot build vector store."
        )

    print(f"Chunks Created : {len(chunks)}")

    embedding_model = get_embedding_model()

    print("\nGenerating embeddings and building FAISS index...")

    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model,
    )

    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

    vector_db.save_local(str(VECTOR_DB_PATH))

    print("\nFAISS Index Saved Successfully.")
    print(f"Location : {VECTOR_DB_PATH}")
    print("=" * 60 + "\n")

    return vector_db


def load_vector_store() -> FAISS:
    """
    Load an existing FAISS vector store.

    If the index doesn't exist yet, it will automatically
    be created from the knowledge base.

    Returns:
        FAISS: Loaded vector store.
    """

    index_file = VECTOR_DB_PATH / "index.faiss"

    if not index_file.exists():

        print("\nNo FAISS index found.")
        print("Building a new vector store...\n")

        return build_vector_store()

    embedding_model = get_embedding_model()

    print("\nLoading existing FAISS index...\n")

    return FAISS.load_local(
        str(VECTOR_DB_PATH),
        embedding_model,
        allow_dangerous_deserialization=True,
    )


if __name__ == "__main__":

    build_vector_store()