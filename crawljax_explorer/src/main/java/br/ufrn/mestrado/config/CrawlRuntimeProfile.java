package br.ufrn.mestrado.config;

public record CrawlRuntimeProfile(
    int maxDepth,
    int maxStates,
    int maxRuntimeMinutes,
    int waitAfterReloadMs,
    int waitAfterEventMs,
    boolean clickOnce,
    boolean randomOrder
) {
}