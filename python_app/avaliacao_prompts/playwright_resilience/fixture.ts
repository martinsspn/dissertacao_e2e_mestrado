import fs from 'node:fs';
import { test as base, expect } from '@playwright/test';

type CatalogTarget = {
  target_id: string;
  page_url: string;
  tag: string;
  attributes: Record<string, string>;
};

type PlannedMutation = {
  mutation_id: string;
  stratum: string;
  operator: string;
  target: CatalogTarget;
  parameters: Record<string, string>;
};

type MutationEvent = {
  mutationId: string;
  targetId: string;
  url: string;
  status: 'applied' | 'marked' | 'interacted' | 'missing' | 'ambiguous' | 'error';
  detail?: string;
};

declare global {
  interface Window {
    __recordResilienceMutation?: (event: MutationEvent) => void;
    __resilienceMutationFinished?: boolean;
  }
}

function selectedMutation(): PlannedMutation | null {
  const mutationId = process.env.RESILIENCE_MUTATION_ID;
  const planPath = process.env.RESILIENCE_PLAN;
  if (!mutationId || !planPath) return null;
  const plan = JSON.parse(fs.readFileSync(planPath, 'utf8')) as { mutations: PlannedMutation[] };
  const mutation = plan.mutations.find((candidate) => candidate.mutation_id === mutationId);
  if (!mutation) throw new Error(`Mutation not found in frozen plan: ${mutationId}`);
  return mutation;
}

const mutation = selectedMutation();
const controlOnly = process.env.RESILIENCE_CONTROL_ONLY === '1';

export const test = base.extend({
  page: async ({ page }, use, testInfo) => {
    const events: MutationEvent[] = [];
    if (mutation) {
      await page.exposeFunction('__recordResilienceMutation', (event: MutationEvent) => events.push(event));
      await page.addInitScript(applyPlannedMutation, { mutation, controlOnly });
    }
    await use(page);
    await testInfo.attach('resilience-mutation-events', {
      body: JSON.stringify(events, null, 2),
      contentType: 'application/json',
    });
  },
});

export { expect };

/**
 * Esta função é serializada pelo Playwright e executada dentro de cada novo
 * documento. Por isso, todos os auxiliares permanecem deliberadamente locais.
 */
