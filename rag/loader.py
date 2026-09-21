from pathlib import Path
import re

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document


DEFAULT_DATA_FOLDER = Path("data/knowledge_base")

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".md",
    ".txt",
}


def clean_text(text: str) -> str:
    """
    Basic text cleanup before chunking.
    """

    text = text.replace("\t", " ")

    text = re.sub(r"[ ]{2,}", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def get_domain(file: Path) -> str:
    """
    Get the course/domain name.

    If documents are inside uploads/courses/<Course Name>/,
    use the parent folder as the domain.

    Otherwise fall back to the filename.
    """

    if file.parent.name != "knowledge_base":

        return file.parent.name

    return (
        file.stem
        .replace("_", " ")
        .replace("-", " ")
    )


def load_documents(
    folder_path: Path | None = None,
) -> list[Document]:
    """
    Load all supported knowledge base documents.
    """
    if folder_path is None:

        folder_path = DEFAULT_DATA_FOLDER
    
    print("\n" + "=" * 60)
    print("LOADER DEBUG")
    print(f"Folder Being Loaded : {folder_path}")
    print("=" * 60)

    documents: list[Document] = []

    if not folder_path.exists():

        raise FileNotFoundError(
            f"Knowledge base folder not found: {folder_path}"
        )

    print(f"\nLoading documents from: {folder_path}\n")

    for file in sorted(folder_path.rglob("*")):

        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:

            if file.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file))

            else:
                loader = TextLoader(
                    str(file),
                    encoding="utf-8"
                )

            loaded_docs = loader.load()

            for doc in loaded_docs:

                doc.page_content = clean_text(
                    doc.page_content
                )

                doc.metadata.update({

                    "source": file.name,

                    "domain": get_domain(file),

                    "file_type": file.suffix.lower()

                })
                

            documents.extend(loaded_docs)

            print(
                f"Loaded: {file.name} "
                f"({len(loaded_docs)} pages)"
            )

        except Exception as e:

            print(
                f"Skipped {file.name}: {e}"
            )

    print(
        f"\nTotal Pages Loaded: {len(documents)}\n"
    )

    return documents


if __name__ == "__main__":

    docs = load_documents()

    print(f"Loaded {len(docs)} pages.")