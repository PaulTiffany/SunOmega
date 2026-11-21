"""Validated Git records -> deterministic MeTTa facts for an in-process AtomSpace."""
from __future__ import annotations

import json
import re
from pathlib import Path

KINDS = {"source", "capability", "technique", "experiment", "preference"}
STATUSES = {"primary-documentation", "documented", "hypothesis", "tested", "contradicted", "deprecated"}
PREDICATES = {"supports", "contradicts", "refines", "depends-on", "enables", "addresses"}
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_records(directory: Path) -> list[dict]:
    if not directory.is_dir():
        raise ValueError(f"Missing knowledge directory: {directory}")
    records = []
    for path in sorted(directory.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"{path}: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path}: expected JSON object")
        records.append(record)
    if not records:
        raise ValueError("Knowledge directory has no records")
    validate_records(records)
    return records


def validate_records(records: list[dict]) -> None:
    seen = {}
    for record in records:
        rid = record.get("id")
        if not isinstance(rid, str) or not ID.fullmatch(rid):
            raise ValueError(f"Invalid id: {rid!r}")
        if rid in seen:
            raise ValueError(f"Duplicate record id: {rid}")
        seen[rid] = record
        if record.get("kind") not in KINDS or record.get("status") not in STATUSES:
            raise ValueError(f"{rid}: invalid kind/status")
        if any(not isinstance(record.get(f), str) or not record[f].strip() for f in ("title", "summary")):
            raise ValueError(f"{rid}: title and summary required")
        for field in ("topics", "sources", "relations"):
            if not isinstance(record.get(field), list):
                raise ValueError(f"{rid}: {field} must be an array")
        if not record["topics"] or any(not isinstance(t, str) or not t for t in record["topics"]):
            raise ValueError(f"{rid}: invalid topics")
        if any(not isinstance(x, str) for x in record["sources"]):
            raise ValueError(f"{rid}: invalid source IDs")
        if record["kind"] == "source":
            if not isinstance(record.get("url"), str) or not record["url"].startswith("https://"):
                raise ValueError(f"{rid}: source requires HTTPS URL")
            if not isinstance(record.get("accessed"), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["accessed"]):
                raise ValueError(f"{rid}: source requires accessed YYYY-MM-DD")
            if record["sources"]:
                raise ValueError(f"{rid}: source cannot cite other sources")
        elif not record["sources"]:
            raise ValueError(f"{rid}: non-source record must cite sources")
        for relation in record["relations"]:
            if not isinstance(relation, dict) or relation.get("predicate") not in PREDICATES or not isinstance(relation.get("target"), str):
                raise ValueError(f"{rid}: invalid relation")

    for rid, record in seen.items():
        for source in record["sources"]:
            if source not in seen or seen[source]["kind"] != "source":
                raise ValueError(f"{rid}: missing source {source}")
        for relation in record["relations"]:
            if relation["target"] not in seen:
                raise ValueError(f"{rid}: missing relation target {relation['target']}")


def to_metta(records: list[dict]) -> str:
    """No independent MeTTa edits: regenerate atoms from canonical JSON."""
    def q(value: str) -> str:
        return json.dumps(value, ensure_ascii=False)
    lines = ["; SunOmega generated MeTTa data; edit JSON sources instead."]
    for r in sorted(records, key=lambda x: x["id"]):
        rid = q(r["id"])
        for pred, value in (("Record", r["kind"]), ("Title", r["title"]),
                            ("Summary", r["summary"]), ("Status", r["status"])):
            lines.append(f"({pred} {rid} {q(value)})")
        for topic in sorted(set(r["topics"])):
            lines.append(f"(Topic {rid} {q(topic)})")
        for source in sorted(set(r["sources"])):
            lines.append(f"(Cites {rid} {q(source)})")
        if r["kind"] == "source":
            lines.append(f"(URL {rid} {q(r['url'])})")
            lines.append(f"(Accessed {rid} {q(r['accessed'])})")
        for edge in r["relations"]:
            lines.append(f"(Relation {rid} {q(edge['predicate'])} {q(edge['target'])})")
    return "\n".join(lines) + "\n"


def smoke_metta(records: list[dict]) -> list:
    """Execute a real Hyperon AtomSpace query, when optional hyperon is present."""
    try:
        from hyperon import MeTTa
    except ImportError as exc:
        raise RuntimeError("Install the atomspace extra: pip install -e '.[atomspace]'") from exc
    metta = MeTTa()
    metta.run(to_metta(records))
    answer = metta.run('!(match &self (Record $id "capability") $id)')
    if "capability-official-mcp" not in str(answer):
        raise RuntimeError(f"MeTTa query did not find a known capability: {answer}")
    return answer
