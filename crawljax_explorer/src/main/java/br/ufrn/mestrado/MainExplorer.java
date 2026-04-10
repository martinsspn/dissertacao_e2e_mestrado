package br.ufrn.mestrado;

import com.crawljax.core.CrawlSession;
import com.crawljax.core.CrawljaxRunner;
import com.crawljax.core.ExitNotifier.ExitStatus;
import com.crawljax.core.configuration.BrowserConfiguration;
import org.openqa.selenium.remote.DesiredCapabilities;
import com.crawljax.core.configuration.CrawljaxConfiguration;
import com.crawljax.core.configuration.CrawljaxConfiguration.CrawljaxConfigurationBuilder;
import com.crawljax.core.plugin.PostCrawlingPlugin;
import com.crawljax.core.state.Element;
import com.crawljax.core.state.Eventable;
import com.crawljax.core.state.Identification;
import com.crawljax.core.state.StateFlowGraph;
import com.crawljax.core.state.StateVertex;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;
import org.neo4j.driver.TransactionContext;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainExplorer {

    public static void main(String[] args) {
        // 1. Pega a URL alvo configurada no docker-compose.yml
        String targetUrl = System.getenv("TARGET_URL");
        if (targetUrl == null || targetUrl.isEmpty()) {
            targetUrl = "http://example.com"; // Fallback para testes
            System.out.println("Aviso: TARGET_URL não definida. Usando " + targetUrl);
        }

        System.out.println("Iniciando exploração no alvo: " + targetUrl);

        // 2. Configura o Crawljax
        CrawljaxConfigurationBuilder builder = CrawljaxConfiguration.builderFor(targetUrl);

        // Usa o Selenium Grid remoto (container selenium_chrome no docker-compose)
        String seleniumHubUrl = System.getenv("SELENIUM_HUB_URL");
        if (seleniumHubUrl == null || seleniumHubUrl.isEmpty()) {
            seleniumHubUrl = "http://localhost:4444/wd/hub"; // fallback local
        }

        int seleniumReadyTimeoutSeconds = getIntEnvOrDefault("SELENIUM_READY_TIMEOUT_SECONDS", 120);
        boolean seleniumReadyRequired = getBooleanEnvOrDefault("SELENIUM_READY_REQUIRED", false);
        waitForSeleniumReady(seleniumHubUrl, seleniumReadyTimeoutSeconds, seleniumReadyRequired);

        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setBrowserName("chrome");
        builder.setBrowserConfig(BrowserConfiguration.remoteConfig(1, seleniumHubUrl, capabilities));

        int maxDepth = getIntEnvOrDefault("CRAWL_MAX_DEPTH", 8);
        int maxStates = getIntEnvOrDefault("CRAWL_MAX_STATES", 400);
        int maxRuntimeMinutes = getIntEnvOrDefault("CRAWL_MAX_RUNTIME_MINUTES", 45);
        int waitAfterReloadMs = getIntEnvOrDefault("CRAWL_WAIT_AFTER_RELOAD_MS", 3000);
        int waitAfterEventMs = getIntEnvOrDefault("CRAWL_WAIT_AFTER_EVENT_MS", 2200);
        boolean clickOnce = getBooleanEnvOrDefault("CRAWL_CLICK_ONCE", false);
        boolean randomOrder = getBooleanEnvOrDefault("CRAWL_RANDOM_ORDER", true);

        // Regras para exploração ampla e profunda da aplicação
        builder.crawlRules().clickOnce(clickOnce);
        builder.crawlRules().clickElementsInRandomOrder(randomOrder);
        builder.crawlRules().crawlHiddenAnchors(true);
        
        // Configura tempos de espera para lidar com carregamento dinâmico (AJAX/JS)
        builder.crawlRules().waitAfterReloadUrl(waitAfterReloadMs, TimeUnit.MILLISECONDS);
        builder.crawlRules().waitAfterEvent(waitAfterEventMs, TimeUnit.MILLISECONDS);

        // O que o Crawler deve clicar
        builder.crawlRules().clickDefaultElements(); // Clica em tags <a>, <button>, <input>
        builder.crawlRules().click("label"); // Clica em labels com comportamento de toggle
        builder.crawlRules().click("summary"); // Abre elementos <details>
        builder.crawlRules().click("option"); // Troca opções de selects
        builder.crawlRules().click("input").withAttribute("type", "submit");
        builder.crawlRules().click("input").withAttribute("type", "button");
        builder.crawlRules().click("input").withAttribute("type", "radio");
        builder.crawlRules().click("input").withAttribute("type", "checkbox");
        builder.crawlRules().click("div"); // Clica em divs interagíveis
        builder.crawlRules().click("span"); // Clica em spans interagíveis
        builder.crawlRules().click("li"); // Clica em itens de lista
        builder.crawlRules().click("img"); // Clica em imagens

        // Limites da exploração (Aumentados para maior cobertura)
        builder.setMaximumDepth(maxDepth);
        builder.setMaximumStates(maxStates);
        builder.setMaximumRunTime(maxRuntimeMinutes, TimeUnit.MINUTES);

        System.out.println(
            "Perfil de crawl -> depth=" + maxDepth +
                ", states=" + maxStates +
                ", runtime(min)=" + maxRuntimeMinutes +
                ", waitReload(ms)=" + waitAfterReloadMs +
                ", waitEvent(ms)=" + waitAfterEventMs +
                ", clickOnce=" + clickOnce +
                ", randomOrder=" + randomOrder
        );

        // 3. Adiciona o nosso plugin que vai salvar os arquivos no final
        builder.addPlugin(new SemanticExportPlugin());

        // 4. Roda a máquina
        CrawljaxRunner crawljax = new CrawljaxRunner(builder.build());
        crawljax.call();
    }

    /**
     * Plugin customizado que executa apenas quando o Crawljax termina a navegação.
     */
    static class SemanticExportPlugin implements PostCrawlingPlugin {
        @Override
        public void postCrawling(CrawlSession session, ExitStatus exitReason) {
            System.out.println("Exploração finalizada. Motivo: " + exitReason);
            System.out.println("Iniciando persistência dos estados e transições no Neo4j...");

            StateFlowGraph sfg = session.getStateFlowGraph();
            String neo4jUri = getEnvOrDefault("NEO4J_URI", "bolt://neo4j:7687");
            String neo4jUser = getEnvOrDefault("NEO4J_USER", "neo4j");
            String neo4jPassword = getEnvOrDefault("NEO4J_PASSWORD", "neo4j_password");

            List<Map<String, Object>> nos = new ArrayList<>();
            List<Map<String, Object>> arestas = new ArrayList<>();

            // Monta os nós básicos do grafo.
            for (StateVertex state : sfg.getAllStates()) {
                Map<String, Object> no = new HashMap<>();
                String dom = state.getDom() == null ? "" : state.getDom();
                no.put("id", state.getName());
                no.put("stateName", state.getName());
                no.put("url", safeValue(state.getUrl(), "url_desconhecida"));
                no.put("title", extractTitleFromDom(dom));
                nos.add(no);
            }

            // Monta as relações entre páginas com metadados mínimos de navegação.
            for (Eventable edge : sfg.getAllEdges()) {
                Map<String, Object> transicao = new HashMap<>();
                transicao.put("origem", edge.getSourceStateVertex().getName());
                transicao.put("destino", edge.getTargetStateVertex().getName());
                transicao.put("action", safeValue(edge.getEventType().toString().toLowerCase(), "desconhecido"));

                Identification identification = edge.getIdentification();
                String selectorTipo = "desconhecido";
                String selectorValor = "desconhecido";
                if (identification != null) {
                    selectorTipo = identification.getHow() == null ? "desconhecido" : identification.getHow().toString().toLowerCase();
                    selectorValor = safeValue(identification.getValue(), "desconhecido");
                }
                transicao.put("selectorType", selectorTipo);
                transicao.put("selectorValue", selectorValor);

                Element element = edge.getElement();
                String elementTag = element == null ? "desconhecido" : safeValue(element.getTag(), "desconhecido");
                String elementText = element == null ? "" : safeValue(element.getText(), "");
                String elementId = element == null ? "" : safeValue(element.getElementId(), "");
                String elementClasses = element == null ? "" : safeValue(element.getAttributeOrNull("class"), "");
                String elementName = element == null ? "" : safeValue(element.getAttributeOrNull("name"), "");
                String elementRole = element == null ? "" : safeValue(element.getAttributeOrNull("role"), "");
                String elementHref = element == null ? "" : safeValue(element.getAttributeOrNull("href"), "");
                String inputType = element == null ? "" : safeValue(element.getAttributeOrNull("type"), "");

                transicao.put("triggerType", elementTag);
                transicao.put("triggerText", elementText);
                transicao.put("elementTag", elementTag);
                transicao.put("elementId", elementId);
                transicao.put("elementClasses", elementClasses);
                transicao.put("elementText", elementText);
                transicao.put("elementName", elementName);
                transicao.put("elementRole", elementRole);
                transicao.put("elementHref", elementHref);
                transicao.put("inputType", inputType);
                transicao.put("interactionKind", classifyInteractionKind(elementTag, inputType, elementHref, elementRole));

                arestas.add(transicao);
            }

            try (Driver driver = GraphDatabase.driver(neo4jUri, AuthTokens.basic(neo4jUser, neo4jPassword));
                 Session neo4jSession = driver.session()) {
                driver.verifyConnectivity();

                // Schema operations must run in a dedicated transaction.
                neo4jSession.executeWrite((TransactionContext tx) -> {
                    tx.run("CREATE CONSTRAINT page_state_id_unique IF NOT EXISTS FOR (n:PageState) REQUIRE n.id IS UNIQUE");
                    return null;
                });

                // Data cleanup in a separate write transaction.
                neo4jSession.executeWrite((TransactionContext tx) -> {
                    tx.run("MATCH (n:PageState) DETACH DELETE n");
                    return null;
                });

                // Batch insert nodes and edges in a separate write transaction.
                neo4jSession.executeWrite((TransactionContext tx) -> {
                    tx.run(
                            "UNWIND $nodes AS node " +
                                    "MERGE (n:PageState {id: node.id}) " +
                                    "SET n.state_name = node.stateName, n.url = node.url, n.title = node.title",
                            Map.of("nodes", nos)
                    );
                    tx.run(
                            "UNWIND $edges AS edge " +
                                    "MATCH (origem:PageState {id: edge.origem}) " +
                                    "MATCH (destino:PageState {id: edge.destino}) " +
                                    "MERGE (origem)-[r:NAVIGATES_TO {selector_value: edge.selectorValue, action: edge.action, destino_id: edge.destino}]->(destino) " +
                                "SET r.selector_type = edge.selectorType, " +
                                "r.trigger_type = edge.triggerType, " +
                                "r.trigger_text = edge.triggerText, " +
                                "r.interaction_kind = edge.interactionKind, " +
                                "r.element_tag = edge.elementTag, " +
                                "r.element_id = edge.elementId, " +
                                "r.element_classes = edge.elementClasses, " +
                                "r.element_text = edge.elementText, " +
                                "r.element_name = edge.elementName, " +
                                "r.element_role = edge.elementRole, " +
                                "r.element_href = edge.elementHref, " +
                                "r.input_type = edge.inputType",
                            Map.of("edges", arestas)
                    );
                    return null;
                });

                System.out.println("Persistência concluída no Neo4j. Nós: " + nos.size() + " | Arestas: " + arestas.size());
            } catch (Exception e) {
                System.err.println("Erro ao persistir grafo no Neo4j: " + e.getMessage());
            }
        }

        private String extractTitleFromDom(String dom) {
            if (dom == null || dom.isBlank()) {
                return "sem_titulo";
            }
            Pattern pattern = Pattern.compile("(?is)<title[^>]*>(.*?)</title>");
            Matcher matcher = pattern.matcher(dom);
            if (!matcher.find()) {
                return "sem_titulo";
            }
            return matcher.group(1).replaceAll("\\s+", " ").trim();
        }

        private String getEnvOrDefault(String key, String fallback) {
            String value = System.getenv(key);
            if (value == null || value.isBlank()) {
                return fallback;
            }
            return value.trim();
        }

        private String safeValue(String value, String fallback) {
            if (value == null) {
                return fallback;
            }
            String normalized = value.replaceAll("\\s+", " ").trim();
            return normalized.isEmpty() ? fallback : normalized;
        }

        private String classifyInteractionKind(String elementTag, String inputType, String elementHref, String elementRole) {
            String tag = safeValue(elementTag, "").toLowerCase();
            String type = safeValue(inputType, "").toLowerCase();
            String href = safeValue(elementHref, "");
            String role = safeValue(elementRole, "").toLowerCase();

            if ("a".equals(tag)) {
                return "anchor";
            }
            if ("button".equals(tag) || "button".equals(type) || "submit".equals(type)) {
                return "button";
            }
            if (!href.isEmpty()) {
                return "link";
            }
            if ("input".equals(tag)) {
                return "input";
            }
            if ("link".equals(role)) {
                return "link_like";
            }
            if ("button".equals(role)) {
                return "button_like";
            }
            return tag.isEmpty() ? "desconhecido" : tag;
        }
    }

    private static int getIntEnvOrDefault(String key, int fallback) {
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

    private static boolean getBooleanEnvOrDefault(String key, boolean fallback) {
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

    private static void waitForSeleniumReady(String seleniumHubUrl, int timeoutSeconds, boolean required) {
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

        String message = "Timeout aguardando Selenium em " + String.join(" | ", statusUrls) +
            ". Verifique o serviço selenium_chrome e a variável SELENIUM_HUB_URL.";
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