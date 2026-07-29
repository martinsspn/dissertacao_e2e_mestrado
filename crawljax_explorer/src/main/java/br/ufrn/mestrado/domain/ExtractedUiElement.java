package br.ufrn.mestrado.domain;

public record ExtractedUiElement(
    String id,
    String pageUrl,
    String kind,
    String suggestedOperation,
    String tag,
    String text,
    String title,
    String label,
    String dataTestId,
    String idAttribute,
    String name,
    String inputType,
    String value,
    String href,
    String role,
    String ariaLabel,
    String placeholder,
    String formAction,
    String formMethod
) {
}
