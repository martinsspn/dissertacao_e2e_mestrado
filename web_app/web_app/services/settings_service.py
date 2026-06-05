from __future__ import annotations

import json

from web_app.config import WebAppConfig


class SettingsService:
    def __init__(self, config: WebAppConfig) -> None:
        self._config = config
        self._path = config.data_dir / "settings.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def target_url(self) -> str:
        value = self._read().get("target_url")
        return str(value) if isinstance(value, str) and value.strip() else self._config.target_url

    def set_target_url(self, target_url: str) -> None:
        data = self._read()
        data["target_url"] = target_url.strip()
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _read(self) -> dict[str, object]:
        if not self._path.exists():
            return {}
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}
