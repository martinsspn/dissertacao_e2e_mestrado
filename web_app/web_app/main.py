from __future__ import annotations

from io import BytesIO
import inspect
from zipfile import ZipFile, ZIP_DEFLATED

import uvicorn
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web_app.config import WebAppConfig
from web_app.services.filesystem_service import FileSystemService
from web_app.services.graph_service import GraphService
from web_app.services.job_manager import JobManager
from web_app.services.pipeline_service import PipelineService
from web_app.services.settings_service import SettingsService


config = WebAppConfig()
jobs = JobManager(config)
files = FileSystemService(config)
graph = GraphService(config)
settings = SettingsService(config)
pipeline = PipelineService(config, jobs)

app = FastAPI(title="Gerador E2E Com Contexto Estruturado")
app.mount("/static", StaticFiles(directory=str(config.repo_root / "web_app" / "web_app" / "static")), name="static")
templates = Jinja2Templates(directory=str(config.repo_root / "web_app" / "web_app" / "templates"))


def _template_uses_request_first() -> bool:
    try:
        params = list(inspect.signature(templates.TemplateResponse).parameters)
    except (TypeError, ValueError):
        return False
    return bool(params) and params[0] == "request"


_TEMPLATE_USES_REQUEST_FIRST = _template_uses_request_first()


def _render_template(name: str, request: Request, context: dict[str, object]) -> HTMLResponse:
    if "request" not in context:
        context = {**context, "request": request}
    if _TEMPLATE_USES_REQUEST_FIRST:
        return templates.TemplateResponse(request, name, context)
    return templates.TemplateResponse(name, context)


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    graph_summary = graph.summary()
    return _render_template(
        "dashboard.html",
        request,
        {
            "active": "dashboard",
            "config": config,
            "graph_summary": graph_summary,
            "specs": files.list_specs(),
            "prompts": files.list_prompts(),
            "structured_tests": files.list_tests("structured_context"),
            "baseline_tests": files.list_tests("baseline"),
            "reports": files.list_reports(),
            "latest_jobs": {
                "crawl": jobs.latest("crawl"),
                "prompts": jobs.latest("prompts"),
                "evaluation": jobs.latest("evaluation"),
            },
        },
    )


@app.get("/crawler", response_class=HTMLResponse)
def crawler_page(request: Request):
    return _render_template(
        "crawler.html",
        request,
        {
            "active": "crawler",
            "config": config,
            "target_url": settings.target_url(),
            "graph_summary": graph.summary(),
            "manifest": files.read_crawl_manifest(),
            "latest_crawl": jobs.latest("crawl"),
        },
    )


@app.post("/crawler/run")
def run_crawler(
    target_url: str = Form(...),
    max_depth: int = Form(...),
    max_states: int = Form(...),
    max_runtime_minutes: int = Form(...),
    wait_after_reload_ms: int = Form(...),
    wait_after_event_ms: int = Form(...),
    click_once: str | None = Form(None),
    random_order: str | None = Form(None),
):
    settings.set_target_url(target_url)
    pipeline.run_crawler(
        target_url=target_url,
        max_depth=max_depth,
        max_states=max_states,
        max_runtime_minutes=max_runtime_minutes,
        wait_after_reload_ms=wait_after_reload_ms,
        wait_after_event_ms=wait_after_event_ms,
        click_once=click_once == "on",
        random_order=random_order == "on",
    )
    return RedirectResponse("/crawler", status_code=303)


@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_page(request: Request, job_id: str):
    return _render_template(
        "job.html",
        request,
        {
            "active": "",
            "job": jobs.get(job_id),
            "log": jobs.read_log(job_id),
        },
    )


@app.get("/graph", response_class=HTMLResponse)
def graph_page(request: Request):
    return _render_template(
        "graph.html",
        request,
        {
            "active": "graph",
            "summary": graph.summary(),
            "graph_data": graph.visualization(),
        },
    )


