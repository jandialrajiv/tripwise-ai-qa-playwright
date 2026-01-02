import { Page, Locator, expect } from '@playwright/test';

/**
 * Page Object Model for the Streamlit UI.
 * Centralizes selectors and actions so tests remain maintainable.
 */
export class TripWisePage {
  readonly page: Page;
  readonly policyQuestionInput: Locator;
  readonly askButton: Locator;
  readonly itineraryRequestTextarea: Locator;
  readonly planTripButton: Locator;
  readonly answerHeading: Locator;
  readonly itineraryHeading: Locator;

  constructor(page: Page) {
    this.page = page;

    // Prefer label-based locators (more resilient for Streamlit apps)
    this.policyQuestionInput = page.getByLabel('Question', { exact: true });
    this.askButton = page.getByRole('button', { name: 'Ask' });

    this.itineraryRequestTextarea = page.getByLabel('Trip request', { exact: true });
    this.planTripButton = page.getByRole('button', { name: 'Plan trip' });

    this.answerHeading = page.getByRole('heading', { name: 'Answer' });
    this.itineraryHeading = page.getByRole('heading', { name: 'Itinerary' });
  }

  async goto() {
    await this.page.goto('/');
    await expect(this.page.getByRole('heading', { name: /TripWise AI/i })).toBeVisible();
  }

  async askPolicyQuestion(question: string) {
    await this.policyQuestionInput.fill(question);
    await this.askButton.click();
    await expect(this.answerHeading).toBeVisible();
  }

  async planItinerary(request: string) {
    await this.itineraryRequestTextarea.fill(request);
    await this.planTripButton.click();
    await expect(this.itineraryHeading).toBeVisible();
  }

  async getLatestAnswerText(): Promise<string> {
    const container = this.answerHeading.locator('..');
    return await container.innerText();
  }

  async getLatestItineraryText(): Promise<string> {
    const container = this.itineraryHeading.locator('..');
    return await container.innerText();
  }
}
