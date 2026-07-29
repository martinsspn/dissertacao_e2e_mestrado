package br.ufrn.mestrado.bootstrap;

import br.ufrn.mestrado.config.CrawlRuntimeProfile;
import br.ufrn.mestrado.config.CrawljaxConfigFactory;
import br.ufrn.mestrado.infra.CrawlRunManifestWriter;
import br.ufrn.mestrado.infra.SeleniumAvailabilityChecker;
import br.ufrn.mestrado.plugin.SemanticExportPlugin;
import com.crawljax.core.CrawljaxRunner;
import com.crawljax.core.configuration.BrowserConfiguration;
import com.crawljax.core.configuration.CrawljaxConfiguration;
import com.crawljax.core.configuration.CrawljaxConfiguration.CrawljaxConfigurationBuilder;
import org.openqa.selenium.remote.DesiredCapabilities;

public class ExplorerBootstrap {

    public void run() {
        String targetUrl = resolveTargetUrl();
        System.out.println("Iniciando exploração no alvo: " + targetUrl);

        CrawljaxConfigurationBuilder builder = CrawljaxConfiguration.builderFor(targetUrl);

        String seleniumHubUrl = resolveSeleniumHubUrl();
        SeleniumAvailabilityChecker.waitForSeleniumReady(seleniumHubUrl, 180, false);

        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setBrowserName("chrome");
        builder.setBrowserConfig(BrowserConfiguration.remoteConfig(1, seleniumHubUrl, capabilities));

        CrawlRuntimeProfile profile = CrawlRuntimeProfile.fromEnvironment();
        CrawljaxConfigFactory.applyRuntimeProfile(builder, profile);
        logRuntimeProfile(profile);
        System.out.println("Manifesto da exploracao -> " + CrawlRunManifestWriter.write(targetUrl, profile));

        builder.addPlugin(new SemanticExportPlugin());

        CrawljaxRunner crawljax = new CrawljaxRunner(builder.build());
        crawljax.call();
    }

    private String resolveTargetUrl() {
        String targetUrl = System.getenv("TARGET_URL");
        if (targetUrl == null || targetUrl.isEmpty()) {
            targetUrl = "https://demowebshop.tricentis.com/";
            System.out.println("Aviso: TARGET_URL não definida. Usando " + targetUrl);
        }
        return targetUrl;
    }

    private String resolveSeleniumHubUrl() {
        String seleniumHubUrl = System.getenv("SELENIUM_HUB_URL");
        if (seleniumHubUrl == null || seleniumHubUrl.isEmpty()) {
            seleniumHubUrl = "http://localhost:4444/wd/hub";
        }
        return seleniumHubUrl;
    }

    private void logRuntimeProfile(CrawlRuntimeProfile profile) {
        System.out.println(
            "Perfil de exploracao -> depth=" + profile.maxDepth()
                + ", states=" + profile.maxStates()
                + ", runtime(min)=" + profile.maxRuntimeMinutes()
                + ", waitReload(ms)=" + profile.waitAfterReloadMs()
                + ", waitEvent(ms)=" + profile.waitAfterEventMs()
                + ", clickOnce=" + profile.clickOnce()
                + ", randomOrder=" + profile.randomOrder()
        );
    }
}
