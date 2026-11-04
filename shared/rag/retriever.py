"""Stable retrieval contract shared by every framework implementation."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, TypedDict

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

try:
    from .ingest import COLLECTION_NAME, DEFAULT_DB_PATH
except ImportError:
    from ingest import COLLECTION_NAME, DEFAULT_DB_PATH


class RetrievedChunk(TypedDict):
    content: str
    metadata: dict[str, Any]
    distance: float
    citation: str


ALIASES = (
    (
        re.compile(r"\bprazo final para acerto de matrícula\b", re.I),
        "fim do período para acerto de matrícula",
    ),
    (re.compile(r"\bbd\s*[- ]?\s*(?:2|ii)\b", re.I), "Banco de Dados II"),
    (re.compile(r"\bbd\s*[- ]?\s*(?:1|i)\b", re.I), "Banco de Dados I"),
    (re.compile(r"\btg\s*[- ]?\s*(?:2|ii)\b", re.I), "Trabalho de Graduação II"),
    (re.compile(r"\btg\s*[- ]?\s*(?:1|i)\b", re.I), "Trabalho de Graduação I"),
)
def normalize_query(query: str) -> str:
    """Expand stable institutional aliases without another model call."""
    normalized = " ".join(query.split())
    for pattern, replacement in ALIASES:
        normalized = pattern.sub(replacement, normalized)
    return normalized


def _where_filter(filters: dict[str, str | int | float | bool] | None) -> Any:
    if not filters:
        return None
    clauses = [{key: value} for key, value in sorted(filters.items())]
    return clauses[0] if len(clauses) == 1 else {"$and": clauses}


def _citation(metadata: dict[str, Any]) -> str:
    source = (
        metadata.get("source_title")
        or metadata.get("source")
        or metadata.get("source_file")
        or "Fonte institucional"
    )
    location = " > ".join(
        str(metadata[level])
        for level in ("title", "section", "subsection")
        if metadata.get(level)
    )
    return f"{source} — {location}" if location else str(source)


def retrieve(
    query: str,
    n_results: int = 3,
    *,
    filters: dict[str, str | int | float | bool] | None = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> list[RetrievedChunk]:
    """Retrieve institutional evidence with the same contract for all frameworks."""
    if not query or not query.strip():
        raise ValueError("A consulta não pode ser vazia.")
    if n_results < 1:
        raise ValueError("n_results deve ser maior que zero.")

    client = chromadb.PersistentClient(path=str(db_path))
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=DefaultEmbeddingFunction(),
        )
    except Exception as exc:
        raise RuntimeError(
            "Índice RAG indisponível. Execute: python -m shared.rag.ingest"
        ) from exc

    count = collection.count()
    if count == 0:
        return []
    query_args: dict[str, Any] = {
        "query_texts": [normalize_query(query)],
        "n_results": min(n_results, count),
        "include": ["documents", "metadatas", "distances"],
    }
    where = _where_filter(filters)
    if where:
        query_args["where"] = where
    results = collection.query(**query_args)

    documents = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    distances = results["distances"][0] if results["distances"] else []
    return [
        {
            "content": document,
            "metadata": metadata,
            "distance": float(distance),
            "citation": _citation(metadata),
        }
        for document, metadata, distance in zip(documents, metadatas, distances)
    ]


if __name__ == "__main__":
    for result in retrieve("Qual o pré-requisito de Banco de Dados II?"):
        print(f"{result['distance']:.4f} | {result['citation']}")
        print(result["content"])
