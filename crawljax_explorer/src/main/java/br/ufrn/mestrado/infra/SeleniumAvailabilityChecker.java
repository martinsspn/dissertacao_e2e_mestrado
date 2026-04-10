package br.ufrn.mestrado.infra;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

public final class SeleniumAvailabilityChecker {

    private SeleniumAvailabilityChecker() {
    }

    public static void waitForSeleniumReady(String seleniumHubUrl, int timeoutSeconds, boolean required) {
        List<String> statusUrls = buildSeleniumStatusUrls(seleniumHubUrl);
        long deadline = System.currentTimeMillis() + TimeUnit.SECONDS.toMillis(timeoutSeconds);

        System.out.println("Aguardando Selenium ficar pronto em: " + String.join(" | ", statusUrls));

        while (System.currentTimeMillis() < deadline) {
            for (String statusUrl : statusUrls) {
                if (isSeleniumReady(statusUrl)) {
                    System.out.println("Selenium pronto para receber sessões WebDriver.");
                    return;
                }
            }

            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Thread interrompida enquanto aguardava Selenium", e);
            }
        }

        String message = "Timeout aguardando Selenium em " + String.join(" | ", statusUrls)
            + ". Verifique o serviço selenium_chrome e a variável SELENIUM_HUB_URL.";
        if (required) {
            throw new RuntimeException(message);
        }
        System.out.println("Aviso: " + message + " Prosseguindo mesmo assim (SELENIUM_READY_REQUIRED=false).");
    }

    private static List<String> buildSeleniumStatusUrls(String seleniumHubUrl) {
        String base = seleniumHubUrl.trim();
        List<String> urls = new ArrayList<>();

        if (base.endsWith("/wd/hub")) {
            urls.add(base + "/status");
            urls.add(base.substring(0, base.length() - "/wd/hub".length()) + "/status");
            return urls;
        }
        if (base.endsWith("/wd/hub/")) {
            urls.add(base + "status");
            urls.add(base.substring(0, base.length() - "/wd/hub/".length()) + "/status");
            return urls;
        }
        if (base.endsWith("/")) {
            urls.add(base + "status");
            return urls;
        }

        urls.add(base + "/status");
        return urls;
    }

    private static boolean isSeleniumReady(String statusUrl) {
        HttpURLConnection connection = null;
        try {
            URL url = new URL(statusUrl);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(3000);
            connection.setReadTimeout(3000);

            int statusCode = connection.getResponseCode();
            if (statusCode < 200 || statusCode >= 300) {
                return false;
            }

            byte[] bodyBytes = connection.getInputStream().readAllBytes();
            String body = new String(bodyBytes, StandardCharsets.UTF_8).toLowerCase();
            return Pattern.compile("\\\"ready\\\"\\s*:\\s*true").matcher(body).find();
        } catch (IOException ex) {
            return false;
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}