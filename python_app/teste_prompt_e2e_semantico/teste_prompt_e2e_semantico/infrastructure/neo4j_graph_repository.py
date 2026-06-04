from __future__ import annotations

import json
import time

try:
    from neo4j import GraphDatabase
except ModuleNotFoundError:  # pragma: no cover - external dependency
    GraphDatabase = None

from teste_prompt_e2e_semantico.config import PromptGeneratorConfig
from teste_prompt_e2e_semantico.domain.models import NavigationGraph, NavigationTransition, PageNode


class Neo4jNavigationGraphRepository:
    def __init__(self, config: PromptGeneratorConfig) -> None:
        if GraphDatabase is None:
            raise ModuleNotFoundError(
                "A dependencia 'neo4j' nao esta instalada. Execute 'pip install -r requirements.txt' ou 'pip install neo4j==5.16.0'."
            )
        self._driver = GraphDatabase.driver(
            config.neo4j_uri,
            auth=(config.neo4j_user, config.neo4j_password),
        )
        self._ready_timeout_seconds = config.neo4j_ready_timeout_seconds

    def close(self) -> None:
        self._driver.close()

    def get_navigation_graph(self, max_edges: int) -> NavigationGraph:
        self._wait_until_ready()
        return NavigationGraph(
            pages=self._get_page_catalog(),
            transitions=self._get_transitions(max_edges),
        )

    def _get_page_catalog(self) -> list[PageNode]:
        query = """
            MATCH (n:PageState)
            RETURN n.id AS id,
                   n.url AS url,
                   coalesce(n.title, '') AS title,
                   coalesce(n.state_count, 1) AS state_count,
                   coalesce(n.h1, '') AS h1,
                   coalesce(n.visible_text_excerpt, '') AS visible_text_excerpt,
                   coalesce(n.interactive_count, 0) AS interactive_count,
                   coalesce(n.screenshot_path, '') AS screenshot_path
            ORDER BY state_count DESC, url
        """
        with self._driver.session() as session:
            result = session.run(query)
            return [
                PageNode(
                    id=record["id"],
                    url=record["url"],
                    title=record["title"],
                    state_count=int(record["state_count"] or 1),
                    h1=record["h1"],
                    visible_text_excerpt=record["visible_text_excerpt"],
                    interactive_count=int(record["interactive_count"] or 0),
                    screenshot_path=record["screenshot_path"],
                )
                for record in result
            ]

    def _get_transitions(self, max_edges: int) -> list[NavigationTransition]:
        query = """
            MATCH (source:PageState)-[rel:NAVIGATES_TO]->(target:PageState)
            RETURN source.url AS source_url,
                   coalesce(source.title, '') AS source_title,
                   target.url AS target_url,
                   coalesce(target.title, '') AS target_title,
                   coalesce(rel.action, '') AS action,
                   coalesce(rel.interaction_kind, '') AS interaction_kind,
                   coalesce(rel.element_tag, '') AS element_tag,
                   coalesce(rel.element_text, '') AS element_text,
                   coalesce(rel.element_id, '') AS element_id,
                   coalesce(rel.element_name, '') AS element_name,
                   coalesce(rel.element_role, '') AS element_role,
                   coalesce(rel.element_aria_label, '') AS element_aria_label,
                   coalesce(rel.element_href, '') AS element_href,
                   coalesce(rel.input_type, '') AS input_type,
                   coalesce(rel.selectors_json, '{}') AS selectors_json,
                   coalesce(rel.selector_scores_json, '{}') AS selector_scores_json
            LIMIT $max_edges
        """
        with self._driver.session() as session:
            records = session.run(query, max_edges=max_edges)
            return [
                NavigationTransition(
                    source={"url": record["source_url"], "title": record["source_title"]},
                    target={"url": record["target_url"], "title": record["target_title"]},
                    action=record["action"],
                    interaction_kind=record["interaction_kind"],
                    element={
                        "tag": record["element_tag"],
                        "text": record["element_text"],
                        "id": record["element_id"],
                        "name": record["element_name"],
                        "role": record["element_role"],
                        "aria_label": record["element_aria_label"],
                        "href": record["element_href"],
                        "input_type": record["input_type"],
                    },
                    selectors=_decode_json_object(record["selectors_json"]),
                    selector_scores=_decode_json_object(record["selector_scores_json"]),
                )
                for record in records
            ]

    def health_check(self) -> bool:
        with self._driver.session() as session:
            return session.run("RETURN 1 AS ok").single()["ok"] == 1

    def _wait_until_ready(self) -> None:
        deadline = time.monotonic() + self._ready_timeout_seconds
        while True:
            try:
                if self.health_check():
                    return
            except Exception:
                pass
            if time.monotonic() >= deadline:
                raise RuntimeError("Neo4j nao ficou pronto dentro do tempo esperado.")
            time.sleep(2)


def _decode_json_object(value: str) -> dict[str, object]:
    try:
        decoded = json.loads(value or "{}")
    except json.JSONDecodeError:
        return {}
    return decoded if isinstance(decoded, dict) else {}
