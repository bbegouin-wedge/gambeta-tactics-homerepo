"""Lecture du modèle du système : composants, relations, manifestes.

Partagé par scripts/workspace, scripts/extract-contracts, scripts/checks/* et
ci/*. Ne dépend que de pyyaml.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "workspace"
CONTRACTS = ROOT / "contracts"
MANIFESTS = ROOT / "manifests"
CURRENT = MANIFESTS / "current.yaml"


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(data: Any, header: str = "") -> str:
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    return header + body


def components() -> dict[str, dict[str, Any]]:
    return load_yaml(ROOT / "system" / "components.yaml")["components"]


def relations() -> list[dict[str, Any]]:
    return load_yaml(ROOT / "system" / "relations.yaml")["relations"]


@dataclass(frozen=True)
class Pin:
    name: str
    sha: str | None
    spec: dict[str, Any]

    @property
    def local_path(self) -> Path | None:
        p = self.spec.get("local_path")
        return (ROOT / p).resolve() if p else None

    @property
    def mounted_in(self) -> dict[str, str] | None:
        return self.spec.get("mounted_in")

    def workspace_dir(self) -> Path:
        m = self.mounted_in
        if m:
            return WORKSPACE / m["component"] / m["path"]
        return WORKSPACE / self.name


def resolve_manifest(path: Path) -> dict[str, Pin]:
    """Les SHA d'un manifeste. Un candidat hérite de current.yaml ce qu'il ne fixe pas."""
    data = load_yaml(path)
    pins: dict[str, Any] = {}
    if data.get("manifest") == "candidate":
        pins.update(load_yaml(CURRENT)["components"])
    pins.update(data.get("components") or {})
    specs = components()
    return {
        name: Pin(name, (entry or {}).get("sha"), specs[name])
        for name, entry in pins.items()
        if name in specs
    }


def git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} : {r.stderr.strip()}")
    return r.stdout.strip()


def has_commit(repo: Path, sha: str) -> bool:
    r = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=repo, capture_output=True
    )
    return r.returncode == 0


class Report:
    """Accumule erreurs et avertissements, et rend le code de sortie."""

    def __init__(self, title: str) -> None:
        self.title = title
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def finish(self) -> int:
        print(f"== {self.title}")
        for w in self.warnings:
            print(f"  ⚠ {w}")
        for e in self.errors:
            print(f"  ✗ {e}")
        if not self.errors:
            print(f"  ✓ ok ({len(self.warnings)} avertissement(s))")
        return 1 if self.errors else 0


def main_guard(fn) -> None:  # type: ignore[no-untyped-def]
    try:
        sys.exit(fn())
    except RuntimeError as e:
        print(f"erreur : {e}", file=sys.stderr)
        sys.exit(2)
