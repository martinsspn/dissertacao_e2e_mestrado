import fs from 'node:fs';
import { test, expect } from './fixture';

type Mutation = {
  mutation_id: string;
  target: {
    target_id: string;
    page_url: string;
    action: string;
    tag: string;
    attributes: Record<string, string>;
  };
};

function mutationFromEnvironment(): Mutation {
  const planPath = process.env.RESILIENCE_PLAN;
  const mutationId = process.env.RESILIENCE_MUTATION_ID;
  if (!planPath || !mutationId) throw new Error('RESILIENCE_PLAN and RESILIENCE_MUTATION_ID are required');
  const plan = JSON.parse(fs.readFileSync(planPath, 'utf8')) as { mutations: Mutation[] };
  const mutation = plan.mutations.find((candidate) => candidate.mutation_id === mutationId);
  if (!mutation) throw new Error(`Unknown mutation: ${mutationId}`);
  return mutation;
}

test('differential functional control', async ({ page }, testInfo) => {
  const mutation = mutationFromEnvironment();
  const pageErrors: string[] = [];
  const failedResponses: string[] = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  page.on('response', (response) => {
    if (response.status() >= 500) failedResponses.push(`${response.status()} ${new URL(response.url()).pathname}`);
  });

  await page.goto(mutation.target.page_url);
  const target = page.locator(`[data-resilience-target="${mutation.target.target_id}"]`);
  await expect(target).toHaveCount(1);
  await expect(target).toBeVisible();

  const attributes = mutation.target.attributes;
  let supported = true;
  if (mutation.target.action === 'fill') {
    await target.fill(attributes.input_type === 'email' ? 'resilience@example.test' : 'resilience-probe');
  } else if (mutation.target.action === 'check') {
    await target.check();
  } else if (mutation.target.action === 'click') {
    if (mutation.target.tag === 'a' && attributes.href) {
      await target.click();
      await page.waitForLoadState('domcontentloaded');
    } else {
      await populateFormSafely(target);
      await target.click();
      await page.waitForTimeout(500);
    }
  } else {
    supported = false;
  }

  const observation = await page.evaluate(
    ({ targetId, supportedAction, errors, responses }) => {
      const normalized = (value: string | null | undefined) => (value || '').replace(/\s+/g, ' ').trim();
      const visibleText = (selector: string) =>
        Array.from(document.querySelectorAll(selector))
          .filter((element) => {
            const style = getComputedStyle(element);
            return style.visibility !== 'hidden' && style.display !== 'none';
          })
          .map((element) => normalized(element.textContent))
          .filter(Boolean)
          .sort();
      const marked = document.querySelector(`[data-resilience-target="${targetId}"]`) as HTMLInputElement | null;
      return {
        supported: supportedAction,
        pathname: location.pathname,
        search: location.search,
        heading: visibleText('h1').slice(0, 3),
        notifications: visibleText('#bar-notification, .validation-summary-errors, .result').slice(0, 5),
        targetPresent: Boolean(marked),
        targetValueChanged: marked ? Boolean(marked.value || marked.checked) : null,
        pageErrors: errors.slice().sort(),
        failedResponses: responses.slice().sort(),
      };
    },
    {
      targetId: mutation.target.target_id,
      supportedAction: supported,
      errors: pageErrors,
      responses: failedResponses,
    },
  );
  await testInfo.attach('resilience-control-observation', {
    body: JSON.stringify(observation, null, 2),
    contentType: 'application/json',
  });
  expect(observation.supported).toBe(true);
  expect(observation.pageErrors).toEqual([]);
  expect(observation.failedResponses).toEqual([]);
});

async function populateFormSafely(target: import('@playwright/test').Locator): Promise<void> {
  const form = target.locator('xpath=ancestor::form[1]');
  if ((await form.count()) !== 1) return;
  const seed = `${Date.now()}-${Math.floor(Math.random() * 1_000_000)}`;
  for (const input of await form.locator('input:visible:not([type=submit]):not([type=button]):not([type=hidden])').all()) {
    const type = (await input.getAttribute('type')) || 'text';
    if (['checkbox', 'radio'].includes(type)) {
      if (await input.isEnabled()) await input.check().catch(() => undefined);
      continue;
    }
    const name = ((await input.getAttribute('name')) || '').toLowerCase();
    let value = 'Resilience';
    if (type === 'email' || name.includes('email')) value = `resilience-${seed}@example.test`;
    else if (type === 'password' || name.includes('password')) value = 'Resilience123!';
    else if (name === 'q') value = 'Blue Jeans';
    else if (name.includes('zip')) value = '59000-000';
    else if (name.includes('phone')) value = '84999999999';
    if (await input.isEditable()) await input.fill(value);
  }
  for (const select of await form.locator('select:visible').all()) {
    const option = select.locator('option:not([value=""]):not([value="0"])').first();
    if ((await option.count()) === 1) await select.selectOption(await option.getAttribute('value') || undefined);
  }
}

