package br.ufrn.mestrado.infra;

public final class EnvironmentUtils {

    private EnvironmentUtils() {
    }

    public static String getEnvOrDefault(String key, String fallback) {
        String value = System.getenv(key);
        if (value == null || value.isBlank()) {
            return fallback;
        }
        return value.trim();
    }

    public static int getIntEnvOrDefault(String key, int fallback) {
        String value = System.getenv(key);
        if (value == null || value.isBlank()) {
            return fallback;
        }
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException ex) {
            System.out.println("Aviso: valor inválido para " + key + ". Usando fallback=" + fallback);
            return fallback;
        }
    }

    public static boolean getBooleanEnvOrDefault(String key, boolean fallback) {
        String value = System.getenv(key);
        if (value == null || value.isBlank()) {
            return fallback;
        }

        String normalized = value.trim().toLowerCase();
        if ("true".equals(normalized) || "1".equals(normalized) || "yes".equals(normalized)) {
            return true;
        }
        if ("false".equals(normalized) || "0".equals(normalized) || "no".equals(normalized)) {
            return false;
        }

        System.out.println("Aviso: valor inválido para " + key + ". Usando fallback=" + fallback);
        return fallback;
    }

    public static String safeValue(String value, String fallback) {
        if (value == null) {
            return fallback;
        }
        String normalized = value.replaceAll("\\s+", " ").trim();
        return normalized.isEmpty() ? fallback : normalized;
    }
}