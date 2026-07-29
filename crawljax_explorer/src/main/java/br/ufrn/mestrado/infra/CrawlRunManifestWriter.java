package br.ufrn.mestrado.infra;

import br.ufrn.mestrado.config.CrawlRuntimeProfile;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.OffsetDateTime;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class CrawlRunManifestWriter {

    private CrawlRunManifestWriter() {
    }

    public static Path write(String targetUrl, CrawlRuntimeProfile profile) {
        String configuredPath = System.getenv("CRAWL_MANIFEST_PATH");
        Path outputPath = Path.of(
            configuredPath == null || configuredPath.isBlank()
                ? "/app/output/crawl_run_manifest.json"
                : configuredPath
        );

        Map<String, Object> manifest = new LinkedHashMap<>();
        manifest.put("target_url", targetUrl);
        manifest.put("started_at", OffsetDateTime.now().toString());
        manifest.put("max_depth", profile.maxDepth());
        manifest.put("max_states", profile.maxStates());
        manifest.put("max_runtime_minutes", profile.maxRuntimeMinutes());
        manifest.put("wait_after_reload_ms", profile.waitAfterReloadMs());
        manifest.put("wait_after_event_ms", profile.waitAfterEventMs());
        manifest.put("click_once", profile.clickOnce());
        manifest.put("random_order", profile.randomOrder());
        manifest.put("crawl_priority", "SHALLOW_FIRST");
        manifest.put("crawl_hidden_anchors", false);
        manifest.put("follow_external_links", false);
        manifest.put("exploration_actions", "navigation_anchors_only");
        manifest.put("clicked_element_tags", List.of("a"));
        manifest.put(
            "ignored_dynamic_regions",
            List.of("slider-wrapper", "block-recently-viewed-products")
        );
        manifest.put(
            "excluded_click_regions",
            List.of("slider-wrapper", "picture", "picture-thumbs", "a[href=#]")
        );
        manifest.put("graph_schema_version", 2);
        manifest.put("structured_ui_elements", true);
        manifest.put("observed_transition_results", true);

        try {
            if (outputPath.getParent() != null) {
                Files.createDirectories(outputPath.getParent());
            }
            new ObjectMapper()
                .enable(SerializationFeature.INDENT_OUTPUT)
                .writeValue(outputPath.toFile(), manifest);
            return outputPath;
        } catch (IOException exception) {
            throw new IllegalStateException("Nao foi possivel registrar o manifesto da exploracao", exception);
        }
    }
}
