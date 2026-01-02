from app.agent import ask_policy
from eval.datasets import POLICY_QA
from eval.metrics import semantic_similarity

THRESH=0.62

def test_semantic_regression_against_gold(rag):
    for row in POLICY_QA:
        out = ask_policy(rag, row['q'])
        assert semantic_similarity(out['answer'], row['gold']) >= THRESH
