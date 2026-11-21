# SunOmega knowledge corpus

Each JSON file in records/ is one canonical, Git-versioned knowledge record. Run `sunomega validate` before contributing, and `sunomega search "keyword"` to retrieve machine-readable records. `sunomega export-metta` deterministically projects these records into MeTTa/Hyperon atoms for symbolic queries.

**Kinds:** source, capability, technique, experiment, preference. **Statuses:** primary-documentation, documented, hypothesis, tested, contradicted, deprecated. Non-source entries cite source records via stable IDs; optional relations (supports, contradicts, refines, depends-on, enables, addresses) point to existing IDs.

Initial official sources are provider documentation. The Reddit guide is a community source; its techniques remain hypotheses until tested. The MIT license does not relicense linked third-party materials. Put private tastes and biometrics outside this public repository.

Agent-facing format is intentionally small: each record can be read by GitHub or the CLI and maps into `(Record "id" "kind")`, `(Cites "id" "source-id")`, `(Topic "id" "topic")`, and other atoms. Do not directly edit generated MeTTa; edit source JSON and re-export.

**Next:** introduce experimental observations, contradicted guidance, per-model applicability, and a read-only shared MCP knowledge interface after the existing repository/query workflow is proven useful.
