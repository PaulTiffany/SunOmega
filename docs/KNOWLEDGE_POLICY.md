# Knowledge admission, evidence and GF-style build contracts

Every `knowledge/records/*.json` file is a versioned, source-attributed fact or proposal. The top-level fields are `id`, `kind`, `title`, `summary`, `status`, `topics`, `sources` and `relations`; source records also require `url` and `accessed`.

**Records are not commands.** Every `technique` must carry a validated `build` object with `target`, `requires`, `inputs`, `outputs`, `execute`, `matchup`, `effects`, `bounds`, `stop_when` and `proof`. A `capability` may carry the same contract; if it references an executable GF helper with `build_path`, it must have a contract too.

Contract metadata is for inspecting requirements and planning an authorized action. It neither installs tools nor grants permissions. `effects` names possible impact (`local-read`, `local-write`, `network-read`, `network-write`, `account-write`, `spend`). `bounds.enforced` must include only limits checked by code. `bounds.operator` identifies constraints that require human/host enforcement. `stop_when` must preclude unbounded paid retries.

**Evidence** is explicitly scoped. `build.proof.status` is one of `proposed`, `provider-documented`, `locally-tested`, `provider-tested`, `listener-observed`. Tested statuses require a visible evidence link. These are distinct types of evidence: provider documentation is not an integration test; source-to-MIDI fidelity does not establish rendered Suno melody fidelity, and either does not prove audience satisfaction. Do not promote an anecdote to tested simply by adding more prose.

**Trust:** vendor docs support provider capabilities and documented grants. Community Reddit prompt advice is a source of hypotheses. Controlled experiments preserve model, full settings, prompt/score hashes, candidate IDs, failures, and human judgments. Model-specific claims should never become universal best practices. Record contradictions explicitly.

**Rights and privacy:** original SunOmega text/code may be MIT licensed; third-party sources and audio retain separate rights. Link and summarize rather than reproduce a full prompt guide. Never store credentials, personal listener profiles, individual biofeedback, third-party recordings without consent, or unpublished origination/continual-learning mechanisms in this public repository.

## Example retrieval

An agent asked “our singer races through the chorus” should find `technique-lyric-prosody`, inspect the GF `matchup`, read its Reddit source and `proposed` evidence status, and prepare an A/B plan. It should not call Suno or spend credits merely because the `execute` list contains a generation step. `sunomega show technique-lyric-prosody` reveals the full contract; `sunomega export-metta` provides graph matching and provenance traversal.
