"""
agent.py
--------
Small agentic workflow for itinerary planning.
Steps: retrieve -> plan -> safety_check
"""

from dataclasses import dataclass
from typing import List, Dict, Any

from app.rag_engine import SimpleRAG
from app.llm_client import chat
from app.prompts import SYSTEM_ITINERARY, SYSTEM_RAG

@dataclass
class AgentStep:
    name: str
    status: str
    details: Dict[str, Any]

class TripAgent:
    def __init__(self, rag: SimpleRAG):
        self.rag = rag

    def plan_trip(self, request: str) -> Dict[str, Any]:
        steps: List[AgentStep] = []

        retrieved = self.rag.retrieve(request)
        steps.append(AgentStep("retrieve", "ok", {"top_k": len(retrieved)}))

        context = self.rag.context_block(retrieved)
        messages = [
            {"role": "system", "content": SYSTEM_ITINERARY},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nTASK:\n{request}"},
        ]
        llm = chat(messages)
        steps.append(AgentStep("plan", "ok", {"model": llm.model}))

        unsafe_terms = ["guaranteed price", "exact fee", "$9999"]
        lowered = llm.text.lower()
        if any(t in lowered for t in unsafe_terms):
            steps.append(AgentStep("safety_check", "fail", {"reason": "price/fee hallucination"}))
            return {"ok": False, "steps": [s.__dict__ for s in steps], "answer": llm.text}

        steps.append(AgentStep("safety_check", "ok", {}))
        return {"ok": True, "steps": [s.__dict__ for s in steps], "answer": llm.text}

def ask_policy(rag: SimpleRAG, question: str) -> Dict[str, Any]:
    retrieved = rag.retrieve(question)
    context = rag.context_block(retrieved)
    messages = [
        {"role": "system", "content": SYSTEM_RAG},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"},
    ]
    llm = chat(messages)
    return {"answer": llm.text, "model": llm.model, "retrieved": [{**c.__dict__, "score": s} for c, s in retrieved]}
