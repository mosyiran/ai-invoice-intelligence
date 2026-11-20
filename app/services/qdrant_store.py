
from pathlib import Path

from qdrant_client import QdrantClient, models


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Qdrant storage directory
QDRANT_PATH = BASE_DIR / "database" / "qdrant_storage"

QDRANT_PATH.mkdir(
    parents=True,
    exist_ok=True
)

COLLECTION_NAME = "invoices"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Create local Qdrant client
client = QdrantClient(
    path=str(QDRANT_PATH)
)


def initialize_collection():

    """
    Create the invoices collection if it does not exist.
    """

    if client.collection_exists(COLLECTION_NAME):
        print("Qdrant collection already exists.")
        return

    vector_size = client.get_embedding_size(
        EMBEDDING_MODEL
    )

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )

    print("Qdrant collection created successfully.")


def close_qdrant():

    client.close()
