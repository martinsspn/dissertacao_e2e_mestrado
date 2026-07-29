from __future__ import annotations

import time

try:
    from neo4j import GraphDatabase
except ModuleNotFoundError:  # pragma: no cover - dependência externa opcional em testes
    GraphDatabase = None

from avaliacao_prompts.domain.models import GraphEvidence


class Neo4jGraphEvidenceReader:
    def __init__(
        self,
        uri: str,
        user: str,
        password: str,
        ready_timeout_seconds: int = 60,
    ) -> None:
        if GraphDatabase is None:
            raise ModuleNotFoundError(
                "A dependência 'neo4j' não está instalada. Execute "
                "'pip install -r requirements.txt'."
            )
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._ready_timeout_seconds = ready_timeout_seconds

    def close(self) -> None:
        self._driver.close()

    def read(self) -> GraphEvidence:
        self._wait_until_ready()
        with self._driver.session() as session:
            pages = list(
                session.run(
                    """
                    MATCH (page:PageState)
                    RETURN coalesce(page.url, '') AS url,
                           coalesce(page.title, '') AS title,
                           coalesce(page.h1, '') AS h1,
                           coalesce(page.visible_text_excerpt, '') AS visible_text
                    """
                )
            )
            transitions = list(
                session.run(
                    """
                    MATCH (source:PageState)-[rel:NAVIGATES_TO]->(target:PageState)
                    RETURN coalesce(source.url, '') AS source_url,
                           coalesce(target.url, '') AS target_url,
                           coalesce(rel.element_text, '') AS element_text,
                           coalesce(rel.element_id, '') AS element_id,
                           coalesce(rel.element_name, '') AS element_name,
                           coalesce(rel.element_role, '') AS element_role,
                           coalesce(rel.element_aria_label, '') AS aria_label,
                           coalesce(rel.element_href, '') AS href,
                           coalesce(rel.selectors_json, '') AS selectors,
                           coalesce(rel.observed_text, '') AS observed_text
                    """
                )
            )
            elements = list(
                session.run(
                    """
                    MATCH (page:PageState)-[:HAS_ELEMENT]->(element:UiElement)
                    RETURN coalesce(page.url, '') AS page_url,
                           coalesce(element.text, '') AS text,
                           coalesce(element.title, '') AS title,
                           coalesce(element.label, '') AS label,
                           coalesce(element.data_testid, '') AS data_testid,
                           coalesce(element.id_attribute, '') AS id_attribute,
                           coalesce(element.name, '') AS name,
                           coalesce(element.value, '') AS value,
                           coalesce(element.href, '') AS href,
                           coalesce(element.role, '') AS role,
                           coalesce(element.aria_label, '') AS aria_label,
                           coalesce(element.placeholder, '') AS placeholder
                    """
                )
            )

        urls = _unique(
            [record["url"] for record in pages]
            + [value for record in transitions for value in (record["source_url"], record["target_url"])]
        )
        texts = _unique(
            [value for record in pages for value in (record["title"], record["h1"], record["visible_text"])]
            + [
                value
                for record in transitions
                for value in (
                    record["element_text"],
                    record["element_id"],
                    record["element_name"],
                    record["element_role"],
                    record["aria_label"],
                    record["href"],
                    record["selectors"],
                    record["observed_text"],
                )
            ]
            + [value for record in elements for value in record.values()]
        )
        return GraphEvidence(urls=urls, texts=texts)

    def _wait_until_ready(self) -> None:
        deadline = time.monotonic() + self._ready_timeout_seconds
        while True:
            try:
                with self._driver.session() as session:
                    if session.run("RETURN 1 AS ok").single()["ok"] == 1:
                        return
            except Exception:
                pass
            if time.monotonic() >= deadline:
                raise RuntimeError("Neo4j não ficou pronto dentro do tempo esperado.")
            time.sleep(2)


def _unique(values: list[object]) -> list[str]:
    return list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))
