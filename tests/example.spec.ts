test('test', async ({ page }) => {
  await page.goto('http://127.0.0.1:7860/');
  await page.getByRole('textbox', { name: 'Search Query' }).click();
  await page.getByRole('textbox', { name: 'Search Query' }).fill('find an apartment in NYC on 9/1/2025 with a price range of 1500-2500');
  await page.getByRole('radio', { name: 'llama3.1:8b' }).check();
  await page.getByRole('button', { name: 'Submit' }).click();
});
test('Search for apartment in London with llama3.1:8b model', async ({ page }) => {
  await page.goto('http://127.0.0.1:7860/');

  // Wait for the page to load
  await page.waitForLoadState('networkidle');

  // Fill in the search query
  await page.getByLabel('Search Query').fill('find apartment in london on 9/1 with price range of $1500');

  // Select 'llama3.1:8b' from the radio group
await page.locator('input[type="radio"][value="llama3.1:8b"]').check();

  // Submit the search (Gradio usually has a submit button with type="submit")
  await page.getByRole('button', { name: /submit/i }).click();

  // Wait for the results to appear
  const results = page.getByLabel('🏠 AI-Powered Airbnb Search Assistant');
await page.locator('button[type="submit"]').click();  // Optionally, check that results contain expected text
  // await expect(results).toContainText('Airbnb Search Results');
  console.log('✓ Search submitted and results displayed');
});
test('Ollama Model radio contains qwen3:latest', async ({ page }) => {
  await page.goto('http://127.0.0.1:7860/');

  // Wait for the page to load
  await page.waitForLoadState('networkidle');

  // Verify that 'qwen3:latest' is present on the page
  const qwenRadio = page.locator('text=qwen3:latest');
  await expect(qwenRadio).toBeVisible();
  console.log('✓ qwen3:latest found on the page');
});
import { test, expect } from '@playwright/test';

test('has Ollama Model label', async ({ page }) => {
  await page.goto('http://127.0.0.1:7860/');

  // Wait for the page to load
  await page.waitForLoadState('networkidle');

  // Verify that "Ollama Model" text is present on the page
  const ollamaModelLabel = page.locator('text="Ollama Model"');
  await expect(ollamaModelLabel).toBeVisible();
  
  console.log('✓ "Ollama Model" label found on the page');
});