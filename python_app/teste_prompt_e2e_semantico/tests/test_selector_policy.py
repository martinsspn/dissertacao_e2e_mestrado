import unittest

from teste_prompt_e2e_semantico.application.selector_policy import (
    best_selector_for,
    selector_priority_for,
)
from teste_prompt_e2e_semantico.domain.models import UiElement


class SelectorPolicyTest(unittest.TestCase):
    def test_uses_input_submit_value_as_role_accessible_name(self) -> None:
        control = UiElement(
            page_url="https://example.test/login",
            kind="button",
            suggested_operation="click",
            element={"tag": "input", "input_type": "submit", "value": "Log in"},
        )

        selector = best_selector_for(control)

        self.assertEqual(selector.kind, "role_name")
        self.assertEqual(selector.value, "Log in")

    def test_stable_id_has_priority_over_text(self) -> None:
        by_id = UiElement(
            page_url="https://example.test/register",
            kind="button",
            suggested_operation="click",
            element={"tag": "input", "input_type": "submit", "id": "register-button", "value": "Register"},
            selectors={"id": "register-button"},
        )
        by_text = UiElement(
            page_url="https://example.test/register",
            kind="link",
            suggested_operation="click",
            element={"tag": "a", "text": "Register", "href": "/register"},
            selectors={"text": "Register", "href": "/register"},
        )

        self.assertLess(selector_priority_for(by_id), selector_priority_for(by_text))

    def test_dynamic_link_counter_uses_exact_accessible_name_instead_of_href(self) -> None:
        control = UiElement(
            page_url="https://example.test/product",
            kind="link",
            suggested_operation="click",
            element={"tag": "a", "text": "Shopping cart (0)", "href": "/cart"},
            selectors={"text": "Shopping cart (0)", "href": "/cart"},
        )

        selector = best_selector_for(control)

        self.assertEqual(selector.kind, "role_name_exact")
        self.assertEqual(selector.value, "Shopping cart")

    def test_dynamic_link_counter_still_prefers_stable_id(self) -> None:
        control = UiElement(
            page_url="https://example.test/product",
            kind="link",
            suggested_operation="click",
            element={"tag": "a", "text": "Shopping cart (0)", "href": "/cart"},
            selectors={"id": "header-cart", "href": "/cart"},
        )

        selector = best_selector_for(control)

        self.assertEqual(selector.kind, "id")
        self.assertEqual(selector.value, "header-cart")


if __name__ == "__main__":
    unittest.main()
