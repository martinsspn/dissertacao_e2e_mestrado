#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = root / "archive_manifest.csv"
    checked = 0
    with manifest.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            path = root / row["archive_path"]
            if not path.is_file():
                raise SystemExit(f"arquivo ausente: {path}")
            if path.stat().st_size != int(row["bytes"]):
                raise SystemExit(f"tamanho divergente: {path}")
            if sha256(path) != row["sha256"]:
                raise SystemExit(f"hash divergente: {path}")
            checked += 1
    print(f"manifesto válido: {checked} arquivos")


if __name__ == "__main__":
    main()
