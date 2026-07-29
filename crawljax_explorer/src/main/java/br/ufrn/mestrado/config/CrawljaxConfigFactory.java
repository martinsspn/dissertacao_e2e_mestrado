package br.ufrn.mestrado.config;

import com.crawljax.core.configuration.CrawljaxConfiguration.CrawljaxConfigurationBuilder;
import com.crawljax.core.configuration.CrawlRules.CrawlPriorityMode;
import com.crawljax.oraclecomparator.OracleComparator;
import com.crawljax.oraclecomparator.comparators.XPathExpressionComparator;

import java.util.concurrent.TimeUnit;

public final class CrawljaxConfigFactory {

    static final String DYNAMIC_CAROUSEL_XPATH =
        "//*[contains(concat(' ', normalize-space(@class), ' '), ' slider-wrapper ')]";
    static final String DYNAMIC_RECENTLY_VIEWED_XPATH =
        "//*[contains(concat(' ', normalize-space(@class), ' '), ' block-recently-viewed-products ')]";

    private CrawljaxConfigFactory() {
    }

    public static void applyRuntimeProfile(CrawljaxConfigurationBuilder builder, CrawlRuntimeProfile profile) {
        // Politica padrao de exploracao: ampla o bastante para descobrir fluxos
        // relevantes, mas limitada para manter o grafo finito e reprodutivel.
        builder.crawlRules().clickOnce(profile.clickOnce());
        builder.crawlRules().clickElementsInRandomOrder(profile.randomOrder());
        builder.crawlRules().setCrawlPriorityMode(CrawlPriorityMode.SHALLOW_FIRST);
        builder.crawlRules().crawlHiddenAnchors(false);
        builder.crawlRules().followExternalLinks(false);

        // O Nivo Slider troca automaticamente imagem, atributos e links. Sem esta
        // normalizacao, cada frame e interpretado como um estado novo e o reset da
        // pagina inicial deixa de reconhecer o estado index.
        builder.crawlRules().addOracleComparator(
            new OracleComparator(
                "ignore-dynamic-carousel",
                new XPathExpressionComparator(DYNAMIC_CAROUSEL_XPATH)
            ),
            new OracleComparator(
                "ignore-recently-viewed-products",
                new XPathExpressionComparator(DYNAMIC_RECENTLY_VIEWED_XPATH)
            )
        );

        builder.crawlRules().waitAfterReloadUrl(profile.waitAfterReloadMs(), TimeUnit.MILLISECONDS);
        builder.crawlRules().waitAfterEvent(profile.waitAfterEventMs(), TimeUnit.MILLISECONDS);

        // A exploracao descobre rotas por links. Botoes, campos e demais controles
        // continuam extraidos do HTML, mas nao sao executados pelo crawler: isso
        // evita mutar carrinho, sessao e formularios durante o mapeamento.
        builder.crawlRules().click("a");
        builder.crawlRules().dontClickChildrenOf("div").withClass("slider-wrapper");
        builder.crawlRules().dontClickChildrenOf("div").withClass("picture");
        builder.crawlRules().dontClickChildrenOf("div").withClass("picture-thumbs");
        builder.crawlRules().dontClick("a").withAttribute("href", "#");

        builder.setMaximumDepth(profile.maxDepth());
        builder.setMaximumStates(profile.maxStates());
        builder.setMaximumRunTime(profile.maxRuntimeMinutes(), TimeUnit.MINUTES);
    }
}
