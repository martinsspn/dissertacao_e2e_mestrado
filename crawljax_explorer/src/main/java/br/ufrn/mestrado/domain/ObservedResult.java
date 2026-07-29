package br.ufrn.mestrado.domain;

public record ObservedResult(String text, String elementId, String role) {
    public static ObservedResult empty() {
        return new ObservedResult("", "", "");
    }
}
