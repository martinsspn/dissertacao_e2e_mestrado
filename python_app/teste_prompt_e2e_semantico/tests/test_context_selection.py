import unittest

from teste_prompt_e2e_semantico.application.context_selection import select_structured_context
from teste_prompt_e2e_semantico.domain.models import (
    NavigationGraph,
    NavigationTransition,
    ObservedResult,
    PageNode,
    SpecificationStep,
    UiElement,
)


class ContextSelectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.home = "https://example.test/"
        self.search = "https://example.test/search"
        self.product = "https://example.test/blue-jeans"
        self.cart = "https://example.test/cart"
        self.search_input = _control(
            self.home,
            "text_input",
            "fill",
            tag="input",
            id="small-searchterms",
            name="q",
            value="Search store",
            form_action="/search",
            form_method="GET",
        )
        self.graph = NavigationGraph(
            pages=[
                PageNode("home", self.home, "Home"),
                PageNode("search", self.search, "Search"),
                PageNode("product", self.product, "Blue Jeans"),
                PageNode("cart", self.cart, "Shopping cart"),
            ],
            transitions=[
                NavigationTransition(
                    source={"url": self.product, "title": "Blue Jeans"},
                    target={"url": self.product, "title": "Blue Jeans"},
                    action="click",
                    interaction_kind="button",
                    element={"tag": "input", "id": "add-to-cart-button-36", "input_type": "button"},
                    selectors={"id": "add-to-cart-button-36"},
                    observed_result=ObservedResult(
                        "The product has been added to your shopping cart",
                        "bar-notification",
                        "alert",
                    ),
                )
            ],
            ui_elements=[
                self.search_input,
                _control(
                    self.home,
                    "button",
                    "click",
                    tag="input",
                    value="Search",
                    input_type="submit",
                    form_action="/search",
                    form_method="GET",
                ),
                _control(self.search, "link", "click", tag="a", text="Blue Jeans", href="/blue-jeans"),
                _control(
                    self.product,
                    "button",
                    "click",
                    tag="input",
                    id="add-to-cart-button-36",
                    value="Add to cart",
                    input_type="button",
                ),
                _control(self.product, "link", "click", tag="a", text="Shopping cart(0)", href="/cart"),
                _control("https://example.test/notebooks", "link", "click", tag="a", text="Shopping cart(0)", href="/cart"),
                _control(self.cart, "link", "click", tag="a", text="Blue Jeans", href="/blue-jeans"),
            ],
        )

    def test_associates_related_controls_without_unrelated_paths_or_duplicates(self) -> None:
        requirements = [
            SpecificationStep("R1", "The user searches for Blue Jeans in the Search store field."),
            SpecificationStep("R2", "The user opens Blue Jeans in the search results."),
            SpecificationStep("R3", "The user selects Add to cart on the product page."),
            SpecificationStep("R4", "The system informs that the product was added to the cart."),
            SpecificationStep("R5", "The user accesses Shopping cart."),
            SpecificationStep("R6", "The system displays Blue Jeans among the cart items."),
        ]

        context = select_structured_context(self.graph, self.home, requirements)

        self.assertEqual(
            [control.element.get("id") or control.element.get("value") for control in context.steps[0].controls],
            ["small-searchterms", "Search"],
        )
        self.assertEqual(context.steps[1].control.page_url, self.search)
        self.assertEqual(context.steps[2].control.element["id"], "add-to-cart-button-36")
        self.assertEqual(
            context.steps[2].observed_result.text,
            "The product has been added to your shopping cart",
        )
        self.assertIsNone(context.steps[3].control)
        self.assertEqual(context.steps[4].control.element["href"], "/cart")
        self.assertEqual(context.steps[4].control.selector.kind, "role_name_exact")
        self.assertEqual(context.steps[4].control.selector.value, "Shopping cart")
        self.assertIsNone(context.steps[5].control)
        self.assertFalse(any(step.control and "notebooks" in step.control.page_url for step in context.steps))
        self.assertEqual(context.item_count, 8)

    def test_returns_empty_step_context_when_literal_label_is_absent(self) -> None:
        context = select_structured_context(
            self.graph,
            self.home,
            [SpecificationStep("R1", "The user consults invoices.")],
        )

        self.assertEqual(context.item_count, 0)
        self.assertIsNone(context.steps[0].control)

    def test_following_action_disambiguates_a_partially_named_product_page(self) -> None:
        product_url = "https://example.test/digital-slr-camera"
        graph = NavigationGraph(
            pages=[
                PageNode("home", self.home, "Home", h1="Home"),
                PageNode(
                    "camera",
                    product_url,
                    "Demo Shop. Digital SLR Camera 12.2 Mpixel",
                    h1="Digital SLR Camera 12.2 Mpixel",
                ),
                PageNode("book", "https://example.test/fiction", "Fiction", h1="Fiction"),
            ],
            transitions=[],
            ui_elements=[
                _control(
                    product_url,
                    "button",
                    "click",
                    tag="input",
                    id="add-to-wishlist-button-18",
                    value="Add to wishlist",
                    input_type="button",
                ),
                _control(
                    product_url,
                    "button",
                    "click",
                    tag="input",
                    id="add-to-wishlist-button-19",
                    value="Add to wishlist",
                    input_type="button",
                ),
                _control(
                    "https://example.test/fiction",
                    "button",
                    "click",
                    tag="input",
                    id="add-to-wishlist-button-45",
                    value="Add to wishlist",
                    input_type="button",
                ),
            ],
        )
        requirements = [
            SpecificationStep("R1", "The user opens a Camera product presented in the results."),
            SpecificationStep("R2", "The user selects Add to wishlist on the product page."),
        ]

        context = select_structured_context(graph, self.home, requirements)

        self.assertEqual(context.steps[0].page_evidence.page_url, product_url)
        self.assertEqual(
            context.steps[0].page_evidence.text,
            "Digital SLR Camera 12.2 Mpixel",
        )
        self.assertEqual(context.steps[1].control.page_url, product_url)
        self.assertEqual(
            context.steps[1].control.selector.value,
            "add-to-wishlist-button-18",
        )

    def test_does_not_use_incidental_single_word_labels(self) -> None:
        sparse_graph = NavigationGraph(
            pages=[PageNode("home", self.home, "Home")],
            transitions=[],
            ui_elements=[
                _control(self.home, "link", "click", tag="a", text="Search", href="/search"),
                _control(self.home, "link", "click", tag="a", text="jeans", href="/producttag/14/jeans"),
            ],
        )

        context = select_structured_context(
            sparse_graph,
            self.home,
            [
                SpecificationStep("R1", "The user opens Blue Jeans in the search results."),
                SpecificationStep("R2", "The system displays Blue Jeans among the cart items."),
            ],
        )

        self.assertTrue(all(step.control is None for step in context.steps))

    def test_does_not_use_value_only_generic_button_as_a_unique_selector(self) -> None:
        value_only_graph = NavigationGraph(
            pages=[PageNode("home", self.home, "Home")],
            transitions=[],
            ui_elements=[
                UiElement(
                    page_url=self.home,
                    kind="button",
                    suggested_operation="click",
                    element={"tag": "input", "input_type": "button", "value": "Add to cart"},
                )
            ],
        )

        context = select_structured_context(
            value_only_graph,
            self.home,
            [SpecificationStep("R1", "The user selects Add to cart.")],
        )

        self.assertIsNone(context.steps[0].control)

    def test_verification_never_becomes_a_click_on_a_homonymous_link(self) -> None:
        graph = NavigationGraph(
            pages=[PageNode("home", self.home, "Home")],
            transitions=[],
            ui_elements=[
                _control(self.home, "link", "click", tag="a", text="book", href="/producttag/10/book")
            ],
        )

        context = select_structured_context(
            graph,
            self.home,
            [SpecificationStep("R1", "The user verifies that the book was added to the cart.")],
        )

        self.assertIsNone(context.steps[0].control)

    def test_compound_action_and_verification_keeps_control_and_destination_evidence(self) -> None:
        downloads = "https://example.test/digital-downloads"
        graph = NavigationGraph(
            pages=[
                PageNode("home", self.home, "Home"),
                PageNode("downloads", downloads, "Digital downloads", h1="Digital downloads"),
            ],
            transitions=[
                NavigationTransition(
                    source={"url": self.home, "title": "Home"},
                    target={"url": downloads, "title": "Digital downloads"},
                    action="click",
                    interaction_kind="link",
                    element={"tag": "a", "text": "Digital downloads", "href": "/digital-downloads"},
                    observed_result=ObservedResult("Digital downloads"),
                )
            ],
            ui_elements=[
                _control(
                    self.home,
                    "link",
                    "click",
                    tag="a",
                    text="Digital downloads",
                    href="/digital-downloads",
                )
            ],
        )

        context = select_structured_context(
            graph,
            self.home,
            [
                SpecificationStep(
                    "R1",
                    "The user must access the Digital downloads category and validate that the Digital downloads page is visible.",
                )
            ],
        )

        self.assertEqual(context.steps[0].control.element["href"], "/digital-downloads")
        self.assertEqual(context.steps[0].page_evidence.page_url, downloads)
        self.assertEqual(context.steps[0].page_evidence.text, "Digital downloads")
        self.assertIsNone(context.steps[0].observed_result)

    def test_does_not_reduce_explicit_update_control_to_navigation_link(self) -> None:
        graph = NavigationGraph(
            pages=[PageNode("cart", self.cart, "Shopping cart")],
            transitions=[],
            ui_elements=[
                _control(self.cart, "link", "click", tag="a", text="Shopping cart", href="/cart")
            ],
        )

        context = select_structured_context(
            graph,
            self.cart,
            [SpecificationStep("R1", "The user selects Update shopping cart.")],
        )

        self.assertIsNone(context.steps[0].control)

    def test_matches_terminal_punctuation_and_readable_id_or_name_aliases(self) -> None:
        login = "https://example.test/login"
        graph = NavigationGraph(
            pages=[PageNode("login", login, "Log in")],
            transitions=[],
            ui_elements=[
                _control(
                    login,
                    "text_input",
                    "fill",
                    tag="input",
                    id="Email",
                    label="Email:",
                    input_type="email",
                    form_action="/login",
                ),
                _control(
                    login,
                    "text_input",
                    "fill",
                    tag="input",
                    id="ConfirmPassword",
                    input_type="password",
                ),
                _control(
                    login,
                    "radio",
                    "check",
                    tag="input",
                    label="Female",
                    id="gender-female",
                    name="Gender",
                    input_type="radio",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            login,
            [
                SpecificationStep("R1", "The user fills in Email with a valid address."),
                SpecificationStep("R2", "The user fills in Confirm password."),
                SpecificationStep("R3", "The user selects a Gender option."),
                SpecificationStep("R4", "The user selects the Female Gender option."),
            ],
        )

        self.assertEqual(context.steps[0].control.element["id"], "Email")
        self.assertEqual(context.steps[1].control.element["id"], "ConfirmPassword")
        self.assertIsNone(context.steps[2].control)
        self.assertEqual(context.steps[3].control.element["id"], "gender-female")
        self.assertTrue(
            all(
                step.control is None or step.control.destination_url == ""
                for step in context.steps
            )
        )
        self.assertEqual(context.steps[0].control.element["form_action"], "/login")

    def test_prefers_stable_selector_for_homonymous_controls_on_same_page(self) -> None:
        register = "https://example.test/register"
        graph = NavigationGraph(
            pages=[PageNode("register", register, "Register")],
            transitions=[],
            ui_elements=[
                _control(register, "link", "click", tag="a", text="Register", href="/register"),
                _control(
                    register,
                    "button",
                    "click",
                    tag="input",
                    id="register-button",
                    value="Register",
                    input_type="submit",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            register,
            [SpecificationStep("R1", "The user selects Register.")],
        )

        self.assertEqual(len(context.steps[0].controls), 1)
        self.assertEqual(context.steps[0].control.element["id"], "register-button")
        self.assertEqual(context.steps[0].control.selector.kind, "id")

    def test_discards_generic_link_when_a_more_specific_link_is_selected(self) -> None:
        downloads = "https://example.test/digital-downloads"
        graph = NavigationGraph(
            pages=[
                PageNode("home", self.home, "Home"),
                PageNode("downloads", downloads, "Digital downloads", h1="Digital downloads"),
            ],
            transitions=[],
            ui_elements=[
                _control(self.home, "link", "click", tag="a", text="digital", href="/producttag/digital"),
                _control(
                    self.home,
                    "link",
                    "click",
                    tag="a",
                    text="Digital downloads",
                    href="/digital-downloads",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            self.home,
            [SpecificationStep("R1", "The user accesses Digital downloads.")],
        )

        self.assertEqual(
            [control.element["text"] for control in context.steps[0].controls],
            ["Digital downloads"],
        )

    def test_discards_object_link_when_step_uses_a_local_button(self) -> None:
        graph = NavigationGraph(
            pages=[PageNode("product", self.product, "Health Book", h1="Health Book")],
            transitions=[],
            ui_elements=[
                _control(self.product, "link", "click", tag="a", text="book", href="/producttag/book"),
                _control(
                    self.product,
                    "button",
                    "click",
                    tag="input",
                    id="add-to-cart-button-1",
                    value="Add to cart",
                    input_type="button",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            self.product,
            [
                SpecificationStep(
                    "R1",
                    "The user adds the book to the cart by selecting Add to cart.",
                )
            ],
        )

        self.assertEqual(len(context.steps[0].controls), 1)
        self.assertEqual(context.steps[0].control.element["id"], "add-to-cart-button-1")

    def test_filters_generic_label_before_applying_causal_scope(self) -> None:
        catalog = "https://example.test/books"
        product = "https://example.test/health-book"
        graph = NavigationGraph(
            pages=[PageNode("catalog", catalog, "Books"), PageNode("product", product, "Health Book")],
            transitions=[],
            ui_elements=[
                _control(catalog, "link", "click", tag="a", text="Book", href="/producttag/book"),
                _control(product, "link", "click", tag="a", text="Health Book", href="/health-book"),
            ],
        )

        context = select_structured_context(
            graph,
            catalog,
            [SpecificationStep("R1", "The user verifies that Health Book is available.")],
        )

        self.assertIsNone(context.steps[0].control)

    def test_adds_literal_h1_evidence_to_verification_and_page_entry(self) -> None:
        graph = NavigationGraph(
            pages=[PageNode("product", self.product, "Product", h1="Blue Jeans")],
            transitions=[],
            ui_elements=[],
        )

        context = select_structured_context(
            graph,
            self.product,
            [
                SpecificationStep("R1", "The system displays the details page with the name Blue Jeans."),
                SpecificationStep("R2", "The user opens Blue Jeans."),
            ],
        )

        self.assertEqual(context.steps[0].page_evidence.source, "h1")
        self.assertEqual(context.steps[0].page_evidence.text, "Blue Jeans")
        self.assertEqual(context.steps[1].page_evidence.source, "h1")
        self.assertEqual(context.steps[1].page_evidence.text, "Blue Jeans")

    def test_extracts_only_a_short_literal_span_from_visible_text(self) -> None:
        excerpt = "Demo Web Shop Home Account Your Shopping Cart is empty! Newsletter Footer information"
        graph = NavigationGraph(
            pages=[PageNode("cart", self.cart, "Cart page", visible_text_excerpt=excerpt)],
            transitions=[],
            ui_elements=[],
        )

        context = select_structured_context(
            graph,
            self.cart,
            [SpecificationStep("R1", "The system displays Your Shopping Cart is empty.")],
        )

        evidence = context.steps[0].page_evidence
        self.assertEqual(evidence.source, "visible_text_excerpt")
        self.assertEqual(evidence.text, "Your Shopping Cart is empty")
        self.assertNotEqual(evidence.text, excerpt)
        self.assertLessEqual(len(evidence.text), 120)

    def test_never_sends_the_complete_visible_text_excerpt(self) -> None:
        excerpt = "Your Shopping Cart is empty"
        graph = NavigationGraph(
            pages=[PageNode("cart", self.cart, "Cart page", visible_text_excerpt=excerpt)],
            transitions=[],
            ui_elements=[],
        )

        context = select_structured_context(
            graph,
            self.cart,
            [SpecificationStep("R1", "The system displays Your Shopping Cart is empty.")],
        )

        self.assertIsNone(context.steps[0].page_evidence)

    def test_does_not_borrow_a_matching_control_from_an_unrelated_page(self) -> None:
        unrelated_product = "https://example.test/build-your-own-computer"
        graph = NavigationGraph(
            pages=[
                PageNode("home", self.home, "Home"),
                PageNode("other-product", unrelated_product, "Build your own computer"),
            ],
            transitions=[],
            ui_elements=[
                self.search_input,
                _control(
                    unrelated_product,
                    "button",
                    "click",
                    tag="input",
                    id="add-to-cart-button-16",
                    value="Add to cart",
                    input_type="button",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            self.home,
            [
                SpecificationStep("R1", "The user searches in the Search store field."),
                SpecificationStep("R2", "The user selects Add to cart on the product page."),
            ],
        )

        self.assertIsNotNone(context.steps[0].control)
        self.assertIsNone(context.steps[1].control)

    def test_search_uses_same_form_controls_and_named_product_page_without_search_state(self) -> None:
        graph = NavigationGraph(
            pages=[
                PageNode("home", self.home, "Home"),
                PageNode("product", self.product, "Blue Jeans", h1="Blue Jeans"),
            ],
            transitions=[],
            ui_elements=[
                self.search_input,
                _control(
                    self.home,
                    "button",
                    "click",
                    tag="input",
                    input_type="submit",
                    value="Search",
                    form_action="/search",
                    form_method="GET",
                ),
                _control(
                    self.product,
                    "button",
                    "click",
                    tag="input",
                    input_type="button",
                    id="add-to-cart-button-36",
                    value="Add to cart",
                    form_action="/blue-jeans",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            self.home,
            [
                SpecificationStep("R1", "The user searches for Blue Jeans and opens the product page."),
                SpecificationStep("R2", "The user adds Blue Jeans to the cart."),
            ],
        )

        self.assertEqual(
            [control.element.get("id") or control.element.get("value") for control in context.steps[0].controls],
            ["small-searchterms", "Search"],
        )
        self.assertEqual(context.steps[0].page_evidence.text, "Blue Jeans")
        self.assertEqual(context.steps[1].control.element["id"], "add-to-cart-button-36")

    def test_compound_steps_keep_all_explicit_fields_on_the_active_page(self) -> None:
        register = "https://example.test/register"
        graph = NavigationGraph(
            pages=[PageNode("register", register, "Register")],
            transitions=[],
            ui_elements=[
                _control(register, "text_input", "fill", tag="input", id="FirstName", label="First name:"),
                _control(register, "text_input", "fill", tag="input", id="LastName", label="Last name:"),
                _control(register, "text_input", "fill", tag="input", id="Password", label="Password:"),
                _control(
                    register,
                    "text_input",
                    "fill",
                    tag="input",
                    id="ConfirmPassword",
                    label="Confirm password:",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            register,
            [
                SpecificationStep("R1", "The user fills in First name and Last name."),
                SpecificationStep("R2", "The user fills in Password and Confirm password."),
            ],
        )

        self.assertEqual(
            [control.element["id"] for control in context.steps[0].controls],
            ["FirstName", "LastName"],
        )
        self.assertEqual(
            [control.element["id"] for control in context.steps[1].controls],
            ["Password", "ConfirmPassword"],
        )

    def test_button_form_action_without_transition_does_not_leave_the_page(self) -> None:
        graph = NavigationGraph(
            pages=[PageNode("product", self.product, "Blue Jeans", h1="Blue Jeans")],
            transitions=[],
            ui_elements=[
                _control(
                    self.product,
                    "button",
                    "click",
                    tag="input",
                    input_type="button",
                    id="add-to-cart-button-36",
                    value="Add to cart",
                    form_action="/cart",
                ),
                _control(self.product, "link", "click", tag="a", text="Shopping cart", href="/cart"),
            ],
        )

        context = select_structured_context(
            graph,
            self.product,
            [
                SpecificationStep("R1", "The user selects Add to cart."),
                SpecificationStep("R2", "The user accesses Shopping cart."),
            ],
        )

        self.assertEqual(context.steps[0].control.element["id"], "add-to-cart-button-36")
        self.assertEqual(context.steps[1].control.page_url, self.product)

    def test_two_named_pages_can_supply_ordered_links_in_one_step(self) -> None:
        computers = "https://example.test/computers"
        desktops = "https://example.test/desktops"
        graph = NavigationGraph(
            pages=[
                PageNode("home", self.home, "Home"),
                PageNode("computers", computers, "Computers", h1="Computers"),
                PageNode("desktops", desktops, "Desktops", h1="Desktops"),
            ],
            transitions=[],
            ui_elements=[
                _control(self.home, "link", "click", tag="a", text="computer", href="/producttag/computer"),
                _control(self.home, "link", "click", tag="a", text="Computers", href="/computers"),
                _control(computers, "link", "click", tag="a", text="Desktops", href="/desktops"),
            ],
        )

        context = select_structured_context(
            graph,
            self.home,
            [SpecificationStep("R1", "The user accesses Computers and opens Desktops.")],
        )

        self.assertEqual(
            [control.element["text"] for control in context.steps[0].controls],
            ["Computers", "Desktops"],
        )
        self.assertEqual(context.steps[0].page_evidence.text, "Desktops")

    def test_submit_uses_the_named_active_form_instead_of_a_global_submit(self) -> None:
        login = "https://example.test/login"
        graph = NavigationGraph(
            pages=[PageNode("login", login, "Log in")],
            transitions=[],
            ui_elements=[
                _control(
                    login,
                    "text_input",
                    "fill",
                    tag="input",
                    id="Email",
                    label="Email:",
                    form_action="/login",
                    form_method="POST",
                ),
                _control(
                    login,
                    "text_input",
                    "fill",
                    tag="input",
                    id="Password",
                    label="Password:",
                    form_action="/login",
                    form_method="POST",
                ),
                _control(
                    login,
                    "button",
                    "click",
                    tag="input",
                    input_type="submit",
                    value="Log in",
                    form_action="/login",
                    form_method="POST",
                ),
                _control(
                    login,
                    "button",
                    "click",
                    tag="input",
                    input_type="submit",
                    value="Search",
                    form_action="/search",
                    form_method="GET",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            login,
            [
                SpecificationStep("R1", "The user fills in Email and Password."),
                SpecificationStep("R2", "The user submits the login form."),
            ],
        )

        self.assertEqual(
            [control.element["id"] for control in context.steps[0].controls],
            ["Email", "Password"],
        )
        self.assertEqual(context.steps[1].control.element["value"], "Log in")

    def test_lowercase_field_reference_and_password_confirmation_are_actions(self) -> None:
        register = "https://example.test/register"
        graph = NavigationGraph(
            pages=[PageNode("register", register, "Register")],
            transitions=[],
            ui_elements=[
                _control(
                    register,
                    "text_input",
                    "fill",
                    tag="input",
                    id="Email",
                    label="Email:",
                ),
                _control(
                    register,
                    "text_input",
                    "fill",
                    tag="input",
                    id="Password",
                    label="Password:",
                    input_type="password",
                ),
                _control(
                    register,
                    "text_input",
                    "fill",
                    tag="input",
                    id="ConfirmPassword",
                    label="Confirm password:",
                    input_type="password",
                ),
            ],
        )

        context = select_structured_context(
            graph,
            register,
            [
                SpecificationStep("R1", "The user fills in the email field."),
                SpecificationStep("R2", "The user fills in the password field."),
                SpecificationStep("R3", "The user confirms the password by typing it again."),
            ],
        )

        self.assertEqual(
            [step.control.element["id"] for step in context.steps],
            ["Email", "Password", "ConfirmPassword"],
        )


def _control(page_url: str, kind: str, operation: str, **element: str) -> UiElement:
    selectors = {
        key: value
        for key, value in element.items()
        if key in {"id", "name", "text", "href", "aria_label", "label", "placeholder"} and value
    }
    return UiElement(page_url, kind, operation, element, selectors)
