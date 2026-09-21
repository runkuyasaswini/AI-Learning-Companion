from langchain_huggingface import HuggingFaceEmbeddings

from utils.config import EMBEDDING_MODEL


# Singleton embedding model instance
_embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={
        "device": "cpu",  # Change to "cuda" if using an NVIDIA GPU
    },
    encode_kwargs={
        "normalize_embeddings": True,
    },
)


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Return the singleton embedding model instance.

    Returns:
        HuggingFaceEmbeddings: Configured embedding model.
    """
    return _embedding_model


if __name__ == "__main__":

    model = get_embedding_model()

    print("\n" + "=" * 60)
    print("Embedding Model Loaded Successfully")
    print("=" * 60)
    print(f"Model : {EMBEDDING_MODEL}")
    print(f"Type  : {type(model).__name__}")
    print("=" * 60 + "\n")