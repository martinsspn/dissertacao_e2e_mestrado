package br.ufrn.mestrado.extraction;

import br.ufrn.mestrado.domain.ObservedResult;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.util.LinkedHashSet;
import java.util.Set;

public final class ObservedResultExtractor {

    private static final String OBSERVABLE_SELECTOR = String.join(", ",
        "[role=alert]", "[aria-live]", "#bar-notification", ".bar-notification",
        ".notification", ".message", ".result", ".validation-summary-errors", "h1"
    );

    public ObservedResult extract(String sourceDom, String targetDom) {
        if (targetDom == null || targetDom.isBlank()) {
            return ObservedResult.empty();
        }
        Document source = Jsoup.parse(sourceDom == null ? "" : sourceDom);
        Document target = Jsoup.parse(targetDom);
        Set<String> sourceObservations = observationKeys(source);

        for (Element candidate : target.select(OBSERVABLE_SELECTOR)) {
            String text = clean(candidate.text(), 240);
            if (text.isBlank()) {
                continue;
            }
            String key = observationKey(candidate, text);
            if (!sourceObservations.contains(key)) {
                return new ObservedResult(text, clean(candidate.id(), 160), clean(candidate.attr("role"), 80));
            }
        }
        return ObservedResult.empty();
    }

    private Set<String> observationKeys(Document document) {
        Set<String> keys = new LinkedHashSet<>();
        for (Element candidate : document.select(OBSERVABLE_SELECTOR)) {
            String text = clean(candidate.text(), 240);
            if (!text.isBlank()) {
                keys.add(observationKey(candidate, text));
            }
        }
        return keys;
    }

    private String observationKey(Element element, String text) {
        return element.tagName() + "|" + element.id() + "|" + element.attr("role") + "|" + text;
    }

    private String clean(String value, int maxLength) {
        String normalized = value == null ? "" : value.replaceAll("\\s+", " ").trim();
        return normalized.length() <= maxLength ? normalized : normalized.substring(0, maxLength).trim();
    }
}
