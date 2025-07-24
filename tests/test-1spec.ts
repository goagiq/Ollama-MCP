import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://127.0.0.1:8002/');
  await page.getByRole('listbox', { name: 'Ollama Model (used only if no' }).dblclick();
  await page.getByRole('option', { name: 'codegemma:latest' }).click();
  await page.getByRole('textbox', { name: 'Search Query' }).click();
  await page.getByRole('textbox', { name: 'Search Query' }).fill('find me apartment in NYC on 9/1 for under 1500');
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByRole('button', { name: 'Submit' }).click();
});