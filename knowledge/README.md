# SunOmega knowledge corpus — GF-style contracts + AtomSpace index

The canonical knowledge source is **Git-versioned JSON**, one file per record under `knowledge/records/`. Agents can inspect the JSON through GitHub or the local `sunomega` CLI. A deterministic projection converts graph edges, source attribution and GF procedure details into queryable MeTTa/Hyperon atoms. **Do not maintain a second, independently edited AtomSpace copy.**

## Retrieval from repository root

```bash
sunomega validate
sunomega builds
sunomega search "breathing"
sunomega show technique-lyric-prosody
sunomega export-metta
sunomega smoke-metta
```

`search` is presently a **case-insensitive substring baseline**, now including build targets, applicable situations, execution steps and proof checks. It is *not* semantic retrieval; evaluating natural-language paraphrases is a separate research task. `show` prints the complete structured record.

## Two layers, one source of truth

**Knowledge records** give stable IDs, titles, kind, status, topics, provenance via source IDs and typed `relations`. Source and experiment records need not be actionable. A **technique** must have a GF-style `build` contract. A capability may also have one. The contract includes:

| GF concept | JSON field | Meaning |
| --- | --- | --- |
| Target | `build.target` | One observable musical/production outcome |
| Equip | `build.requires`, `inputs`, `outputs` | Host, grants, materials, result |
| Execute | `build.execute[]` | Ordered production steps; advisory until authorized |
| Matchup | `build.matchup.applies_when`, `avoid_when` | Context, limits, known blockers |
| Effects and bounds | `build.effects`, `bounds.enforced`, `bounds.operator` | Local/network/account/spend scope; guaranteed vs operator-enforced |
| Stop | `build.stop_when` | Bounded completion and failure |
| Proof | `build.proof.status`, `checks`, `evidence` | Observability, evidence and caveats |

Proof statuses: `proposed`, `provider-documented`, `locally-tested`, `provider-tested`, `listener-observed`. The provider-documented status means official instructions exist, **not** that Omega successfully exercised the operation. These are distinct evidence categories, not a single universal quality score. Community prompt advice stays proposed unless independently tested.

**Executable GF packages** are separately referenced by `build_path`, e.g. `capability-semantic-midi` links to `skills/semantic-midi/build.json`. Only these packages expose an entrypoint helper, package-local skill, license and evidence. A declarative musical recipe does not become executable code merely because it has `execute` steps. Validation checks linked package files without running them.

## Example of the AtomSpace index

Generated facts include:

```metta
(Record "technique-lyric-prosody" "technique")
(Cites "technique-lyric-prosody" "source-reddit-v6-guide-2026")
(BuildProofStatus "technique-lyric-prosody" "proposed")
(BuildEffect "technique-lyric-prosody" "spend")
(BuildPath "capability-semantic-midi" "skills/semantic-midi/build.json")
```

MeTTa can match a technique, inspect its provenance and request the full build from the canonical record. No `BuildStep` confers permission to run tools. Tool/grant authentication and credit approvals remain with the actual host/operator.

## Contribution policy

- One focused, source-linked record per claim or procedure; cite original source URLs and access dates.
- Keep failures, contradictions, model/version scope and human listening evaluations as distinct evidence.
- Preserve the GF distinction between specified score, verified MIDI, completed Suno clip, measured audio adherence and listener experience.
- Do not copy copyrighted source guides/audio into the MIT corpus, commit tokens, or publish individual mood/taste/biometric data.
- Run `python -m unittest discover -s tests -v` and (when installed) `sunomega smoke-metta`; review the generated diff.

See [knowledge policy](../docs/KNOWLEDGE_POLICY.md), [GF transfer](../research/GF_TRANSFER.md), and [semantic-midi skill](../skills/semantic-midi/SKILL.md).
