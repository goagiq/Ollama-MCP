import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('http://127.0.0.1:8002/');

  // Expect the page to contain "Airbnb Apartment Search"
  await expect(page.getByText('Airbnb Apartment Search')).toBeVisible();
});

test('has search functionality', async ({ page }) => {
  await page.goto('http://127.0.0.1:8002/');

  // Check if the search query textbox is present
  await expect(page.getByLabel('Search Query')).toBeVisible();
  
  // Check if the Ollama Model dropdown is present
  await expect(page.getByLabel('Ollama Model (used only if no OpenAI API key)')).toBeVisible();
});
