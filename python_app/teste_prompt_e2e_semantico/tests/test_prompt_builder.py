from pathlib import Path
import unittest

from teste_prompt_e2e_semantico.application.prompt_builder import build_structured_prompt
from teste_prompt_e2e_semantico.domain.models import (
    ContextElement,
    InteractionContext,
    ObservedResult,
    PageEvidence,
    SelectorCandidate,
    SpecPlan,
    SpecificationStep,
    StepContext,
    StructuredContext,
)


class PromptBuilderTest(unittest.TestCase):
    def test_structured_prompt_groups_compact_context_by_step(self) -> None:
        spec = SpecPlan(Path("cart.txt"), "Add Blue Jeans to cart.", "cart")
        steps = [
            SpecificationStep("R1", "Open Blue Jeans."),
            SpecificationStep("R2", "Select Add to cart."),
        ]
        context = StructuredContext(
            steps=[
                StepContext(
                    "R1",
                    (
                        InteractionContext(
                            ContextElement(
                                "https://example.test/search",
                                "click",
                                "link",
                                {"tag": "a", "text": "Blue Jeans", "href": "/blue-jeans"},
                                SelectorCandidate("text", "Blue Jeans"),
                                "https://example.test/blue-jeans",
                            )
                        ),
                    ),
                ),
                StepContext(
                    "R2",
                    (
                        InteractionContext(
                            ContextElement(
                                "https://example.test/blue-jeans",
                                "click",
                                "button",
                                {"tag": "input", "id": "add-to-cart-button-36", "value": "Add to cart"},
                                SelectorCandidate("id", "add-to-cart-button-36"),
                            ),
                            ObservedResult("Added to cart", "bar-notification", "alert"),
                        ),
                    ),
                ),
            ]
        )

        prompt = build_structured_prompt(spec, "https://example.test", steps, context)

        self.assertIn("Contexto estruturado por etapa", prompt)
        self.assertIn("Etapa 1 (R1)", prompt)
        self.assertIn("controle=tag=a, text=Blue Jeans, href=/blue-jeans", prompt)
        self.assertIn("destino=https://example.test/blue-jeans", prompt)
        self.assertIn("resultado_observado=Added to cart", prompt)
        self.assertIn("um unico bloco de codigo `typescript`, sem texto fora dele", prompt)
        self.assertIn("arquivo Playwright `.spec.ts` completo e executavel", prompt)
        self.assertIn("await page.goto('https://example.test/')", prompt)
        self.assertIn("URLs literais tambem em `toHaveURL`", prompt)
        self.assertIn("sem regex ou links Markdown", prompt)
        self.assertIn("Nao derive rotas do texto de links", prompt)
        self.assertIn("Use `toHaveURL` somente quando a URL exata", prompt)
        self.assertIn("confirme a pagina por elementos visiveis", prompt)
        self.assertIn("locators Playwright legiveis e unicos no modo estrito", prompt)
        self.assertIn("Cada valor `locator_playwright=...`", prompt)
        self.assertIn("preserve esse locator", prompt)
        self.assertIn("nao o substitua por um locator generico", prompt)
        self.assertIn("Nunca passe uma expressao `page.getBy*`", prompt)
        self.assertIn("nem invente engines como `role_name:`", prompt)
        self.assertIn(
            'locator_playwright=page.getByText("Blue Jeans", { exact: true }).first()',
            prompt,
        )
        self.assertIn(
            'locator_playwright=page.locator("[id=\\"add-to-cart-button-36\\"]")',
            prompt,
        )
        self.assertIn(
            'locator_playwright_resultado=page.locator("[id=\\"bar-notification\\"]")',
            prompt,
        )
        self.assertIn("varios itens ou variantes compartilharem a mesma acao", prompt)
        self.assertIn("nao trate o titulo da pagina agrupadora como nome do item", prompt)
        self.assertIn("sem inventar um rotulo", prompt)
        self.assertIn("contexto é apenas um guia", prompt)
        self.assertIn("experiencia para navegar", prompt)
        self.assertIn("Caso seja possível acessar a aplicação", prompt)
        self.assertIn("sem afirmar que executou acoes", prompt)
        self.assertIn("sem limitar o teste a elas", prompt)
        self.assertNotIn("Caminho navegacional", prompt)
        self.assertNotIn("coverage", prompt.casefold())
        self.assertNotIn("score", prompt.casefold())

    def test_does_not_render_form_action_as_observed_navigation(self) -> None:
        spec = SpecPlan(Path("register.txt"), "Submit registration.", "register")
        steps = [SpecificationStep("R1", "Select Register.")]
        context = StructuredContext(
            [
                StepContext(
                    "R1",
                    (
                        InteractionContext(
                            ContextElement(
                                "https://example.test/register",
                                "click",
                                "button",
                                {
                                    "tag": "input",
                                    "id": "register-button",
                                    "value": "Register",
                                    "form_action": "/register",
                                },
                                SelectorCandidate("id", "register-button"),
                                "https://example.test/register",
                            )
                        ),
                    ),
                )
            ]
        )

        prompt = build_structured_prompt(spec, "https://example.test", steps, context)

        self.assertIn("form_action=/register", prompt)
        self.assertNotIn("- destino=", prompt)

    def test_renders_exact_role_name_as_executable_playwright_locator(self) -> None:
        spec = SpecPlan(Path("cart.txt"), "Open the shopping cart.", "cart")
        steps = [SpecificationStep("R1", "Open the shopping cart.")]
        context = StructuredContext(
            [
                StepContext(
                    "R1",
                    (
                        InteractionContext(
                            ContextElement(
                                "https://example.test/product",
                                "click",
                                "link",
                                {"tag": "a", "text": "Shopping cart", "href": "/cart"},
                                SelectorCandidate("role_name_exact", "Shopping cart"),
                                "https://example.test/cart",
                            )
                        ),
                    ),
                )
            ]
        )

        prompt = build_structured_prompt(spec, "https://example.test", steps, context)

        self.assertIn(
            'locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })',
            prompt,
        )

    def test_numbers_multiple_interactions_without_repeating_graph_paths(self) -> None:
        spec = SpecPlan(Path("search.txt"), "Search for Blue Jeans.", "search")
        steps = [SpecificationStep("R1", "The user searches for Blue Jeans.")]
        context = StructuredContext(
            [
                StepContext(
                    "R1",
                    (
                        InteractionContext(
                            ContextElement(
                                "https://example.test/",
                                "fill",
                                "text_input",
                                {"tag": "input", "id": "small-searchterms"},
                                SelectorCandidate("id", "small-searchterms"),
                            )
                        ),
                        InteractionContext(
                            ContextElement(
                                "https://example.test/",
                                "click",
                                "button",
                                {"tag": "input", "input_type": "submit", "value": "Search"},
                                SelectorCandidate("role_name", "Search"),
                            )
                        ),
                    ),
                )
            ]
        )

        prompt = build_structured_prompt(spec, "https://example.test", steps, context)

        self.assertIn("controle_1=tag=input, id=small-searchterms", prompt)
        self.assertIn("operacao_1=fill", prompt)
        self.assertIn("controle_2=tag=input, input_type=submit, value=Search", prompt)
        self.assertIn("operacao_2=click", prompt)
        self.assertIn(
            'locator_playwright_1=page.locator("[id=\\"small-searchterms\\"]")',
            prompt,
        )
        self.assertIn(
            'locator_playwright_2=page.getByRole("button", { name: "Search", exact: true })',
            prompt,
        )
        self.assertEqual(prompt.count("- pagina=https://example.test/"), 1)
        self.assertNotIn("pagina_1=", prompt)
        self.assertNotIn("pagina_2=", prompt)
        self.assertNotIn("Caminho navegacional", prompt)

    def test_never_renders_internal_selector_dsl_as_locator(self) -> None:
        spec = SpecPlan(Path("register.txt"), "Register a user.", "register")
        steps = [SpecificationStep("R1", "Fill Email and submit Register.")]
        context = StructuredContext(
            [
                StepContext(
                    "R1",
                    (
                        InteractionContext(
                            ContextElement(
                                "https://example.test/register",
                                "fill",
                                "text_input",
                                {"tag": "input", "label": "Email:"},
                                SelectorCandidate("label", "Email:"),
                            )
                        ),
                        InteractionContext(
                            ContextElement(
                                "https://example.test/register",
                                "click",
                                "button",
                                {"tag": "input", "input_type": "submit", "id": "register-button"},
                                SelectorCandidate("id", "register-button"),
                            )
                        ),
                    ),
                )
            ]
        )

        prompt = build_structured_prompt(spec, "https://example.test", steps, context)
        locator_lines = [
            line for line in prompt.splitlines() if line.startswith("- locator_playwright")
        ]

        self.assertEqual(len(locator_lines), 2)
        self.assertTrue(all("=page." in line for line in locator_lines))
        self.assertNotIn("=label:", prompt)
        self.assertNotIn("=id:", prompt)
        self.assertNotIn("=role_name:", prompt)

    def test_structured_prompt_reports_empty_context_explicitly(self) -> None:
        spec = SpecPlan(Path("contact.txt"), "Acessar Contact Us.", "contact")
        steps = [SpecificationStep("R1", "Acessar Contact Us.")]

        prompt = build_structured_prompt(spec, "https://example.test", steps, StructuredContext([StepContext("R1")]))

        self.assertIn("Nenhum controle ou resultado correspondente foi observado", prompt)

    def test_structured_prompt_renders_compact_page_evidence(self) -> None:
        spec = SpecPlan(Path("details.txt"), "Show Blue Jeans.", "details")
        steps = [SpecificationStep("R1", "The system displays Blue Jeans.")]
        context = StructuredContext(
            [
                StepContext(
                    "R1",
                    page_evidence=PageEvidence(
                        "https://example.test/blue-jeans",
                        "h1",
                        "Blue Jeans",
                    ),
                )
            ]
        )

        prompt = build_structured_prompt(spec, "https://example.test", steps, context)

        self.assertIn("pagina_evidencia=https://example.test/blue-jeans", prompt)
        self.assertIn("evidencia_pagina=h1:Blue Jeans", prompt)
        self.assertIn("pagina_evidencia` nao comprova uma transicao", prompt)
        self.assertNotIn("Etapas sem contexto observado", prompt)
