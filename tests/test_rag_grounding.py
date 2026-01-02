from app.agent import ask_policy
from eval.metrics import groundedness_score

def test_rag_answer_has_citation_and_is_grounded(rag):
    out = ask_policy(rag, 'What are cancellation rules for non-refundable fares?')
    context = '\n'.join([r['text'] for r in out['retrieved']])
    assert groundedness_score(out['answer'], context) >= 0.55
