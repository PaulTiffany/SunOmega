"""Read-only CLI for the Git-backed SunOmega knowledge graph."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .knowledge import load_records, smoke_metta, to_metta


def main() -> None:
    parser = argparse.ArgumentParser(prog="sunomega")
    parser.add_argument("--records", type=Path, default=Path.cwd() / "knowledge" / "records")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    search = commands.add_parser("search")
    search.add_argument("query")
    commands.add_parser("export-metta")
    commands.add_parser("smoke-metta")
    args = parser.parse_args()
    try:
        records = load_records(args.records)
        if args.command == "validate":
            print(f"Validated {len(records)} knowledge records.")
        elif args.command == "search":
            term = args.query.casefold()
            found = [r for r in records if term in " ".join(
                [r["id"], r["title"], r["summary"], *r["topics"]]).casefold()]
            print(json.dumps(found, ensure_ascii=False, indent=2))
        elif args.command == "export-metta":
            sys.stdout.write(to_metta(records))
        elif args.command == "smoke-metta":
            print(f"AtomSpace query returned: {smoke_metta(records)}")
    except (RuntimeError, ValueError) as exc:
        parser.exit(1, f"SunOmega: {exc}\n")


if __name__ == "__main__":
    main()
