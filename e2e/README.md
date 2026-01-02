# Playwright E2E (Page Object Model)

## Why POM?
Streamlit UIs can change quickly. The Page Object Model:
- Centralizes selectors and actions in `pages/TripWisePage.ts`
- Keeps tests readable and maintainable
- Reduces the cost of UI changes

## Run
```bash
npm install
npx playwright install
UI_BASE_URL=http://localhost:8501 API_BASE_URL=http://localhost:8000 npm test
```

## Notes for interviews
- UI tests assert *behavioral outcomes* (page loads, response visible, citations present)
- Backend PyTest suite asserts deeper AI quality (grounding, hallucinations, regressions)
