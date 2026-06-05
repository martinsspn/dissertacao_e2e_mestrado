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
        } catch (NumberFormatException exception) {
            System.out.println("Aviso: valor invalido para " + key + ". Usando " + fallback + ".");
            return fallback;
        }
    }

    public static boolean getBooleanEnvOrDefault(String key, boolean fallback) {
        String value = System.getenv(key);
        if (value == null || value.isBlank()) {
            return fallback;
        }
        return Boolean.parseBoolean(value.trim());
    }

    public static String safeValue(String value, String fallback) {
        if (value == null) {
            return fallback;
        }
        String normalized = value.replaceAll("\\s+", " ").trim();
        return normalized.isEmpty() ? fallback : normalized;
    }
}
