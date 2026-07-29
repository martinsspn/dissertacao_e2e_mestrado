package br.ufrn.mestrado.extraction;

import br.ufrn.mestrado.domain.ObservedResult;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ObservedResultExtractorTest {

    private final ObservedResultExtractor extractor = new ObservedResultExtractor();

    @Test
    void returnsNewNotificationFromTargetState() {
        String source = "<h1>Blue Jeans</h1><div id='bar-notification'></div>";
        String target = "<h1>Blue Jeans</h1><div id='bar-notification' role='alert'>Added to cart</div>";

        ObservedResult result = extractor.extract(source, target);

        assertEquals("Added to cart", result.text());
        assertEquals("bar-notification", result.elementId());
        assertEquals("alert", result.role());
    }

    @Test
    void ignoresUnchangedHeading() {
        ObservedResult result = extractor.extract("<h1>Cart</h1>", "<h1>Cart</h1>");

        assertEquals("", result.text());
    }
}
