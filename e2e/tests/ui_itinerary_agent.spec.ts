import { test, expect } from '@playwright/test';
import { TripWisePage } from '../pages/TripWisePage';

test('UI can generate itinerary (agent workflow)', async ({ page }) => {
  const tripwise = new TripWisePage(page);
  await tripwise.goto();

  await tripwise.planItinerary('Plan a 3-day itinerary in Denver under $500.');
  const itinerary = await tripwise.getLatestItineraryText();

  expect(itinerary.length).toBeGreaterThan(20);
  expect(itinerary.toLowerCase()).not.toContain('guaranteed price');
});
