package br.ufrn.mestrado.extraction;

import br.ufrn.mestrado.domain.ExtractedUiElement;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public final class UiElementExtractor {

    private static final String CONTROL_SELECTOR = String.join(", ",
        "a[href]", "button", "input:not([type=hidden])", "select", "textarea",
        "[role=button]", "[role=link]", "[role=textbox]", "[role=alert]", "[aria-label]"
    );

    public List<ExtractedUiElement> extract(String pageUrl, String dom) {
        if (dom == null || dom.isBlank()) {
            return List.of();
        }

        Document document = Jsoup.parse(dom, pageUrl == null ? "" : pageUrl);
        Map<String, String> labelsByControlId = labelsByControlId(document);
        Map<String, ExtractedUiElement> unique = new LinkedHashMap<>();

        for (Element element : document.select(CONTROL_SELECTOR)) {
            ExtractedUiElement extracted = extractElement(pageUrl, element, labelsByControlId);
            if (extracted != null) {
                unique.putIfAbsent(extracted.id(), extracted);
            }
        }
        return new ArrayList<>(unique.values());
    }

    private ExtractedUiElement extractElement(
        String pageUrl,
        Element element,
        Map<String, String> labelsByControlId
    ) {
        String tag = clean(element.tagName(), 40);
        String inputType = clean(element.attr("type"), 40).toLowerCase(Locale.ROOT);
        if ("hidden".equals(inputType) || element.hasAttr("disabled")) {
            return null;
        }

        String text = clean(element.text(), 160);
        String title = clean(element.attr("title"), 160);
        String idAttribute = clean(element.id(), 160);
        String label = clean(labelsByControlId.getOrDefault(idAttribute, closestLabel(element)), 160);
        String dataTestId = clean(firstNonBlank(element.attr("data-testid"), element.attr("data-test")), 160);
        String name = clean(element.attr("name"), 160);
        String value = safeValue(element, inputType);
        String href = clean(element.attr("href"), 300);
        String role = clean(element.attr("role"), 80);
        String ariaLabel = clean(element.attr("aria-label"), 160);
        String placeholder = clean(element.attr("placeholder"), 160);
        Element form = element.closest("form");
        String formAction = form == null ? "" : clean(form.attr("action"), 300);
        String formMethod = form == null ? "" : clean(form.attr("method"), 20).toUpperCase(Locale.ROOT);
        if (form != null && formMethod.isBlank()) {
            formMethod = "GET";
        }

        if (allBlank(text, title, label, dataTestId, idAttribute, name, value, href, role, ariaLabel, placeholder)) {
            return null;
        }

        String kind = classifyKind(tag, inputType, role);
        String operation = suggestedOperation(kind);
        String identity = String.join("|", safe(pageUrl), tag, firstStableAttribute(
            dataTestId, ariaLabel, idAttribute, name, placeholder, href, role, text, value
        ), normalizeDynamicText(text));

        return new ExtractedUiElement(
            "ui_" + sha256(identity).substring(0, 24),
            safe(pageUrl),
            kind,
            operation,
            tag,
            text,
            title,
            label,
            dataTestId,
            idAttribute,
            name,
            inputType,
            value,
            href,
            role,
            ariaLabel,
            placeholder,
            formAction,
            formMethod
        );
    }

    private Map<String, String> labelsByControlId(Document document) {
        Map<String, String> labels = new LinkedHashMap<>();
        for (Element label : document.select("label[for]")) {
            String target = clean(label.attr("for"), 160);
            String text = clean(label.text(), 160);
            if (!target.isBlank() && !text.isBlank()) {
                labels.putIfAbsent(target, text);
            }
        }
        return labels;
    }

    private String closestLabel(Element element) {
        Element parentLabel = element.closest("label");
        return parentLabel == null ? "" : parentLabel.text();
    }

    private String safeValue(Element element, String inputType) {
        if ("password".equals(inputType)) {
            return "";
        }
        String tag = element.tagName().toLowerCase(Locale.ROOT);
        if ("button".equals(tag) || "button".equals(inputType) || "submit".equals(inputType)) {
            return clean(element.attr("value"), 160);
        }
        if (("text".equals(inputType) || "search".equals(inputType) || inputType.isBlank())
            && element.hasAttr("value")) {
            return clean(element.attr("value"), 160);
        }
        return "";
    }

    private String classifyKind(String tag, String inputType, String role) {
        if ("alert".equalsIgnoreCase(role)) {
            return "feedback";
        }
        if ("textarea".equals(tag) || "textbox".equalsIgnoreCase(role)
            || ("input".equals(tag) && (inputType.isBlank() || "text".equals(inputType)
                || "search".equals(inputType) || "email".equals(inputType)
                || "number".equals(inputType) || "password".equals(inputType)))) {
            return "text_input";
        }
        if ("select".equals(tag)) {
            return "select";
        }
        if ("checkbox".equals(inputType)) {
            return "checkbox";
        }
        if ("radio".equals(inputType)) {
            return "radio";
        }
        if ("button".equals(tag) || "button".equals(inputType) || "submit".equals(inputType)
            || "button".equalsIgnoreCase(role)) {
            return "button";
        }
        if ("a".equals(tag) || "link".equalsIgnoreCase(role)) {
            return "link";
        }
        return "control";
    }

    private String suggestedOperation(String kind) {
        return switch (kind) {
            case "text_input" -> "fill";
            case "select" -> "selectOption";
            case "checkbox", "radio" -> "check";
            case "button", "link" -> "click";
            case "feedback" -> "assert";
            default -> "interact";
        };
    }

    private String firstStableAttribute(String... values) {
        for (String value : values) {
            if (value != null && !value.isBlank()) {
                return value;
            }
        }
        return "unidentified";
    }

    private String normalizeDynamicText(String text) {
        return safe(text).replaceFirst("(?i)\\s*\\(\\d+\\)\\s*$", "").trim().toLowerCase(Locale.ROOT);
    }

    private String clean(String value, int maxLength) {
        String normalized = safe(value).replaceAll("\\s+", " ").trim();
        return normalized.length() <= maxLength ? normalized : normalized.substring(0, maxLength).trim();
    }

    private boolean allBlank(String... values) {
        for (String value : values) {
            if (value != null && !value.isBlank()) {
                return false;
            }
        }
        return true;
    }

    private String firstNonBlank(String first, String second) {
        return first != null && !first.isBlank() ? first : second;
    }

    private String safe(String value) {
        return value == null ? "" : value;
    }

    private String sha256(String value) {
        try {
            byte[] digest = MessageDigest.getInstance("SHA-256").digest(value.getBytes(StandardCharsets.UTF_8));
            StringBuilder result = new StringBuilder();
            for (byte item : digest) {
                result.append(String.format("%02x", item));
            }
            return result.toString();
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 indisponivel", exception);
        }
    }
}
