import { test, expect } from '@playwright/test';
import { TripWisePage } from '../pages/TripWisePage';

test('UI loads and answers a policy question (grounded)', async ({ page }) => {
  const tripwise = new TripWisePage(page);
  await tripwise.goto();

  await tripwise.askPolicyQuestion('What are cancellation rules for non-refundable fares?');
  const answer = await tripwise.getLatestAnswerText();

  expect(answer.toLowerCase()).toContain('non-refundable');
  expect(answer).toMatch(/\[doc:[\w\-]+#\d+\]/);
});
