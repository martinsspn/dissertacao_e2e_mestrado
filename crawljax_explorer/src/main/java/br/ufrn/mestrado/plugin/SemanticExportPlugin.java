package br.ufrn.mestrado.plugin;

import br.ufrn.mestrado.domain.ExtractedUiElement;
import br.ufrn.mestrado.domain.ObservedResult;
import br.ufrn.mestrado.extraction.ObservedResultExtractor;
import br.ufrn.mestrado.extraction.UiElementExtractor;
import br.ufrn.mestrado.infra.EnvironmentUtils;

import com.crawljax.core.CrawlSession;
import com.crawljax.core.CrawlerContext;
import com.crawljax.core.ExitNotifier.ExitStatus;
import com.crawljax.core.plugin.OnNewStatePlugin;
import com.crawljax.core.plugin.PreStateCrawlingPlugin;
import com.crawljax.core.plugin.PostCrawlingPlugin;
import com.crawljax.core.CandidateElement;
import com.crawljax.core.state.Element;
import com.crawljax.core.state.Eventable;
import com.crawljax.core.state.Identification;
import com.crawljax.core.state.StateFlowGraph;
import com.crawljax.core.state.StateVertex;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.ImmutableList;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;
import org.neo4j.driver.TransactionContext;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SemanticExportPlugin implements OnNewStatePlugin, PreStateCrawlingPlugin, PostCrawlingPlugin {

    private static final ObjectMapper JSON_MAPPER = new ObjectMapper();
    private final Map<String, String> stateScreenshots = new HashMap<>();
    private final UiElementExtractor uiElementExtractor = new UiElementExtractor();
    private final ObservedResultExtractor observedResultExtractor = new ObservedResultExtractor();

    @Override
    public void onNewState(CrawlerContext context, StateVertex newState) {
        captureStateScreenshot(context, newState);
    }

    @Override
    public void preStateCrawling(
        CrawlerContext context,
        ImmutableList<CandidateElement> candidateElements,
        StateVertex state
    ) {
        captureStateScreenshot(context, state);
    }

    @Override
    public void postCrawling(CrawlSession session, ExitStatus exitReason) {
        System.out.println("Exploração finalizada. Motivo: " + exitReason);
        System.out.println("Iniciando persistência dos estados e transições no Neo4j...");

        StateFlowGraph sfg = session.getStateFlowGraph();
        String neo4jUri = EnvironmentUtils.getEnvOrDefault("NEO4J_URI", "bolt://neo4j:7687");
        String neo4jUser = EnvironmentUtils.getEnvOrDefault("NEO4J_USER", "neo4j");
        String neo4jPassword = EnvironmentUtils.getEnvOrDefault("NEO4J_PASSWORD", "neo4j_password");

        // Mapear estados para URLs consolidadas
        Map<String, String> stateUrlMapping = createStateUrlMapping(sfg);
        
        List<Map<String, Object>> nos = mapStatesToNodes(sfg);
        List<Map<String, Object>> elementos = mapStatesToUiElements(sfg);
        List<Map<String, Object>> arestas = mapEdgesToRelationships(sfg, stateUrlMapping);

        persistGraph(neo4jUri, neo4jUser, neo4jPassword, nos, elementos, arestas);
    }

    private Map<String, String> createStateUrlMapping(StateFlowGraph sfg) {
        Map<String, String> stateToUrl = new HashMap<>();
        for (StateVertex state : sfg.getAllStates()) {
            String url = EnvironmentUtils.safeValue(state.getUrl(), "url_desconhecida");
            stateToUrl.put(state.getName(), url);
        }
        return stateToUrl;
    }

    private List<Map<String, Object>> mapStatesToNodes(StateFlowGraph sfg) {
        List<Map<String, Object>> nos = new ArrayList<>();
        Map<String, Map<String, Object>> urlToNode = new HashMap<>();

        for (StateVertex state : sfg.getAllStates()) {
            String url = EnvironmentUtils.safeValue(state.getUrl(), "url_desconhecida");
            String dom = state.getDom() == null ? "" : state.getDom();
            String title = extractTitleFromDom(dom);
            String h1 = extractFirstTagText(dom, "h1", "");
            String visibleText = extractVisibleText(dom, 1200);
            int interactiveCount = countInteractiveElements(dom);

            // Consolidar por URL - usar URL como chave única
            if (!urlToNode.containsKey(url)) {
                Map<String, Object> no = new HashMap<>();
                no.put("id", generateIdFromUrl(url));  // ID seguro baseado em URL
                no.put("url", url);
                no.put("title", title);
                no.put("state_count", 1);  // Rastrear quantos estados foram consolidados
                no.put("h1", h1);
                no.put("visible_text_excerpt", visibleText);
                no.put("interactive_count", interactiveCount);
                no.put("screenshot_path", EnvironmentUtils.safeValue(stateScreenshots.get(state.getName()), ""));
                urlToNode.put(url, no);
            } else {
                // Incrementar contador de estados consolidados
                Map<String, Object> existing = urlToNode.get(url);
                int count = (Integer) existing.getOrDefault("state_count", 1);
                existing.put("state_count", count + 1);
                if (EnvironmentUtils.safeValue((String) existing.get("screenshot_path"), "").isEmpty()) {
                    existing.put("screenshot_path", EnvironmentUtils.safeValue(stateScreenshots.get(state.getName()), ""));
                }
            }
        }

        nos.addAll(urlToNode.values());
        System.out.println("✓ Nós consolidados: " + urlToNode.size() + " URLs únicas de " + sfg.getAllStates().size() + " estados");
        return nos;
    }

    private String generateIdFromUrl(String url) {
        // Gerar um ID único e seguro a partir da URL
        return Math.abs(url.hashCode()) + "_" + url.replaceAll("[^a-zA-Z0-9]", "_").substring(0, Math.min(30, url.length()));
    }

    private List<Map<String, Object>> mapStatesToUiElements(StateFlowGraph sfg) {
        Map<String, Map<String, Object>> uniqueElements = new LinkedHashMap<>();
        for (StateVertex state : sfg.getAllStates()) {
            String pageUrl = EnvironmentUtils.safeValue(state.getUrl(), "url_desconhecida");
            String dom = state.getDom() == null ? "" : state.getDom();
            for (ExtractedUiElement element : uiElementExtractor.extract(pageUrl, dom)) {
                Map<String, Object> data = new LinkedHashMap<>();
                data.put("id", element.id());
                data.put("page_id", generateIdFromUrl(pageUrl));
                data.put("page_url", element.pageUrl());
                data.put("kind", element.kind());
                data.put("suggested_operation", element.suggestedOperation());
                data.put("tag", element.tag());
                data.put("text", element.text());
                data.put("title", element.title());
                data.put("label", element.label());
                data.put("data_testid", element.dataTestId());
                data.put("id_attribute", element.idAttribute());
                data.put("name", element.name());
                data.put("input_type", element.inputType());
                data.put("value", element.value());
                data.put("href", element.href());
                data.put("role", element.role());
                data.put("aria_label", element.ariaLabel());
                data.put("placeholder", element.placeholder());
                data.put("form_action", element.formAction());
                data.put("form_method", element.formMethod());
                uniqueElements.putIfAbsent(element.id(), data);
            }
        }
        System.out.println("✓ Controles estruturados: " + uniqueElements.size());
        return new ArrayList<>(uniqueElements.values());
    }

    private List<Map<String, Object>> mapEdgesToRelationships(StateFlowGraph sfg, Map<String, String> stateUrlMapping) {
        List<Map<String, Object>> arestas = new ArrayList<>();

        for (Eventable edge : sfg.getAllEdges()) {
            String sourceState = edge.getSourceStateVertex().getName();
            String targetState = edge.getTargetStateVertex().getName();
            
            // Mapear para URLs consolidadas
            String sourceUrl = stateUrlMapping.getOrDefault(sourceState, "url_desconhecida");
            String targetUrl = stateUrlMapping.getOrDefault(targetState, "url_desconhecida");
            
            Map<String, Object> transicao = new HashMap<>();
            transicao.put("origem", generateIdFromUrl(sourceUrl));
            transicao.put("destino", generateIdFromUrl(targetUrl));
            transicao.put("action", EnvironmentUtils.safeValue(edge.getEventType().toString().toLowerCase(), "desconhecido"));

            Identification identification = edge.getIdentification();
            String selectorTipo = "desconhecido";
            String selectorValor = "desconhecido";
            if (identification != null) {
                selectorTipo = identification.getHow() == null
                    ? "desconhecido"
                    : identification.getHow().toString().toLowerCase();
                selectorValor = EnvironmentUtils.safeValue(identification.getValue(), "desconhecido");
            }
            transicao.put("selectorType", selectorTipo);
            transicao.put("selectorValue", selectorValor);

            Element element = edge.getElement();
            String elementTag = element == null ? "desconhecido" : EnvironmentUtils.safeValue(element.getTag(), "desconhecido");
            String elementText = element == null ? "" : EnvironmentUtils.safeValue(element.getText(), "");
            String elementId = element == null ? "" : EnvironmentUtils.safeValue(element.getElementId(), "");
            String elementClasses = element == null ? "" : EnvironmentUtils.safeValue(element.getAttributeOrNull("class"), "");
            String elementName = element == null ? "" : EnvironmentUtils.safeValue(element.getAttributeOrNull("name"), "");
            String elementRole = element == null ? "" : EnvironmentUtils.safeValue(element.getAttributeOrNull("role"), "");
            String elementAria = element == null ? "" : EnvironmentUtils.safeValue(element.getAttributeOrNull("aria-label"), "");
            String elementHref = element == null ? "" : EnvironmentUtils.safeValue(element.getAttributeOrNull("href"), "");
            String inputType = element == null ? "" : EnvironmentUtils.safeValue(element.getAttributeOrNull("type"), "");
            transicao.put("triggerType", elementTag);
            transicao.put("triggerText", elementText);
            transicao.put("elementTag", elementTag);
            transicao.put("elementId", elementId);
            transicao.put("elementClasses", elementClasses);
            transicao.put("elementText", elementText);
            transicao.put("elementName", elementName);
            transicao.put("elementRole", elementRole);
            transicao.put("elementAriaLabel", elementAria);
            transicao.put("elementHref", elementHref);
            transicao.put("inputType", inputType);
            transicao.put("interactionKind", classifyInteractionKind(elementTag, inputType, elementHref, elementRole));

            ObservedResult observedResult = observedResultExtractor.extract(
                edge.getSourceStateVertex().getDom(),
                edge.getTargetStateVertex().getDom()
            );
            transicao.put("observedText", observedResult.text());
            transicao.put("observedElementId", observedResult.elementId());
            transicao.put("observedElementRole", observedResult.role());

            // Montar mapa de seletores com múltiplas opções (usar identification como possível xpath/cs)
            Map<String, Object> selectors = new HashMap<>();
            putSelectorIfUseful(selectors, "id", elementId, 120);
            putSelectorIfUseful(selectors, "name", elementName, 120);
            putSelectorIfUseful(selectors, "aria_label", elementAria, 120);
            putSelectorIfUseful(selectors, "text", elementText, 80);
            putSelectorIfUseful(selectors, "href", elementHref, 240);
            putSelectorIfUseful(selectors, "class", elementClasses, 160);
            putSelectorIfUseful(selectors, "role", elementRole, 80);
            // Se o identification contiver xpath/css, incluir como fallback
            if (selectorTipo != null && selectorValor != null && !"desconhecido".equals(selectorValor)) {
                if (selectorTipo.contains("xpath")) {
                    selectors.put("xpath", selectorValor);
                } else if (selectorTipo.contains("css") || selectorTipo.contains("selector")) {
                    selectors.put("css", selectorValor);
                } else {
                    // ainda assim expor como xpath fallback
                    selectors.put("xpath", selectorValor);
                }
            }

            transicao.put("selectorsJson", toJson(selectors));

            arestas.add(transicao);
        }

        return arestas;
    }

    private void persistGraph(
        String neo4jUri,
        String neo4jUser,
        String neo4jPassword,
        List<Map<String, Object>> nos,
        List<Map<String, Object>> elementos,
        List<Map<String, Object>> arestas
    ) {
        try (Driver driver = GraphDatabase.driver(neo4jUri, AuthTokens.basic(neo4jUser, neo4jPassword));
             Session neo4jSession = driver.session()) {
            driver.verifyConnectivity();

            // Schema operations must run in a dedicated transaction.
            neo4jSession.executeWrite((TransactionContext tx) -> {
                tx.run("CREATE CONSTRAINT page_state_id_unique IF NOT EXISTS FOR (n:PageState) REQUIRE n.id IS UNIQUE");
                tx.run("CREATE CONSTRAINT ui_element_id_unique IF NOT EXISTS FOR (n:UiElement) REQUIRE n.id IS UNIQUE");
                return null;
            });

            // Data cleanup in a separate write transaction.
            neo4jSession.executeWrite((TransactionContext tx) -> {
                tx.run("MATCH (n:UiElement) DETACH DELETE n");
                tx.run("MATCH (n:PageState) DETACH DELETE n");
                return null;
            });

            // Batch insert nodes and edges in a separate write transaction.
            neo4jSession.executeWrite((TransactionContext tx) -> {
                tx.run(
                    "UNWIND $nodes AS node "
                        + "MERGE (n:PageState {id: node.id}) "
                        + "SET n.url = node.url, "
                        + "n.title = node.title, "
                        + "n.state_count = node.state_count, "
                        + "n.h1 = node.h1, "
                        + "n.visible_text_excerpt = node.visible_text_excerpt, "
                        + "n.interactive_count = node.interactive_count, "
                        + "n.screenshot_path = node.screenshot_path",
                    Map.of("nodes", nos)
                );
                tx.run(
                    "UNWIND $elements AS element "
                        + "MATCH (page:PageState {id: element.page_id}) "
                        + "MERGE (control:UiElement {id: element.id}) "
                        + "SET control.page_url = element.page_url, "
                        + "control.kind = element.kind, "
                        + "control.suggested_operation = element.suggested_operation, "
                        + "control.tag = element.tag, "
                        + "control.text = element.text, "
                        + "control.title = element.title, "
                        + "control.label = element.label, "
                        + "control.data_testid = element.data_testid, "
                        + "control.id_attribute = element.id_attribute, "
                        + "control.name = element.name, "
                        + "control.input_type = element.input_type, "
                        + "control.value = element.value, "
                        + "control.href = element.href, "
                        + "control.role = element.role, "
                        + "control.aria_label = element.aria_label, "
                        + "control.placeholder = element.placeholder, "
                        + "control.form_action = element.form_action, "
                        + "control.form_method = element.form_method "
                        + "MERGE (page)-[:HAS_ELEMENT]->(control)",
                    Map.of("elements", elementos)
                );
                tx.run(
                    "UNWIND $edges AS edge "
                        + "MATCH (origem:PageState {id: edge.origem}) "
                        + "MATCH (destino:PageState {id: edge.destino}) "
                        + "MERGE (origem)-[r:NAVIGATES_TO {selector_value: edge.selectorValue, action: edge.action, destino_id: edge.destino}]->(destino) "
                        + "SET r.selector_type = edge.selectorType, "
                        + "r.trigger_type = edge.triggerType, "
                        + "r.trigger_text = edge.triggerText, "
                        + "r.interaction_kind = edge.interactionKind, "
                        + "r.element_tag = edge.elementTag, "
                        + "r.element_id = edge.elementId, "
                        + "r.element_classes = edge.elementClasses, "
                        + "r.element_text = edge.elementText, "
                        + "r.element_name = edge.elementName, "
                        + "r.element_role = edge.elementRole, "
                        + "r.element_aria_label = edge.elementAriaLabel, "
                        + "r.element_href = edge.elementHref, "
                        + "r.input_type = edge.inputType, "
                        + "r.selectors_json = edge.selectorsJson, "
                        + "r.observed_text = edge.observedText, "
                        + "r.observed_element_id = edge.observedElementId, "
                        + "r.observed_element_role = edge.observedElementRole",
                    Map.of("edges", arestas)
                );
                return null;
            });

            System.out.println(
                "Persistência concluída no Neo4j. Páginas: " + nos.size()
                    + " | Controles: " + elementos.size()
                    + " | Transições: " + arestas.size()
            );
        } catch (Exception e) {
            System.err.println("Erro ao persistir grafo no Neo4j: " + e.getMessage());
        }
    }

    private void captureStateScreenshot(CrawlerContext context, StateVertex state) {
        if (context == null || state == null || stateScreenshots.containsKey(state.getName())) {
            return;
        }

        File screenshotDir = new File("/app/output", "page_state_screenshots");
        if (!screenshotDir.exists() && !screenshotDir.mkdirs()) {
            System.out.println("Aviso: nao foi possivel criar diretorio de screenshots: " + screenshotDir);
            return;
        }

        File screenshotFile = new File(screenshotDir, safeFileName(state.getName()) + ".png");
        try {
            context.getBrowser().saveScreenShot(screenshotFile);
            stateScreenshots.put(state.getName(), screenshotFile.getPath());
        } catch (Exception ex) {
            System.out.println("Aviso: falha ao capturar screenshot do estado " + state.getName() + ": " + ex.getMessage());
        }
    }

    private String toJson(Map<?, ?> value) {
        try {
            return JSON_MAPPER.writeValueAsString(value);
        } catch (JsonProcessingException e) {
            return "{}";
        }
    }

    private void putSelectorIfUseful(Map<String, Object> selectors, String selectorName, String value, int maxLength) {
        String normalized = EnvironmentUtils.safeValue(value, "");
        if (!normalized.isBlank() && normalized.length() <= maxLength) {
            selectors.put(selectorName, normalized);
        }
    }

    private String extractFirstTagText(String dom, String tagName, String fallback) {
        if (dom == null || dom.isBlank()) {
            return fallback;
        }

        Pattern pattern = Pattern.compile("(?is)<" + tagName + "[^>]*>(.*?)</" + tagName + ">");
        Matcher matcher = pattern.matcher(dom);
        if (!matcher.find()) {
            return fallback;
        }
        return normalizeHtmlText(matcher.group(1), 200);
    }

    private String extractVisibleText(String dom, int maxLength) {
        if (dom == null || dom.isBlank()) {
            return "";
        }
        String withoutScripts = dom
            .replaceAll("(?is)<script[^>]*>.*?</script>", " ")
            .replaceAll("(?is)<style[^>]*>.*?</style>", " ")
            .replaceAll("(?is)<noscript[^>]*>.*?</noscript>", " ");
        return normalizeHtmlText(withoutScripts, maxLength);
    }

    private String normalizeHtmlText(String html, int maxLength) {
        String text = html
            .replaceAll("(?is)<[^>]+>", " ")
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", "\"")
            .replace("&#39;", "'")
            .replaceAll("\\s+", " ")
            .trim();
        if (text.length() <= maxLength) {
            return text;
        }
        return text.substring(0, maxLength).trim();
    }

    private int countInteractiveElements(String dom) {
        if (dom == null || dom.isBlank()) {
            return 0;
        }
        Pattern pattern = Pattern.compile("(?is)<(a|button|input|select|textarea|summary)\\b");
        Matcher matcher = pattern.matcher(dom);
        int count = 0;
        while (matcher.find()) {
            count++;
        }
        return count;
    }

    private String safeFileName(String value) {
        return EnvironmentUtils.safeValue(value, "state").replaceAll("[^a-zA-Z0-9._-]", "_");
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

    private String classifyInteractionKind(String elementTag, String inputType, String elementHref, String elementRole) {
        String tag = EnvironmentUtils.safeValue(elementTag, "").toLowerCase();
        String type = EnvironmentUtils.safeValue(inputType, "").toLowerCase();
        String href = EnvironmentUtils.safeValue(elementHref, "");
        String role = EnvironmentUtils.safeValue(elementRole, "").toLowerCase();

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
