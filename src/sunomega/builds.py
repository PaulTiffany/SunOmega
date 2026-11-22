"""GF-inspired, inspectable production-build contracts embedded in knowledge records.

Contracts describe an agent's capability and boundaries. They are NOT authority
to execute tools. JSON stays canonical; AtomSpace facts are only a projection.
"""
from __future__ import annotations
import json
import re

EFFECTS = {"local-read", "local-write", "network-read", "network-write", "account-write", "spend"}
PROOF_STATES = {"proposed", "provider-documented", "locally-tested", "provider-tested", "listener-observed"}
BUILD_FIELDS = {"target", "requires", "inputs", "outputs", "execute", "matchup", "effects",
                "bounds", "stop_when", "proof"}
MATCHUP_FIELDS = {"applies_when", "avoid_when"}
BOUNDS_FIELDS = {"enforced", "operator"}
PROOF_FIELDS = {"status", "checks", "evidence"}
PATH_RE = re.compile(r"^(?:skills|docs|research)/[a-zA-Z0-9_./-]+$")


def _strings(items: object, field: str, *, required: bool = True) -> None:
    if not isinstance(items, list) or (required and not items) or len(items) > 32:
        raise ValueError(f"{field}: expected bounded {'nonempty ' if required else ''}list")
    if any(not isinstance(i, str) or not 1 <= len(i.strip()) <= 500 for i in items):
        raise ValueError(f"{field}: expected short nonempty strings")


def validate_build(build: object, record_id: str) -> None:
    """Validate one GF-style production contract without executing anything."""
    label = f"{record_id} build"
    if not isinstance(build, dict) or set(build) != BUILD_FIELDS:
        raise ValueError(f"{label}: missing or unexpected build fields")
    if not isinstance(build["target"], str) or not 1 <= len(build["target"].strip()) <= 500:
        raise ValueError(f"{label}: requires an observable target")
    for field in ("requires", "inputs", "outputs", "execute", "stop_when"):
        _strings(build[field], f"{label}.{field}")
    matchup = build["matchup"]
    if not isinstance(matchup, dict) or set(matchup) != MATCHUP_FIELDS:
        raise ValueError(f"{label}: matchup must declare applies_when and avoid_when")
    _strings(matchup["applies_when"], f"{label}.matchup.applies_when")
    _strings(matchup["avoid_when"], f"{label}.matchup.avoid_when", required=False)
    _strings(build["effects"], f"{label}.effects")
    if len(set(build["effects"])) != len(build["effects"]) or any(e not in EFFECTS for e in build["effects"]):
        raise ValueError(f"{label}: invalid or duplicate effects")
    bounds = build["bounds"]
    if not isinstance(bounds, dict) or set(bounds) != BOUNDS_FIELDS:
        raise ValueError(f"{label}: bounds must declare enforced and operator")
    _strings(bounds["enforced"], f"{label}.bounds.enforced", required=False)
    _strings(bounds["operator"], f"{label}.bounds.operator")
    proof = build["proof"]
    if not isinstance(proof, dict) or set(proof) != PROOF_FIELDS or proof.get("status") not in PROOF_STATES:
        raise ValueError(f"{label}: invalid proof declaration")
    _strings(proof["checks"], f"{label}.proof.checks")
    _strings(proof["evidence"], f"{label}.proof.evidence", required=False)
    for pointer in proof["evidence"]:
        if not (pointer.startswith("https://") or (PATH_RE.fullmatch(pointer) and ".." not in pointer.split("/"))):
            raise ValueError(f"{label}: proof evidence must be a safe local path or HTTPS URL")
    if proof["status"] in {"locally-tested", "provider-tested", "listener-observed"} and not proof["evidence"]:
        raise ValueError(f"{label}: tested proof must name evidence")


def build_metta(record: dict) -> list[str]:
    """Generate searchable symbolic metadata; no tool evaluation is embedded."""
    build = record.get("build")
    if build is None:
        return []
    def q(value: str) -> str:
        return json.dumps(value, ensure_ascii=False)
    rid = q(record["id"])
    facts = [f"(BuildTarget {rid} {q(build['target'])})",
             f"(BuildProofStatus {rid} {q(build['proof']['status'])})"]
    for key, predicate in (("requires", "BuildRequires"), ("inputs", "BuildInput"),
                           ("outputs", "BuildOutput"), ("effects", "BuildEffect"),
                           ("stop_when", "BuildStopWhen")):
        for value in build[key]:
            facts.append(f"({predicate} {rid} {q(value)})")
    for idx, step in enumerate(build["execute"], 1):
        facts.append(f"(BuildStep {rid} {idx} {q(step)})")
    for key, predicate in (("applies_when", "BuildAppliesWhen"), ("avoid_when", "BuildAvoidWhen")):
        for value in build["matchup"][key]:
            facts.append(f"({predicate} {rid} {q(value)})")
    for key, predicate in (("enforced", "BuildEnforcedBound"), ("operator", "BuildOperatorBound")):
        for value in build["bounds"][key]:
            facts.append(f"({predicate} {rid} {q(value)})")
    for key, predicate in (("checks", "BuildProofCheck"), ("evidence", "BuildEvidence")):
        for value in build["proof"][key]:
            facts.append(f"({predicate} {rid} {q(value)})")
    return facts


def validate_package_links(records: list[dict], records_dir: object) -> None:
    """Check a GF skill's declaration and package-local files without invoking it."""
    from pathlib import Path
    root = Path(records_dir).resolve().parent.parent
    for record in records:
        if "build_path" not in record:
            continue
        rid = record["id"]
        manifest_path = root / record["build_path"]
        if not manifest_path.is_file():
            raise ValueError(f"{rid}: missing build manifest {record['build_path']}")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"{rid}: invalid GF build manifest") from exc
        if not isinstance(manifest, dict) or manifest.get("id") != manifest_path.parent.name:
            raise ValueError(f"{rid}: GF manifest id must match package directory")
        for field in ("skill", "entrypoint", "license"):
            path = manifest.get(field)
            if not isinstance(path, str) or not path or path.startswith("/") or ".." in path.split("/"):
                raise ValueError(f"{rid}: unsafe GF {field} path")
            if not (manifest_path.parent / path).is_file():
                raise ValueError(f"{rid}: missing GF package file {field}: {path}")
        references = manifest.get("evidence")
        if not isinstance(references, list) or not references:
            raise ValueError(f"{rid}: GF manifest has no evidence files")
        for path in references:
            if not isinstance(path, str) or path.startswith("/") or ".." in path.split("/"):
                raise ValueError(f"{rid}: unsafe GF evidence path")
            if not (manifest_path.parent / path).is_file():
                raise ValueError(f"{rid}: missing GF evidence file: {path}")


def searchable_text(record: dict) -> str:
    """A simple retrieval baseline including procedural fields; not semantic search."""
    parts = [record["id"], record["title"], record["summary"], *record["topics"]]
    if "build" in record:
        b = record["build"]
        parts.extend([b["target"], *b["requires"], *b["inputs"], *b["outputs"],
                      *b["execute"], *b["matchup"]["applies_when"], *b["matchup"]["avoid_when"],
                      *b["proof"]["checks"]])
    return " ".join(parts).casefold()
