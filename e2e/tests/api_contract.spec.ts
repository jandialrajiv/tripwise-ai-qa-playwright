import { test, expect } from '@playwright/test';

const API = process.env.API_BASE_URL || 'http://localhost:8000';

test('API health is OK', async ({ request }) => {
  const res = await request.get(`${API}/health`);
  expect(res.ok()).toBeTruthy();
  const data = await res.json();
  expect(data.ok).toBeTruthy();
});

test('API /ask returns answer with citation', async ({ request }) => {
  const res = await request.post(`${API}/ask`, { data: { question: 'What is the baggage policy for domestic flights?' } });
  expect(res.ok()).toBeTruthy();
  const data = await res.json();
  expect(typeof data.answer).toBe('string');
  expect(data.answer).toMatch(/\[doc:[\w\-]+#\d+\]/);
});
