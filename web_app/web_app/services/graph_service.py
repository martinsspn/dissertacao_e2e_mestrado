from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from web_app.config import WebAppConfig

try:
    from neo4j import GraphDatabase
except ModuleNotFoundError:  # pragma: no cover
    GraphDatabase = None


@dataclass(frozen=True)
class GraphSummary:
    pages: int
    transitions: int
    error: str = ""


class GraphService:
    def __init__(self, config: WebAppConfig) -> None:
        self._config = config

    def summary(self) -> GraphSummary:
        if GraphDatabase is None:
            return GraphSummary(0, 0, "Dependencia neo4j nao instalada.")
        availability_error = self._availability_error()
        if availability_error:
            return GraphSummary(0, 0, availability_error)
        try:
            with self._driver() as driver:
                with driver.session() as session:
                    pages = session.run("MATCH (n:PageState) RETURN count(n) AS total").single()["total"]
                    transitions = session.run("MATCH ()-[r:NAVIGATES_TO]->() RETURN count(r) AS total").single()["total"]
                    return GraphSummary(int(pages), int(transitions))
        except Exception as exc:
            return GraphSummary(0, 0, str(exc))

    def visualization(self) -> dict[str, list[dict[str, Any]]]:
        if GraphDatabase is None:
            return {"nodes": [], "edges": []}
        if self._availability_error():
            return {"nodes": [], "edges": []}
        try:
            with self._driver() as driver:
                with driver.session() as session:
                    nodes = [
                        {
                            "id": record["id"],
                            "label": _page_label(record["title"], record["url"]),
                            "url": record["url"],
                            "title": record["title"],
                            "state_count": record["state_count"],
                            "h1": record["h1"],
                            "interactive_count": record["interactive_count"],
                        }
                        for record in session.run(
                            """
                            MATCH (n:PageState)
                            RETURN n.id AS id,
                                   n.url AS url,
                                   coalesce(n.title, '') AS title,
                                   coalesce(n.state_count, 1) AS state_count,
                                   coalesce(n.h1, '') AS h1,
                                   coalesce(n.interactive_count, 0) AS interactive_count
                            ORDER BY state_count DESC, url
                            """
                        )
                    ]
                    edges = [
                        {
                            "id": f"{record['source']}__{record['target']}__{index}",
                            "source": record["source"],
                            "target": record["target"],
                            "label": _edge_label(record["action"], record["text"]),
                            "action": record["action"],
                            "text": record["text"],
                            "selectors": _decode_json(record["selectors_json"]),
                        }
                        for index, record in enumerate(
                            session.run(
                                """
                                MATCH (source:PageState)-[rel:NAVIGATES_TO]->(target:PageState)
                                RETURN source.id AS source,
                                       target.id AS target,
                                       coalesce(rel.action, '') AS action,
                                       coalesce(rel.element_text, '') AS text,
                                       coalesce(rel.selectors_json, '{}') AS selectors_json
                                LIMIT 300
                                """
                            )
                        )
                    ]
                    return {"nodes": nodes, "edges": edges}
        except Exception:
            return {"nodes": [], "edges": []}

    def _driver(self):
        return GraphDatabase.driver(
            self._config.neo4j_uri,
            auth=(self._config.neo4j_user, self._config.neo4j_password),
            connection_timeout=2,
            connection_acquisition_timeout=2,
        )

    def _availability_error(self) -> str:
        parsed = urlparse(self._config.neo4j_uri)
        host = parsed.hostname or "localhost"
        port = parsed.port or 7687
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return ""
        except OSError as exc:
            return f"Neo4j indisponivel em {host}:{port}: {exc}"


def _page_label(title: str, url: str) -> str:
    if title:
        return title.replace("Demo Web Shop. ", "").strip()
    return url.rstrip("/").rsplit("/", 1)[-1] or "home"


def _edge_label(action: str, text: str) -> str:
    text = " ".join((text or "").split())
    if text:
        return f"{action} {text[:32]}"
    return action or "navega"


def _decode_json(value: str) -> dict[str, object]:
    try:
        decoded = json.loads(value or "{}")
    except json.JSONDecodeError:
        return {}
    return decoded if isinstance(decoded, dict) else {}