function applyPlannedMutation(instruction: { mutation: PlannedMutation; controlOnly: boolean }): void {
  const { mutation, controlOnly } = instruction;
  const record = (status: MutationEvent['status'], detail = '') => {
    window.__recordResilienceMutation?.({
      mutationId: mutation.mutation_id,
      targetId: mutation.target.target_id,
      url: window.location.href,
      status,
      detail,
    });
  };

  const samePage = (): boolean => {
    if (!mutation.target.page_url) return false;
    const expected = new URL(mutation.target.page_url);
    return expected.origin === window.location.origin && expected.pathname === window.location.pathname;
  };

  const exactText = (element: Element, expected: string): boolean =>
    (element.textContent || '').replace(/\s+/g, ' ').trim() === expected.replace(/\s+/g, ' ').trim();

  const findCandidates = (): Element[] => {
    const attributes = mutation.target.attributes;
    const tag = mutation.target.tag || '*';
    if (attributes.id) {
      const element = document.getElementById(attributes.id);
      return element ? [element] : [];
    }
    const candidates = Array.from(document.querySelectorAll(tag));
    const byAttributes = candidates.filter((element) => {
      if (attributes.name && element.getAttribute('name') !== attributes.name) return false;
      if (attributes.href) {
        const actual = element.getAttribute('href') || '';
        if (actual !== attributes.href && new URL(actual, window.location.origin).pathname !== attributes.href) return false;
      }
      if (attributes.input_type && element.getAttribute('type') !== attributes.input_type) return false;
      if (attributes.value && element.getAttribute('value') !== attributes.value) return false;
      if (attributes.text && !exactText(element, attributes.text)) return false;
      return true;
    });
    if (byAttributes.length || !attributes.label) return byAttributes;
    const labels = Array.from(document.querySelectorAll('label')).filter((label) => exactText(label, attributes.label));
    return labels
      .map((label) => {
        const htmlFor = (label as HTMLLabelElement).htmlFor;
        return htmlFor ? document.getElementById(htmlFor) : label.querySelector(tag);
      })
      .filter((element): element is Element => Boolean(element));
  };

  const preserveComputedPresentation = (element: HTMLElement) => {
    const computed = window.getComputedStyle(element);
    for (const property of Array.from(computed)) {
      element.style.setProperty(property, computed.getPropertyValue(property), computed.getPropertyPriority(property));
    }
  };

  const updateIdReferences = (oldValue: string, newValue: string) => {
    for (const attribute of ['for', 'aria-controls', 'aria-describedby', 'aria-labelledby']) {
      for (const element of Array.from(document.querySelectorAll(`[${attribute}]`))) {
        const tokens = (element.getAttribute(attribute) || '').split(/\s+/);
        if (tokens.includes(oldValue)) {
          element.setAttribute(attribute, tokens.map((token) => (token === oldValue ? newValue : token)).join(' '));
        }
      }
    }
  };

  const mutate = (element: HTMLElement) => {
    element.dataset.resilienceTarget = mutation.target.target_id;
    const parameters = mutation.parameters;
    switch (mutation.operator) {
      case 'insert_wrapper': {
        const wrapper = document.createElement(parameters.tag || 'div');
        wrapper.dataset.resilienceWrapper = mutation.mutation_id;
        wrapper.style.display = 'contents';
        element.parentNode?.insertBefore(wrapper, element);
        wrapper.appendChild(element);
        break;
      }
      case 'insert_noninteractive_sibling_before': {
        const sibling = document.createElement(parameters.tag || 'span');
        sibling.dataset.resilienceSibling = mutation.mutation_id;
        sibling.hidden = true;
        sibling.setAttribute('aria-hidden', 'true');
        element.parentNode?.insertBefore(sibling, element);
        break;
      }
      case 'rename_id': {
        const oldValue = element.id;
        preserveComputedPresentation(element);
        updateIdReferences(oldValue, parameters.new_value);
        element.id = parameters.new_value;
        break;
      }
      case 'rename_class': {
        preserveComputedPresentation(element);
        element.classList.remove(parameters.old_value);
        element.classList.add(parameters.new_value);
        break;
      }
      case 'input_submit_to_button': {
        const input = element as HTMLInputElement;
        preserveComputedPresentation(input);
        const button = document.createElement('button');
        for (const attribute of Array.from(input.attributes)) {
          if (!['type', 'value', 'data-resilience-target'].includes(attribute.name)) {
            button.setAttribute(attribute.name, attribute.value);
          }
        }
        button.type = 'submit';
        button.value = input.value;
        button.textContent = input.value;
        button.dataset.resilienceTarget = mutation.target.target_id;
        input.replaceWith(button);
        break;
      }
      case 'change_accessible_name': {
        const suffix = parameters.suffix || ' updated';
        const attributes = mutation.target.attributes;
        if (attributes.label) {
          const label = Array.from(document.querySelectorAll('label')).find((candidate) =>
            exactText(candidate, attributes.label),
          );
          if (label) label.textContent = `${label.textContent || ''}${suffix}`;
          else element.setAttribute('aria-label', `${attributes.label}${suffix}`);
        } else if (element.hasAttribute('aria-label')) {
          element.setAttribute('aria-label', `${element.getAttribute('aria-label') || ''}${suffix}`);
        } else if (element instanceof HTMLInputElement && ['submit', 'button'].includes(element.type)) {
          element.value = `${element.value}${suffix}`;
        } else if (attributes.text) {
          element.textContent = `${element.textContent || ''}${suffix}`;
        } else if (attributes.value) {
          element.setAttribute('aria-label', `${attributes.value}${suffix}`);
        }
        break;
      }
      case 'rename_test_id': {
        const current = element.getAttribute('data-testid');
        if (current) element.setAttribute('data-testid', parameters.new_value);
        break;
      }
      default:
        throw new Error(`Unsupported operator: ${mutation.operator}`);
    }
  };

  const instrumentInteractions = (element: HTMLElement) => {
    for (const eventName of ['click', 'input', 'change']) {
      element.addEventListener(
        eventName,
        () => record('interacted', eventName),
        { capture: true },
      );
    }
  };

  const attempt = () => {
    if (window.__resilienceMutationFinished || !samePage()) return;
    const candidates = findCandidates();
    if (candidates.length === 0) return;
    window.__resilienceMutationFinished = true;
    if (candidates.length > 1) {
      record('ambiguous', `${candidates.length} bootstrap candidates`);
      return;
    }
    try {
      const target = candidates[0] as HTMLElement;
      target.dataset.resilienceTarget = mutation.target.target_id;
      if (controlOnly) {
        instrumentInteractions(target);
        record('marked');
      }
      else {
        mutate(target);
        const mutatedTarget = document.querySelector(
          `[data-resilience-target="${mutation.target.target_id}"]`,
        ) as HTMLElement | null;
        if (mutatedTarget) instrumentInteractions(mutatedTarget);
        record('applied');
      }
    } catch (error) {
      record('error', error instanceof Error ? error.message : String(error));
    }
  };

  const start = () => {
    attempt();
    if (!window.__resilienceMutationFinished) {
      const observer = new MutationObserver(() => {
        attempt();
        if (window.__resilienceMutationFinished) observer.disconnect();
      });
      observer.observe(document.documentElement, { childList: true, subtree: true });
      window.setTimeout(() => {
        observer.disconnect();
        if (!window.__resilienceMutationFinished && samePage()) record('missing');
      }, 5000);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
}
