from app.agent import TripAgent

def test_agent_step_order_and_no_loop(rag):
    agent = TripAgent(rag)
    out = agent.plan_trip('Plan a 3-day itinerary in Denver under $500.')
    steps = [s['name'] for s in out['steps']]
    assert steps == ['retrieve','plan','safety_check']
    assert len(steps) < 10
