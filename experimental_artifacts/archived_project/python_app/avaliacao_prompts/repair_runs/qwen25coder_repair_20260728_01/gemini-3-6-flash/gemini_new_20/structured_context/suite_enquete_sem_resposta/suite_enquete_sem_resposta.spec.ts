import { test, expect } from '@playwright/test';

test.describe('Suite Enquete Sem Resposta', () => {
  test('Deve impedir a votação sem selecionar uma resposta', async ({ page }) => {
    // Etapa 1: O usuário acessa a página inicial do Demo Web Shop em um novo contexto
    await page.goto('https://demowebshop.tricentis.com/');
    await expect(page).toHaveTitle('Demo Web Shop');

    // Etapa 2: Na enquete "Do you like nopCommerce?", o usuário não seleciona resposta e clica em Vote
    const voteButton = page.locator("[id=\"vote-poll-1\"]");
    await voteButton.click();

    // Etapa 3: O sistema impede o voto e informa o usuário para selecionar uma resposta
    const errorElement = page.locator('#block-poll-vote-error-1');
    await expect(errorElement).toBeVisible();
    await expect(errorElement).toHaveText('Please select an answer');
  });
});
