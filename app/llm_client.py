"""
llm_client.py
-------------
Unified LLM client used by the app and tests.

Why this exists (AI QA leadership point):
- We separate "how we call the model" from "how we test the behavior".
- CI uses LLM_MODE=mock (deterministic, fast, cheap).
- Pre-release or staging can use LLM_MODE=openai for real behavior validation.
"""

import os
from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LLMResponse:
    text: str
    model: str

def _mock_chat(messages: List[Dict[str, str]]) -> str:
    """Deterministic mock for CI and for users without an API key."""
    user = "\n".join([m["content"] for m in messages if m["role"] == "user"])
    u = user.lower()
    if "pci" in u:
        return "PCI DSS is a security standard to protect payment card data. [doc:sample_faq#0]"
    if "baggage" in u:
        return "Standard carry-on is 1 carry-on plus 1 personal item. [doc:baggage_policy#0]"
    if "cancel" in u or "cancellation" in u:
        return ("Non-refundable fares typically are not eligible for cash refunds; "
                "a credit may be offered depending on fare rules. [doc:cancellation_policy#0]")
    if "itinerary" in u or "plan" in u:
        return ("Day 1: Downtown sights. Day 2: Museums + parks. Day 3: Neighborhoods + local food. "
                "Keep costs low by using transit and free attractions. [doc:travel_policy#0]")
    return "I don't have that information in the provided documents."

def chat(messages: List[Dict[str, str]]) -> LLMResponse:
    mode = os.getenv("LLM_MODE", "mock").lower()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if mode == "openai":
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required when LLM_MODE=openai")
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
        )
        return LLMResponse(text=resp.choices[0].message.content, model=model)

    return LLMResponse(text=_mock_chat(messages), model="mock")
