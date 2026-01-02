from app.agent import ask_policy
from eval.datasets import POLICY_QA

def test_policy_qa_must_contain_keywords(rag):
    for row in POLICY_QA:
        out = ask_policy(rag, row['q'])
        low = out['answer'].lower()
        for term in row['must_contain']:
            assert term.lower() in low
