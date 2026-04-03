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
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
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
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setBrowserName("chrome");
        builder.setBrowserConfig(BrowserConfiguration.remoteConfig(1, seleniumHubUrl, capabilities));

        // Regras para exploração ampla e profunda da aplicação
        builder.crawlRules().clickOnce(true);
        
        // Configura tempos de espera para lidar com carregamento dinâmico (AJAX/JS)
        builder.crawlRules().waitAfterReloadUrl(2000, TimeUnit.MILLISECONDS);
        builder.crawlRules().waitAfterEvent(1500, TimeUnit.MILLISECONDS);

        // O que o Crawler deve clicar
        builder.crawlRules().clickDefaultElements(); // Clica em tags <a>, <button>, <input>
        builder.crawlRules().click("div"); // Clica em divs interagíveis
        builder.crawlRules().click("span"); // Clica em spans interagíveis
        builder.crawlRules().click("li"); // Clica em itens de lista
        builder.crawlRules().click("img"); // Clica em imagens

        // Limites da exploração (Aumentados para maior cobertura)
        builder.setMaximumDepth(5); 
        builder.setMaximumStates(150); 
        builder.setMaximumRunTime(30, TimeUnit.MINUTES);

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
            System.out.println("Iniciando exportação dos estados e transições...");

            StateFlowGraph sfg = session.getStateFlowGraph();
            String outputDir = "/app/output/"; // Este é o mapeamento do volume no Docker
            new File(outputDir).mkdirs();

            ObjectMapper mapper = new ObjectMapper();
            List<Map<String, String>> nos = new ArrayList<>();
            List<Map<String, String>> arestas = new ArrayList<>();

            try {
                // Exporta apenas os nós do grafo (sem snapshot completo)
                for (StateVertex state : sfg.getAllStates()) {
                    Map<String, String> no = new HashMap<>();
                    String dom = state.getDom() == null ? "" : state.getDom();
                    String domCanonico = canonicalizeDom(dom);

                    no.put("id", state.getName());
                    no.put("url_canonica", safeValue(state.getUrl(), "url_desconhecida"));
                    no.put("titulo", extractTitleFromDom(dom));
                    no.put("h1_principal", extractFirstTagText(dom, "h1", "sem_h1"));
                    no.put("form_ids_presentes", extractFormIds(dom));
                    no.put("mensagens_erro_visiveis", extractErrorMessages(dom));
                    no.put("interactive_count", String.valueOf(countInteractiveElements(dom)));
                    no.put("dom_hash_canonico", sha256(domCanonico));
                    no.put("dom_tamanho", String.valueOf(dom.length()));

                    nos.add(no);
                }

                // Exporta as transições (Arestas) para o JSON
                for (Eventable edge : sfg.getAllEdges()) {
                    Map<String, String> transicao = new HashMap<>();
                    transicao.put("origem", edge.getSourceStateVertex().getName());
                    transicao.put("destino", edge.getTargetStateVertex().getName());
                    transicao.put("acao", edge.getEventType().toString());

                    Identification identification = edge.getIdentification();
                    String selectorTipo = "desconhecido";
                    String selectorValor = "desconhecido";
                    if (identification != null) {
                        selectorTipo = identification.getHow() == null ? "desconhecido" : identification.getHow().toString().toLowerCase();
                        selectorValor = safeValue(identification.getValue(), "desconhecido");
                    }
                    transicao.put("selector_tipo", selectorTipo);
                    transicao.put("selector_valor", selectorValor);
                    transicao.put("xpath_do_elemento", selectorValor);

                    Element element = edge.getElement();
                    transicao.put("element_tag", element == null ? "desconhecido" : safeValue(element.getTag(), "desconhecido"));
                    String elementText = element == null ? "" : safeValue(element.getText(), "");
                    transicao.put("element_text", elementText);
                    transicao.put("trigger_text", elementText);
                    transicao.put("element_id", element == null ? "" : safeValue(element.getElementId(), ""));
                    transicao.put("aria_label", element == null ? "" : safeValue(element.getAttributeOrNull("aria-label"), ""));
                    transicao.put("title_attr", element == null ? "" : safeValue(element.getAttributeOrNull("title"), ""));
                    transicao.put("input_type", element == null ? "" : safeValue(element.getAttributeOrNull("type"), ""));
                    transicao.put("input_name", element == null ? "" : safeValue(element.getAttributeOrNull("name"), ""));
                    transicao.put("input_id", element == null ? "" : safeValue(element.getAttributeOrNull("id"), ""));
                    transicao.put("href", element == null ? "" : safeValue(element.getAttributeOrNull("href"), ""));
                    transicao.put("form_action", element == null ? "" : safeValue(element.getAttributeOrNull("formaction"), ""));
                    transicao.put("related_frame", safeValue(edge.getRelatedFrame(), ""));
                    
                    arestas.add(transicao);
                }

                // Grava os arquivos JSON de nós e arestas
                mapper.writerWithDefaultPrettyPrinter().writeValue(new File(outputDir + "nos.json"), nos);
                mapper.writerWithDefaultPrettyPrinter().writeValue(new File(outputDir + "arestas.json"), arestas);
                cleanupHtmlSnapshots(outputDir);
                
                System.out.println("Exportação concluída com sucesso no diretório: " + outputDir);

            } catch (IOException e) {
                System.err.println("Erro ao salvar os arquivos de saída: " + e.getMessage());
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

        private String extractFirstTagText(String dom, String tagName, String fallback) {
            if (dom == null || dom.isBlank()) {
                return fallback;
            }
            Pattern pattern = Pattern.compile("(?is)<" + tagName + "[^>]*>(.*?)</" + tagName + ">");
            Matcher matcher = pattern.matcher(dom);
            if (!matcher.find()) {
                return fallback;
            }
            String valor = matcher.group(1)
                    .replaceAll("(?is)<[^>]+>", " ")
                    .replaceAll("\\s+", " ")
                    .trim();
            return valor.isEmpty() ? fallback : valor;
        }

        private String extractFormIds(String dom) {
            if (dom == null || dom.isBlank()) {
                return "";
            }
            Pattern formPattern = Pattern.compile("(?is)<form[^>]*>");
            Pattern idPattern = Pattern.compile("(?is)\\bid\\s*=\\s*['\"]([^'\"]+)['\"]");
            Matcher formMatcher = formPattern.matcher(dom);
            Set<String> formIds = new LinkedHashSet<>();
            int semId = 0;

            while (formMatcher.find()) {
                String formTag = formMatcher.group();
                Matcher idMatcher = idPattern.matcher(formTag);
                if (idMatcher.find()) {
                    formIds.add(idMatcher.group(1).trim());
                } else {
                    semId++;
                    formIds.add("form_sem_id_" + semId);
                }
            }
            return String.join("|", formIds);
        }

        private String extractErrorMessages(String dom) {
            if (dom == null || dom.isBlank()) {
                return "";
            }
            Pattern pattern = Pattern.compile("(?is)<[^>]*class=['\"][^'\"]*(error|validation|alert)[^'\"]*['\"][^>]*>(.*?)</[^>]+>");
            Matcher matcher = pattern.matcher(dom);
            Set<String> mensagens = new LinkedHashSet<>();

            while (matcher.find()) {
                String texto = matcher.group(2)
                        .replaceAll("(?is)<[^>]+>", " ")
                        .replaceAll("\\s+", " ")
                        .trim();
                if (!texto.isEmpty() && texto.length() <= 220) {
                    mensagens.add(texto);
                }
            }

            return String.join("|", mensagens);
        }

        private int countInteractiveElements(String dom) {
            if (dom == null || dom.isBlank()) {
                return 0;
            }
            Pattern pattern = Pattern.compile("(?is)<(a|button|input|select|textarea)\\b");
            Matcher matcher = pattern.matcher(dom);
            int count = 0;
            while (matcher.find()) {
                count++;
            }
            return count;
        }

        private String canonicalizeDom(String dom) {
            if (dom == null || dom.isBlank()) {
                return "";
            }
            String semComentarios = dom.replaceAll("(?is)<!--.*?-->", " ");
            String semScript = semComentarios.replaceAll("(?is)<script[^>]*>.*?</script>", " ");
            String semStyle = semScript.replaceAll("(?is)<style[^>]*>.*?</style>", " ");
            return semStyle.replaceAll("\\s+", " ").trim().toLowerCase();
        }

        private String sha256(String valor) {
            try {
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] hash = digest.digest(valor.getBytes(StandardCharsets.UTF_8));
                StringBuilder hex = new StringBuilder();
                for (byte b : hash) {
                    String h = Integer.toHexString(0xff & b);
                    if (h.length() == 1) {
                        hex.append('0');
                    }
                    hex.append(h);
                }
                return hex.toString();
            } catch (NoSuchAlgorithmException e) {
                return "hash_indisponivel";
            }
        }

        private void cleanupHtmlSnapshots(String outputDir) {
            File pasta = new File(outputDir);
            File[] arquivos = pasta.listFiles((dir, name) -> name.toLowerCase().endsWith(".html"));
            if (arquivos == null) {
                return;
            }
            for (File arquivo : arquivos) {
                if (!arquivo.delete()) {
                    System.err.println("Aviso: não foi possível remover snapshot: " + arquivo.getName());
                }
            }
        }

        private String safeValue(String value, String fallback) {
            if (value == null) {
                return fallback;
            }
            String normalized = value.replaceAll("\\s+", " ").trim();
            return normalized.isEmpty() ? fallback : normalized;
        }
    }
}