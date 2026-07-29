package br.ufrn.mestrado.config;

import com.crawljax.core.configuration.CrawljaxConfiguration;
import com.crawljax.core.configuration.CrawlRules.CrawlPriorityMode;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CrawljaxConfigFactoryTest {

    @Test
    void exploresOnlyNavigationAnchorsAndIgnoresDynamicRegions() {
        CrawljaxConfiguration.CrawljaxConfigurationBuilder builder =
            CrawljaxConfiguration.builderFor("https://example.test/");

        CrawljaxConfigFactory.applyRuntimeProfile(builder, CrawlRuntimeProfile.defaultProfile());
        CrawljaxConfiguration configuration = builder.build();

        assertFalse(configuration.getCrawlRules().isCrawlHiddenAnchors());
        assertFalse(configuration.getCrawlRules().isFollowExternalLinks());
        assertEquals(CrawlPriorityMode.SHALLOW_FIRST, configuration.getCrawlRules().getCrawlPriorityMode());
        assertTrue(
            configuration.getCrawlRules().getOracleComparators().stream()
                .anyMatch(item -> "ignore-dynamic-carousel".equals(item.getId()))
        );
        assertTrue(
            configuration.getCrawlRules().getOracleComparators().stream()
                .anyMatch(item -> "ignore-recently-viewed-products".equals(item.getId()))
        );
        assertEquals(1, configuration.getCrawlRules().getPreCrawlConfig().getIncludedElements().size());
        assertEquals(
            "A",
            configuration.getCrawlRules().getPreCrawlConfig().getIncludedElements().get(0).getTagName()
        );
        assertTrue(
            configuration.getCrawlRules().getPreCrawlConfig().getExcludedElements().stream()
                .anyMatch(item -> item.getWithXpathExpression() != null
                    && item.getWithXpathExpression().contains("slider-wrapper"))
        );
    }
}
