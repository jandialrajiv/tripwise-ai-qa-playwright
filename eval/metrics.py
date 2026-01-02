import re
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(a: str, b: str) -> float:
    emb = _model.encode([a, b], normalize_embeddings=True)
    return float(cosine_similarity([emb[0]], [emb[1]])[0][0])

CITATION_RE = re.compile(r"\[doc:([\w\-]+)#(\d+)\]")

def extract_citations(text: str) -> List[Tuple[str, int]]:
    return [(m.group(1), int(m.group(2))) for m in CITATION_RE.finditer(text)]

def groundedness_score(answer: str, context: str) -> float:
    if not extract_citations(answer):
        return 0.0
    return semantic_similarity(answer, context)

def contains_forbidden_facts(answer: str, forbidden: List[str]) -> bool:
    low = answer.lower()
    return any(f.lower() in low for f in forbidden)
