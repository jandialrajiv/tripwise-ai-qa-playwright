from app.agent import ask_policy
from eval.metrics import contains_forbidden_facts

FORBIDDEN = ['Galactic Travel Regulation','unicorn baggage fee','guaranteed price','$9999']

def test_no_forbidden_facts_in_policy_answers(rag):
    out = ask_policy(rag, 'What are cancellation rules for non-refundable fares?')
    assert not contains_forbidden_facts(out['answer'], FORBIDDEN)
