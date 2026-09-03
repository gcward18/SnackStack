"""ChromaDB vector-store setup and retrieval helpers."""
import os
from functools import lru_cache # caching to prevent multiple chroma instances from being created

from langchain_chroma import Chroma # manages the vector collection
from langchain_core.retrievers import BaseRetriever # return type for retriever

from config import get_embedding # provides embedding model
from data.menu import get_menu_documents # provides menu documents

COLLECTION_NAME = "snackstack_menu"
CHROMA_DIRECTORY = os.getenv("CHROMA_DIRECTORY", "./chroma_db")

@lru_cache
def get_menu_vector_store() -> Chroma:
    """Return cached Chroma vector-store."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedding(),
        persist_directory=CHROMA_DIRECTORY,
    )

def index_menu() -> int:
    documents = get_menu_documents()
    vector_store = get_menu_vector_store()

    ids = [
        str(document.id) for document in documents
    ]

    vector_store.add_documents(
        documents=documents,
        ids=ids
    )

    return len(documents)

@lru_cache
def get_retriever() -> BaseRetriever:
    """Return cached retriever."""
    return get_menu_vector_store().as_retriever(
        search_type="similarity",
        search_kwars={"k": 2, "score_threshold": 0.5},
    )

if __name__ == "__main__":
    from time import time

    start = time()

    index_count = index_menu()

    end = time()
    print(f"Indexed {index_count} menus in {time() - start:.2f} seconds.")
