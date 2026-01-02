from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_engine import SimpleRAG
from app.agent import TripAgent, ask_policy

app = FastAPI(title='TripWise AI QA API', version='2.0.0')
rag = SimpleRAG(); agent = TripAgent(rag)
class AskRequest(BaseModel):
    question: str
class PlanRequest(BaseModel):
    request: str
@app.get('/health')
def health():
    return {'ok': True}
@app.post('/ask')
def ask(req: AskRequest):
    return ask_policy(rag, req.question)
@app.post('/plan')
def plan(req: PlanRequest):
    return agent.plan_trip(req.request)
