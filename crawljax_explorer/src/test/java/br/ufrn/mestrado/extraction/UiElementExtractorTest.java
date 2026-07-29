package br.ufrn.mestrado.extraction;

import br.ufrn.mestrado.domain.ExtractedUiElement;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class UiElementExtractorTest {

    private final UiElementExtractor extractor = new UiElementExtractor();

    @Test
    void extractsControlsWithoutPersistingSensitiveValues() {
        String html = """
            <html><body>
              <form action="/search" method="get">
                <label for="small-searchterms">Search store</label>
                <input id="small-searchterms" name="q" type="text" value="Search store">
                <input type="submit" value="Search">
              </form>
              <a href="/blue-jeans">Blue Jeans</a>
              <input id="add-to-cart-button-36" type="button" value="Add to cart">
              <input id="password" type="password" value="secret">
              <input type="hidden" name="token" value="private">
            </body></html>
            """;

        List<ExtractedUiElement> elements = extractor.extract("https://example.test/", html);

        ExtractedUiElement search = elements.stream()
            .filter(item -> "small-searchterms".equals(item.idAttribute()))
            .findFirst()
            .orElseThrow();
        assertEquals("text_input", search.kind());
        assertEquals("fill", search.suggestedOperation());
        assertEquals("Search store", search.label());
        assertEquals("/search", search.formAction());
        assertEquals("GET", search.formMethod());

        assertTrue(elements.stream().anyMatch(item -> "Blue Jeans".equals(item.text()) && "/blue-jeans".equals(item.href())));
        assertTrue(elements.stream().anyMatch(item -> "Add to cart".equals(item.value()) && "click".equals(item.suggestedOperation())));
        ExtractedUiElement password = elements.stream()
            .filter(item -> "password".equals(item.idAttribute()))
            .findFirst()
            .orElseThrow();
        assertEquals("password", password.inputType());
        assertEquals("text_input", password.kind());
        assertEquals("fill", password.suggestedOperation());
        assertEquals("", password.value());
        assertFalse(elements.stream().anyMatch(item -> "token".equals(item.name())));
    }

    @Test
    void deduplicatesTheSameControlWithinOnePage() {
        String html = "<a href='/cart'>Shopping cart(0)</a><a href='/cart'>Shopping cart(0)</a>";

        List<ExtractedUiElement> elements = extractor.extract("https://example.test/", html);

        assertEquals(1, elements.size());
    }
}
