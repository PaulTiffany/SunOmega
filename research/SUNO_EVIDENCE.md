# Suno production evidence and research priorities

**Checked:** 2026-11-22. This is a citable research register, not a vendor-specific hidden prompt syntax. See [sources.json](sources.json) for exact publisher, URLs and evidence classes. Neither source claims nor snippets are relicensed by SunOmega's MIT license.

## Provider-confirmed capabilities

| Finding | Scope / qualification | Source ID |
|---|---|---|
| Official remote MCP endpoint `https://api.suno.com/mcp`; supported clients authorize via sign-in | Other clients must have appropriate remote MCP + authorization flow; *Omega not yet proven* | S1 |
| MCP works across plans, including Free; song creation draws credits | Tool grants and model access vary by account | S2 |
| v6, v6-wild, v6-mini have different creative roles; v6-mini for all; v6/v6-wild Pro/Premier | Models and access may change; inspect current account before calling | S3 |
| v6 Simple Mode supports complex briefs and multiple references; Variety can rewrite styles; 0 is a controlled tag baseline | Model still stochastic; provider does not promise exact phrase timing | S4 |
| MIDI file upload in *Simple Create*: notes guide musical material, text directs timbre/feel | Web desktop documentation says Pro/Premier; November 4, 2026; actual MCP support/grants require discovery | S5 |
| Stem separation is supported; Pro/Premier Get Stems; advanced modes can consume credits | Studio-specific modes and pricing are not automatically the same as MCP operations | S6 |
| Suno My Taste already personalizes style prompts | A personalized Omega DJ's novelty cannot simply be “learning musical taste” | S7 |

**Connector-specific provisional observation:** the Suno tool interface available in this ChatGPT environment advertises a MIDI upload path for original scores, followed by a `midi_upload_id` on simple `audio_create`, conditional on specific model and sign-in grants. Treat this as an interface contract for that connected environment, **not** proof that another Omega will see identical tools. The connection proof must discover actual names/grants.

## Early community prompt guidance — hypotheses only

The linked Reddit guide synthesizes launch-week v6 experiments rather than a controlled study or undocumented system prompt [S8]. Candidate rules worth testing:
- Prefer prioritized musician/producer instructions over tag clouds; compare short vs long briefs.
- Specify a rhythmic **feel**, instrument **actions** and evolving **arrangement arc**, not just genre and BPM.
- Specify singer's register, articulation, dynamics and section behavior; use lyric syllable patterns and line breaks as possible melodic control.
- Treat bracket tags, exact bar counts, numerical BPM and invented commands as **soft conditioning**, not deterministic instructions.
- A/B Simple vs custom modes, keep all controls fixed, test one change at a time. Variety=0 has a provider-documented meaning but does *not* imply seed determinism.
- Try editing or extending a nearly good song rather than discarding it; test sibling mashups and references separately. Do not infer guaranteed superiority.

Independent community experience [S9] documents possible vocal/instrument loss, distant mixes, abrupt endings and tuning difficulties; use these as candidate failure categories, not prevalence estimates.

## Independent academic findings (not Suno claims)

- Score-format representation matters: a 2026 preprint compares MusicXML, MIDI and ABC across 26 models and reports benefits for richer notation on its benchmarks [S10]. It does not validate a Suno MIDI workflow or our score DSL.
- In a 2025 ISMIR study, common distributional audio metrics correlated poorly with human preference in the measured tasks [S11]. **Implication:** listen in blinded comparisons; do not use beat/key analysis alone as proof of artistic success.
- A 2025 ISMIR late-breaking demonstration reports improvements from retrieval-augmented prompt rewrites for Stable Audio 2.0 [S12]. Supports researching retrieval-based prompt assistance **as a hypothesis**; not automatically transferable to Suno.
- CMU's reference distinguishes MIDI performance messages from richer score notation [S13]. music21 imports/exports music notation and MIDI [S14]; mido is well suited to small exact MIDI writes [S15].

## What would help an LLM producer most

1. **Feature/capability gates:** never waste calls on unavailable models, hidden slider grants, unsupported MIDI routes or unauthorized credit spending.
2. **Problem -> verified procedure retrieval:** “rushed vocals”, “chorus did not lift”, “drum bridge”, “MIDI motif adherence” need precise, source-ranked remedies with negative evidence.
3. **Semantic score:** intent and phrase structure separated from exact note-time instructions; a compiler rejects missing decisions rather than pretending to infer them.
4. **Output receipts:** complete request parameters, model, feature grants, source version, clip IDs, analysis with uncertainty, human preference.
5. **Two-stage evaluation:** local technical validity first; listening/fidelity experiments only when the operator authorizes Suno credit use.

## High-priority unanswered questions

- Can an actual Omega authenticate with the official server and expose the required operations? **M0 outstanding.**
- Does the MCP MIDI path behave the same way as the documented desktop Create path? What model constraints apply?
- Does a 4/8-bar original melody retain intervals, onset patterns and cadence after generation better than an otherwise matched text brief?
- Can agents reliably steer **vocal pacing** through prosody without flattening a dramatic build?
- Is a short, structured production brief more effective than a detailed one under identical controls?
- Which stem operations produce a clean, cost-effective drum bridge, and does the transition survive objective beat alignment and subjective DJ listening?
- What does private user preference add beyond Suno's existing My Taste feature?

## Non-goals

No invented deterministic Suno prompt syntax, no untested universal slider recipes, no claim that v6 can perfectly copy a MIDI score, no automatic mood diagnosis, and no transfer of private user listening data into the public AtomSpace.
