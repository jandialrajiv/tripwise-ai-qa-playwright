# TripWise AI  — Playwright POM + AI Quality Gates (Travel Domain)

This repo is a portfolio-ready **AI QA automation framework** for a travel assistant (TripWise) that includes:
- **Streamlit UI** + **FastAPI API**
- **RAG + Agent workflow** (LLM mode: mock or OpenAI)
- **AI Quality tests** (grounding, hallucinations, semantic regressions)
- **Playwright E2E UI automation using Page Object Model (POM)**

---

## What’s included

### 1) Backend (Python)
- `api/main.py` — FastAPI endpoints: `/ask`, `/plan`
- `app/` — RAG engine, agent workflow, prompts, LLM client (mock/openai)
- `data/` — travel knowledge base
- `eval/` + `tests/` — AI QA tests (PyTest)

### 2) UI (Streamlit)
- `ui/app.py` — Streamlit front-end that calls the API

### 3) UI Automation (Playwright POM)
- `e2e/` — TypeScript Playwright tests using POM
  - `e2e/pages/TripWisePage.ts` — Page Object
  - `e2e/tests/*.spec.ts` — E2E tests
  - `e2e/README.md` — how to run tests + what they cover

## Quickstart (local)

### A) Start Python services
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# choose mode
export LLM_MODE=mock   # or openai + OPENAI_API_KEY

uvicorn api.main:app --reload --port 8000
streamlit run ui/app.py
```

### B) Run AI Quality tests (backend quality gates)
```bash
pytest -q
```

### C) Run Playwright UI automation (POM)
```bash
cd e2e
npm install
npx playwright install
UI_BASE_URL=http://localhost:8501 API_BASE_URL=http://localhost:8000 npm test
```

---



## CI: UI E2E Playwright
This repo includes a GitHub Actions workflow that **starts FastAPI + Streamlit** and runs Playwright tests automatically:
- `.github/workflows/ui-e2e-playwright.yml`