@app.get("/specs", response_class=HTMLResponse)
def specs_page(request: Request, spec_id: str | None = None):
    spec_paths = files.list_specs()
    selected = spec_id or (spec_paths[0].stem if spec_paths else "")
    content = files.read_spec(selected) if selected else ""
    return _render_template(
        "specs.html",
        request,
        {
            "active": "specs",
            "specs": spec_paths,
            "selected": selected,
            "content": content,
        },
    )


@app.post("/specs/save")
def save_spec(spec_id: str = Form(...), content: str = Form(...)):
    files.write_spec(spec_id, content)
    return RedirectResponse(f"/specs?spec_id={spec_id}", status_code=303)


@app.post("/specs/upload")
async def upload_specs(uploaded_specs: list[UploadFile] = File(default=[])):
    for uploaded_spec in uploaded_specs:
        if not uploaded_spec.filename:
            continue
        files.write_uploaded_spec(uploaded_spec.filename, await uploaded_spec.read())
    return RedirectResponse("/specs", status_code=303)


@app.post("/specs/delete")
def delete_specs(spec_ids: list[str] = Form(default=[])):
    files.delete_specs(spec_ids)
    return RedirectResponse("/specs", status_code=303)


@app.get("/prompts", response_class=HTMLResponse)
def prompts_page(request: Request, prompt_id: str | None = None):
    prompt_paths = files.list_prompts()
    selected = prompt_id or (prompt_paths[0].name.removesuffix(".prompt.md") if prompt_paths else "")
    content = files.read_prompt(selected) if selected else ""
    return _render_template(
        "prompts.html",
        request,
        {
            "active": "prompts",
            "config": config,
            "target_url": settings.target_url(),
            "prompts": prompt_paths,
            "selected": selected,
            "content": content,
            "latest_job": jobs.latest("prompts"),
        },
    )


@app.post("/prompts/generate")
def generate_prompts():
    pipeline.generate_prompts(settings.target_url())
    return RedirectResponse("/prompts", status_code=303)


@app.post("/prompts/download")
def download_prompts(prompt_ids: list[str] = Form(default=[]), download_scope: str = Form("selected")):
    prompt_paths = files.prompt_paths(None if download_scope == "all" else prompt_ids)
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for prompt_path in prompt_paths:
            archive.write(prompt_path, arcname=prompt_path.name)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="prompts_gerados.zip"'},
    )


@app.post("/prompts/delete")
def delete_prompts(prompt_ids: list[str] = Form(default=[])):
    files.delete_prompts(prompt_ids)
    return RedirectResponse("/prompts", status_code=303)


@app.get("/tests", response_class=HTMLResponse)
def tests_page(request: Request, approach: str = "structured_context", spec_id: str | None = None):
    test_paths = files.list_tests(approach)
    selected = spec_id or (test_paths[0].name.removesuffix(".spec.ts") if test_paths else "")
    code = files.read_test(approach, selected) if selected else ""
    return _render_template(
        "tests.html",
        request,
        {
            "active": "tests",
            "approach": approach,
            "tests": test_paths,
            "selected": selected,
            "code": code,
        },
    )


@app.post("/tests/save")
def save_test(approach: str = Form(...), spec_id: str = Form(...), code: str = Form(...)):
    files.write_test(approach, spec_id, code)
    return RedirectResponse(f"/tests?approach={approach}&spec_id={spec_id}", status_code=303)


@app.get("/evaluation", response_class=HTMLResponse)
def evaluation_page(request: Request, report_id: str | None = None):
    report_paths = files.list_reports()
    selected = report_id or (report_paths[0].stem if report_paths else "")
    content = files.read_report(selected) if selected else ""
    return _render_template(
        "evaluation.html",
        request,
        {
            "active": "evaluation",
            "reports": report_paths,
            "selected": selected,
            "content": content,
            "latest_job": jobs.latest("evaluation"),
        },
    )


@app.post("/evaluation/run")
def run_evaluation(approach: str = Form(...), use_graph: str | None = Form(None)):
    pipeline.evaluate_tests(approach, use_graph == "on", settings.target_url())
    return RedirectResponse("/evaluation", status_code=303)


def main() -> None:
    uvicorn.run("web_app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
