import pytest
from app.rag_engine import SimpleRAG

@pytest.fixture(scope='session')
def rag():
    return SimpleRAG()
