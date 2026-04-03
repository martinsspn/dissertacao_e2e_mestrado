import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def safe_filename(value: str) -> str:
    return "".join(char if char.isalnum() or char in "-_" else "_" for char in value)


def page_context(page) -> Dict[str, str]:
    title = ""
    text = ""
    html = ""
    try:
        title = page.title()
    except Exception:
        title = ""
    try:
        text = page.evaluate("document.body ? document.body.innerText : ''")
    except Exception:
        text = ""
    try:
        html = page.content()
    except Exception:
        html = ""
    return {
        "url": page.url,
        "title": title,
        "visible_text": text[:8000],
        "html_excerpt": html[:20000],
    }


def capture_edge_package(
    edge: Dict[str, str],
    nodes_by_id: Dict[str, Dict[str, str]],
    page,
    screenshots_dir: Path,
) -> Dict[str, Any]:
    origem = edge.get("origem", "")
    destino = edge.get("destino", "")
    action = (edge.get("acao", "") or "").lower()
    selector_type = edge.get("selector_tipo", "") or ""
    selector_value = edge.get("selector_valor", edge.get("xpath_do_elemento", "")) or ""

    origem_node = nodes_by_id.get(origem, {})
    destino_node = nodes_by_id.get(destino, {})
    origem_url = origem_node.get("url_canonica", "")

    edge_id = f"{origem}__{action}__{destino}"
    edge_file = safe_filename(edge_id)

    screenshots_dir.mkdir(parents=True, exist_ok=True)
    before_path = screenshots_dir / f"{edge_file}__before.png"
    after_path = screenshots_dir / f"{edge_file}__after.png"
    element_path = screenshots_dir / f"{edge_file}__element.png"

    package: Dict[str, Any] = {
        "edge_id": edge_id,
        "edge": edge,
        "origin_node": origem_node,
        "destination_node": destino_node,
        "collector_status": "ok",
        "collector_errors": [],
    }

    if not origem_url:
        package["collector_status"] = "error"
        package["collector_errors"].append("origem_sem_url")
        return package

    try:
        page.goto(origem_url, wait_until="domcontentloaded", timeout=45000)
    except PlaywrightTimeoutError:
        package["collector_errors"].append("timeout_navegacao_origem")
    except Exception as exc:
        package["collector_status"] = "error"
        package["collector_errors"].append(f"erro_navegacao_origem:{exc}")
        return package

    page.screenshot(path=str(before_path), full_page=True)
    package["origin_context"] = page_context(page)
    package["origin_screenshot"] = str(before_path)

    if action == "click" and selector_type == "xpath" and selector_value:
        locator = page.locator(f"xpath={selector_value}")
        try:
            if locator.count() > 0:
                locator.first.screenshot(path=str(element_path))
                package["element_screenshot"] = str(element_path)

                element_metadata = locator.first.evaluate(
                    """
                    (el) => ({
                      tag: el.tagName,
                      text: (el.innerText || el.textContent || '').trim().slice(0, 500),
                      id: el.id || '',
                      name: el.getAttribute('name') || '',
                      type: el.getAttribute('type') || '',
                      href: el.getAttribute('href') || '',
                      ariaLabel: el.getAttribute('aria-label') || '',
                      title: el.getAttribute('title') || ''
                    })
                    """
                )
                package["element_metadata"] = element_metadata

                locator.first.click(timeout=12000)
            else:
                package["collector_errors"].append("elemento_xpath_nao_encontrado")
        except PlaywrightTimeoutError:
            package["collector_errors"].append("timeout_click")
        except Exception as exc:
            package["collector_errors"].append(f"erro_click:{exc}")

    elif action == "reload" and selector_type == "url" and selector_value:
        try:
            page.goto(selector_value, wait_until="domcontentloaded", timeout=45000)
        except PlaywrightTimeoutError:
            package["collector_errors"].append("timeout_reload_url")
        except Exception as exc:
            package["collector_errors"].append(f"erro_reload:{exc}")
    else:
        package["collector_errors"].append("acao_nao_mapeada_no_collector")

    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass

    page.screenshot(path=str(after_path), full_page=True)
    package["destination_context"] = page_context(page)
    package["destination_screenshot"] = str(after_path)

    if package["collector_errors"]:
        package["collector_status"] = "partial"

    return package


def main() -> None:
    parser = argparse.ArgumentParser(description="Coletor multimodal por aresta usando Playwright")
    parser.add_argument("--input-dir", default="/app/data_input")
    parser.add_argument("--output-dir", default="/app/data_input/multimodal_dataset")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    screenshots_dir = output_dir / "screenshots"

    nodes = load_json(input_dir / "nos.json")
    edges = load_json(input_dir / "arestas.json")
    nodes_by_id = {node.get("id", ""): node for node in nodes}

    packages: List[Dict[str, Any]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        for edge in edges:
            package = capture_edge_package(edge, nodes_by_id, page, screenshots_dir)
            packages.append(package)

        browser.close()

    save_json(output_dir / "multimodal_packages.json", packages)
    save_json(
        output_dir / "multimodal_packages_summary.json",
        {
            "total_edges": len(edges),
            "packages_generated": len(packages),
            "status_distribution": {
                "ok": sum(1 for package in packages if package["collector_status"] == "ok"),
                "partial": sum(1 for package in packages if package["collector_status"] == "partial"),
                "error": sum(1 for package in packages if package["collector_status"] == "error"),
            },
        },
    )

    print("Coleta multimodal concluída.")
    print(f"Output: {output_dir / 'multimodal_packages.json'}")


if __name__ == "__main__":
    main()