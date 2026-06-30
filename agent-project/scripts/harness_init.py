from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXIT_CODE = 0


def ok(msg: str) -> None:
    print(f"[OK]   {msg}")


def fail(msg: str) -> None:
    global EXIT_CODE
    print(f"[FAIL] {msg}")
    EXIT_CODE = 1


def require_file(rel_path: str) -> None:
    path = ROOT / rel_path
    if path.is_file():
        ok(f"Existe {rel_path}")
    else:
        fail(f"Falta {rel_path}")


def validate_feature_list() -> None:
    path = ROOT / "feature_list.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"feature_list.json invalido: {exc}")
        return

    valid_status = set(data.get("rules", {}).get("valid_status", []))
    if not valid_status:
        valid_status = {"pending", "spec_ready", "in_progress", "done", "blocked"}

    features = data.get("features", [])
    in_progress_count = sum(1 for f in features if f.get("status") == "in_progress")
    if in_progress_count > 1:
        fail("Hay mas de una feature en in_progress")

    seen_names: set[str] = set()
    for feature in features:
        name = feature.get("name")
        status = feature.get("status")
        sdd = feature.get("sdd") is True

        if not name:
            fail("Feature sin name")
            continue

        if name in seen_names:
            fail(f"Feature duplicada: {name}")
        seen_names.add(name)

        if status not in valid_status:
            fail(f"Estado invalido en {name}: {status}")

        if sdd and status in {"spec_ready", "in_progress", "done"}:
            for spec_name in ("requirements.md", "design.md", "tasks.md"):
                rel = f"specs/{name}/{spec_name}"
                if (ROOT / rel).is_file():
                    ok(f"Spec presente: {rel}")
                else:
                    fail(f"Falta spec: {rel}")

    ok(f"feature_list.json valido ({len(features)} features)")


def main() -> int:
    print("== 1. Entorno ==")
    ok(f"Python {sys.version.split()[0]}")

    print("\n== 2. Archivos base ==")
    base_files = [
        "AGENTS.md",
        "feature_list.json",
        "CHECKPOINTS.md",
        "progress/current.md",
        "progress/history.md",
        "docs/sdd/specs.md",
        "docs/sdd/conventions.md",
        "docs/sdd/verification.md",
        ".github/agents/sdd-leader.agent.md",
        ".github/agents/sdd-spec-author.agent.md",
        ".github/agents/sdd-implementer.agent.md",
        ".github/agents/sdd-reviewer.agent.md",
    ]
    for rel in base_files:
        require_file(rel)

    print("\n== 3. Coherencia SDD ==")
    validate_feature_list()

    print("\n== 4. Resumen ==")
    if EXIT_CODE == 0:
        ok("Arnes SDD valido")
    else:
        fail("Arnes SDD invalido")

    return EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
