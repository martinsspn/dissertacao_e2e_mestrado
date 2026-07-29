from __future__ import annotations

import json
import time

try:
    from neo4j import GraphDatabase
except ModuleNotFoundError:  # pragma: no cover - external dependency
    GraphDatabase = None

from teste_prompt_e2e_semantico.config import PromptGeneratorConfig
from teste_prompt_e2e_semantico.domain.models import (
    NavigationGraph,
    NavigationTransition,
    ObservedResult,
    PageNode,
    UiElement,
)


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

    def get_navigation_graph(self) -> NavigationGraph:
        self._wait_until_ready()
        return NavigationGraph(
            pages=self._get_page_catalog(),
            transitions=self._get_transitions(),
            ui_elements=self._get_ui_elements(),
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

    def _get_transitions(self) -> list[NavigationTransition]:
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
                   coalesce(rel.observed_text, '') AS observed_text,
                   coalesce(rel.observed_element_id, '') AS observed_element_id,
                   coalesce(rel.observed_element_role, '') AS observed_element_role
            ORDER BY source.url, target.url, element_text, element_id
        """
        with self._driver.session() as session:
            records = session.run(query)
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
                    observed_result=(
                        ObservedResult(
                            text=record["observed_text"],
                            element_id=record["observed_element_id"],
                            role=record["observed_element_role"],
                        )
                        if record["observed_text"]
                        else None
                    ),
                )
                for record in records
            ]

    def _get_ui_elements(self) -> list[UiElement]:
        query = """
            MATCH (page:PageState)-[:HAS_ELEMENT]->(element:UiElement)
            RETURN page.url AS page_url,
                   coalesce(element.kind, '') AS kind,
                   coalesce(element.suggested_operation, '') AS suggested_operation,
                   coalesce(element.tag, '') AS tag,
                   coalesce(element.text, '') AS text,
                   coalesce(element.title, '') AS title,
                   coalesce(element.label, '') AS label,
                   coalesce(element.data_testid, '') AS data_testid,
                   coalesce(element.id_attribute, '') AS id_attribute,
                   coalesce(element.name, '') AS name,
                   coalesce(element.input_type, '') AS input_type,
                   coalesce(element.value, '') AS value,
                   coalesce(element.href, '') AS href,
                   coalesce(element.role, '') AS role,
                   coalesce(element.aria_label, '') AS aria_label,
                   coalesce(element.placeholder, '') AS placeholder,
                   coalesce(element.form_action, '') AS form_action,
                   coalesce(element.form_method, '') AS form_method
            ORDER BY page.url, element.id
        """
        with self._driver.session() as session:
            records = session.run(query)
            elements = []
            for record in records:
                element = {
                    "tag": record["tag"],
                    "text": record["text"],
                    "title": record["title"],
                    "label": record["label"],
                    "data_testid": record["data_testid"],
                    "id": record["id_attribute"],
                    "name": record["name"],
                    "input_type": record["input_type"],
                    "value": record["value"],
                    "href": record["href"],
                    "role": record["role"],
                    "aria_label": record["aria_label"],
                    "placeholder": record["placeholder"],
                    "form_action": record["form_action"],
                    "form_method": record["form_method"],
                }
                elements.append(
                    UiElement(
                        page_url=record["page_url"],
                        kind=record["kind"],
                        suggested_operation=record["suggested_operation"],
                        element=element,
                        selectors=_selectors_from_element(element),
                    )
                )
            return elements

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


def _selectors_from_element(element: dict[str, str]) -> dict[str, object]:
    selectors = {}
    for key in ("data_testid", "aria_label", "label", "id", "name", "placeholder", "text", "href", "role"):
        value = element.get(key, "").strip()
        if value:
            selectors[key] = value
    return selectors
