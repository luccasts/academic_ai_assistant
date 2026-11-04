"""Framework-independent retrieval utilities for the experiment."""
from __future__ import annotations

from typing import Any


def retrieve(*args: Any, **kwargs: Any):
    """Lazily load the retriever so the ingestion CLI has no import side effects."""
    from .retriever import retrieve as retrieve_impl

    return retrieve_impl(*args, **kwargs)


__all__ = ["retrieve"]
