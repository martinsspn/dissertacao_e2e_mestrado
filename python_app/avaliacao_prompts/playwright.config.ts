import { defineConfig } from '@playwright/test';

/**
 * Configuração exclusiva da ferramenta auxiliar de avaliação.
 * Usa o Chromium completo já instalado, evitando depender do headless shell.
 */
export default defineConfig({
  testDir: process.env.RESILIENCE_TEST_DIR || '../teste_prompt_e2e_semantico/generated_tests',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 20_000,
  expect: {
    timeout: 7_000,
  },
  outputDir: '/tmp/avaliacao-prompts-playwright',
  use: {
    baseURL:
      process.env.PROMPT_E2E_BASE_URL ||
      'https://demowebshop.tricentis.com/',
    browserName: 'chromium',
    channel: 'chromium',
    headless: true,
    ignoreHTTPSErrors: true,
    trace: process.env.RESILIENCE_CAPTURE_EVIDENCE === '1' ? 'on' : 'off',
    screenshot: process.env.RESILIENCE_CAPTURE_EVIDENCE === '1' ? 'on' : 'off',
    navigationTimeout: 15_000,
    actionTimeout: 10_000,
  },
});
