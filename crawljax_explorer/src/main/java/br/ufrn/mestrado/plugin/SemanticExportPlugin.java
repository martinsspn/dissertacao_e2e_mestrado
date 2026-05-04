package br.ufrn.mestrado.plugin;

import br.ufrn.mestrado.infra.EnvironmentUtils;

import com.crawljax.core.CrawlSession;
import com.crawljax.core.ExitNotifier.ExitStatus;
import com.crawljax.core.plugin.PostCrawlingPlugin;
import com.crawljax.core.state.Element;
import com.crawljax.core.state.Eventable;
import com.crawljax.core.state.Identification;
import com.crawljax.core.state.StateFlowGraph;
import com.crawljax.core.state.StateVertex;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;
import org.neo4j.driver.TransactionContext;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SemanticExportPlugin implements PostCrawlingPlugin {

    private static final ObjectMapper JSON_MAPPER = new ObjectMapper();

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
        List<Map<String, Object>> arestas = mapEdgesToRelationships(sfg, stateUrlMapping);

        persistGraph(neo4jUri, neo4jUser, neo4jPassword, nos, arestas);
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

            // Consolidar por URL - usar URL como chave única
            if (!urlToNode.containsKey(url)) {
                Map<String, Object> no = new HashMap<>();
                no.put("id", generateIdFromUrl(url));  // ID seguro baseado em URL
                no.put("url", url);
                no.put("title", title);
                no.put("state_count", 1);  // Rastrear quantos estados foram consolidados
                urlToNode.put(url, no);
            } else {
                // Incrementar contador de estados consolidados
                Map<String, Object> existing = urlToNode.get(url);
                int count = (Integer) existing.getOrDefault("state_count", 1);
                existing.put("state_count", count + 1);
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

            // Montar mapa de seletores com múltiplas opções (usar identification como possível xpath/cs)
            Map<String, Object> selectors = new HashMap<>();
            if (elementId != null && !elementId.isBlank()) selectors.put("id", elementId);
            if (elementName != null && !elementName.isBlank()) selectors.put("name", elementName);
            if (elementAria != null && !elementAria.isBlank()) selectors.put("aria_label", elementAria);
            if (elementText != null && !elementText.isBlank()) selectors.put("text", elementText);
            if (elementHref != null && !elementHref.isBlank()) selectors.put("href", elementHref);
            if (elementClasses != null && !elementClasses.isBlank()) selectors.put("class", elementClasses);
            if (elementRole != null && !elementRole.isBlank()) selectors.put("role", elementRole);
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

            // Score de robustez para priorização no gerador
            Map<String, Integer> selectorScores = new HashMap<>();
            selectorScores.put("id", 5);
            selectorScores.put("aria_label", 4);
            selectorScores.put("name", 4);
            selectorScores.put("text", 3);
            selectorScores.put("href", 3);
            selectorScores.put("css", 2);
            selectorScores.put("class", 2);
            selectorScores.put("role", 2);
            selectorScores.put("xpath", 1);

            transicao.put("selectorsJson", toJson(selectors));
            transicao.put("selectorScoresJson", toJson(selectorScores));

            arestas.add(transicao);
        }

        return arestas;
    }

    private void persistGraph(
        String neo4jUri,
        String neo4jUser,
        String neo4jPassword,
        List<Map<String, Object>> nos,
        List<Map<String, Object>> arestas
    ) {
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
                    "UNWIND $nodes AS node "
                        + "MERGE (n:PageState {id: node.id}) "
                        + "SET n.url = node.url, n.title = node.title, n.state_count = node.state_count",
                    Map.of("nodes", nos)
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
                        + "r.selector_scores_json = edge.selectorScoresJson",
                    Map.of("edges", arestas)
                );
                return null;
            });

            System.out.println("Persistência concluída no Neo4j. Nós: " + nos.size() + " | Arestas: " + arestas.size());
        } catch (Exception e) {
            System.err.println("Erro ao persistir grafo no Neo4j: " + e.getMessage());
        }
    }

    private String toJson(Map<?, ?> value) {
        try {
            return JSON_MAPPER.writeValueAsString(value);
        } catch (JsonProcessingException e) {
            return "{}";
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
