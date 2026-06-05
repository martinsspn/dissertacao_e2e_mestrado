package br.ufrn.mestrado.config;

import com.crawljax.core.configuration.CrawljaxConfiguration.CrawljaxConfigurationBuilder;

import java.util.concurrent.TimeUnit;

public final class CrawljaxConfigFactory {

    private CrawljaxConfigFactory() {
    }

    public static void applyRuntimeProfile(CrawljaxConfigurationBuilder builder, CrawlRuntimeProfile profile) {
        // Politica padrao de exploracao: ampla o bastante para descobrir fluxos
        // relevantes, mas limitada para manter o grafo finito e reprodutivel.
        builder.crawlRules().clickOnce(profile.clickOnce());
        builder.crawlRules().clickElementsInRandomOrder(profile.randomOrder());
        builder.crawlRules().crawlHiddenAnchors(true);

        builder.crawlRules().waitAfterReloadUrl(profile.waitAfterReloadMs(), TimeUnit.MILLISECONDS);
        builder.crawlRules().waitAfterEvent(profile.waitAfterEventMs(), TimeUnit.MILLISECONDS);

        builder.crawlRules().clickDefaultElements();
        builder.crawlRules().click("label");
        builder.crawlRules().click("summary");
        builder.crawlRules().click("option");
        builder.crawlRules().click("input").withAttribute("type", "submit");
        builder.crawlRules().click("input").withAttribute("type", "button");
        builder.crawlRules().click("input").withAttribute("type", "radio");
        builder.crawlRules().click("input").withAttribute("type", "checkbox");
        builder.crawlRules().click("div");
        builder.crawlRules().click("span");
        builder.crawlRules().click("li");
        builder.crawlRules().click("img");

        builder.setMaximumDepth(profile.maxDepth());
        builder.setMaximumStates(profile.maxStates());
        builder.setMaximumRunTime(profile.maxRuntimeMinutes(), TimeUnit.MINUTES);
    }
}
