"""
rag_engine.py
-------------
Local-doc RAG engine:
- Loads /data docs
- Chunks them
- Embeds chunks
- Retrieves top-k chunks for a query
"""

import os
import glob
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Chunk:
    doc_id: str
    chunk_id: int
    text: str

class SimpleRAG:
    def __init__(self, data_dir: str = "data", chunk_size: int = 500, overlap: int = 60):
        self.data_dir = data_dir
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chunks: List[Chunk] = []
        self.embeddings: np.ndarray | None = None
        self._load()

    def _load(self) -> None:
        files = sorted(glob.glob(os.path.join(self.data_dir, "*.md")) + glob.glob(os.path.join(self.data_dir, "*.txt")))
        chunks: List[Chunk] = []
        for fp in files:
            doc_id = os.path.splitext(os.path.basename(fp))[0]
            txt = open(fp, "r", encoding="utf-8").read().strip()
            for i, c in enumerate(self._chunk_text(txt)):
                chunks.append(Chunk(doc_id=doc_id, chunk_id=i, text=c))
        self.chunks = chunks
        self.embeddings = self.model.encode([c.text for c in chunks], normalize_embeddings=True) if chunks else np.zeros((0, 384), dtype=np.float32)

    def _chunk_text(self, txt: str) -> List[str]:
        out = []
        start = 0
        while start < len(txt):
            end = min(len(txt), start + self.chunk_size)
            out.append(txt[start:end])
            start = max(0, end - self.overlap)
            if end == len(txt):
                break
        return out

    def retrieve(self, query: str, top_k: int | None = None) -> List[Tuple[Chunk, float]]:
        if top_k is None:
            top_k = int(os.getenv("TOP_K", "4"))
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        q = self.model.encode([query], normalize_embeddings=True)
        sims = cosine_similarity(q, self.embeddings)[0]
        idx = np.argsort(-sims)[:top_k]
        return [(self.chunks[i], float(sims[i])) for i in idx]

    def context_block(self, retrieved: List[Tuple[Chunk, float]]) -> str:
        lines = []
        for chunk, score in retrieved:
            lines.append(f"[doc:{chunk.doc_id}#{chunk.chunk_id} score={score:.3f}]\n{chunk.text}\n")
        return "\n".join(lines)
