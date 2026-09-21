from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.loader import load_documents
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP
from pathlib import Path

def split_documents(
    folder_path: Path | None = None,
) -> list[Document]:
    """
    Load all knowledge base documents and split them into
    semantic chunks for embedding.

    Returns:
        List[Document]: Chunked LangChain documents.
    """

    documents = load_documents(
        folder_path
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)

    print("\n" + "=" * 60)
    print(f"Documents Loaded : {len(documents)}")
    print(f"Chunks Generated : {len(chunks)}")
    print("=" * 60 + "\n")

    return chunks


if __name__ == "__main__":

    chunks = split_documents()

    print(f"\nTotal Chunks : {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:5], start=1):

        print("=" * 80)
        print(f"Chunk #{i}")
        print(chunk.metadata)
        print()
        print(chunk.page_content[:500])
        print()