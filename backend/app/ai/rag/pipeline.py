import hashlib
import logging
from typing import Optional
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGPipeline:
    def __init__(self):
        self.collection_name = settings.CHROMA_COLLECTION_NAME
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                import chromadb
                self._client = chromadb.HttpClient(
                    host=settings.CHROMA_HOST,
                    port=settings.CHROMA_PORT,
                )
            except Exception as e:
                logger.warning(f"ChromaDB not available: {e}. Using in-memory mode.")
                import chromadb
                self._client = chromadb.Client()
        return self._client

    def _get_or_create_collection(self):
        try:
            return self.client.get_or_create_collection(self.collection_name)
        except Exception as e:
            logger.error(f"Failed to get/create collection: {e}")
            return None

    def ingest_text(self, text: str, metadata: dict, doc_id: str) -> bool:
        try:
            collection = self._get_or_create_collection()
            if not collection:
                return False

            chunks = self._chunk_text(text)
            chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

            collection.add(
                documents=chunks,
                metadatas=[{**metadata, "chunk_index": i} for i in range(len(chunks))],
                ids=chunk_ids,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to ingest text: {e}")
            return False

    def search(self, query: str, n_results: int = 5) -> list[dict]:
        try:
            collection = self._get_or_create_collection()
            if not collection:
                return []

            results = collection.query(
                query_texts=[query],
                n_results=n_results,
            )

            documents = []
            if results.get("documents"):
                for i, doc in enumerate(results["documents"][0]):
                    documents.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                        "distance": results["distances"][0][i] if results.get("distances") else 0,
                    })
            return documents
        except Exception as e:
            logger.error(f"Failed to search: {e}")
            return []

    def get_context_for_agent(self, query: str, agent_type: str, n_results: int = 3) -> str:
        results = self.search(query, n_results=n_results)
        if not results:
            return ""
        context_parts = []
        for r in results:
            context_parts.append(r["content"])
        return "\n\n".join(context_parts)

    def _chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks

    def compute_query_hash(self, query: str) -> str:
        return hashlib.sha256(query.encode()).hexdigest()
