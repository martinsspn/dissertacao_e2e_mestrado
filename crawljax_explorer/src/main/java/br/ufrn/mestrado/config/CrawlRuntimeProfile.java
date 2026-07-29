package br.ufrn.mestrado.config;

import br.ufrn.mestrado.infra.EnvironmentUtils;

public record CrawlRuntimeProfile(
    int maxDepth,
    int maxStates,
    int maxRuntimeMinutes,
    int waitAfterReloadMs,
    int waitAfterEventMs,
    boolean clickOnce,
    boolean randomOrder
) {
    public static CrawlRuntimeProfile defaultProfile() {
        return new CrawlRuntimeProfile(
            8,
            400,
            45,
            3000,
            2200,
            true,
            false
        );
    }

    public static CrawlRuntimeProfile fromEnvironment() {
        CrawlRuntimeProfile defaults = defaultProfile();
        return new CrawlRuntimeProfile(
            EnvironmentUtils.getIntEnvOrDefault("CRAWL_MAX_DEPTH", defaults.maxDepth()),
            EnvironmentUtils.getIntEnvOrDefault("CRAWL_MAX_STATES", defaults.maxStates()),
            EnvironmentUtils.getIntEnvOrDefault("CRAWL_MAX_RUNTIME_MINUTES", defaults.maxRuntimeMinutes()),
            EnvironmentUtils.getIntEnvOrDefault("CRAWL_WAIT_AFTER_RELOAD_MS", defaults.waitAfterReloadMs()),
            EnvironmentUtils.getIntEnvOrDefault("CRAWL_WAIT_AFTER_EVENT_MS", defaults.waitAfterEventMs()),
            EnvironmentUtils.getBooleanEnvOrDefault("CRAWL_CLICK_ONCE", defaults.clickOnce()),
            EnvironmentUtils.getBooleanEnvOrDefault("CRAWL_RANDOM_ORDER", defaults.randomOrder())
        );
    }
}
