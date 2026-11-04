"""Build the shared, framework-independent institutional knowledge index."""
from __future__ import annotations

import argparse
import hashlib
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import chromadb
import frontmatter
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langchain_text_splitters import MarkdownHeaderTextSplitter

SHARED_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = SHARED_DIR / "knowledge"
DEFAULT_DB_PATH = SHARED_DIR / "rag" / "chroma_db"
COLLECTION_NAME = "institutional-knowledge-v1"
HEADERS = [("#", "title"), ("##", "section"), ("###", "subsection")]
ACADEMIC_PERIOD = re.compile(r"\b20\d{2}\.[12]\b")


def _metadata_value(value: Any) -> str | int | float | bool:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _chunk_id(document_id: str, headings: list[str], content: str) -> str:
    identity = "\n".join((document_id, *headings, content))
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def load_chunks(
    knowledge_dir: Path = KNOWLEDGE_DIR,
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    """Load every Markdown source and return stable IDs, texts and metadata."""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS, strip_headers=True
    )
    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict[str, Any]] = []

    for path in sorted(knowledge_dir.rglob("*.md")):
        post = frontmatter.load(path)
        document_id = path.relative_to(knowledge_dir).as_posix().lower()
        base_metadata = {
            key: _metadata_value(value) for key, value in post.metadata.items()
        }
        base_metadata.update({"document_id": document_id, "source_file": document_id})
        for chunk in splitter.split_text(post.content):
            headings = [
                chunk.metadata.get(level, "")
                for level in ("title", "section", "subsection")
            ]
            headings = [heading for heading in headings if heading]
            text = "\n\n".join((*headings, chunk.page_content)).strip()
            if text:
                metadata = {**base_metadata, **chunk.metadata}
                period = ACADEMIC_PERIOD.search(" ".join(headings))
                if period:
                    metadata["academic_period"] = period.group()
                ids.append(_chunk_id(document_id, headings, chunk.page_content))
                documents.append(text)
                metadatas.append(metadata)

    if not documents:
        raise ValueError(f"Nenhum documento Markdown encontrado em {knowledge_dir}")
    return ids, documents, metadatas


def get_collection(db_path: Path = DEFAULT_DB_PATH):
    """Open the collection with the embedding function fixed for the experiment."""
    client = chromadb.PersistentClient(path=str(db_path))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),
        metadata={
            "embedding_model": "all-MiniLM-L6-v2",
            "corpus": "shared/knowledge",
            "schema_version": 1,
        },
    )


def ingest(
    knowledge_dir: Path = KNOWLEDGE_DIR,
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    """Synchronize the collection with the Markdown knowledge directory."""
    ids, documents, metadatas = load_chunks(knowledge_dir)
    collection = get_collection(db_path)
    stale = sorted(set(collection.get(include=[])["ids"]) - set(ids))
    if stale:
        collection.delete(ids=stale)
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    return len(ids)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--knowledge-dir", type=Path, default=KNOWLEDGE_DIR)
    parser.add_argument("--db-path", type=Path, default=DEFAULT_DB_PATH)
    args = parser.parse_args()
    count = ingest(args.knowledge_dir, args.db_path)
    print(f"INFO: {count} chunks sincronizados em '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    main()
