# DESIGN.md — Stemma: an AI-assisted research monorepo template

> **Status: living design document, exploratory.**
> This repository is a domain-agnostic *template* for AI-assisted academic research.
> The design below is high-level on purpose: structural commitments are minimal, and
> most mechanics (verification, literature, meetings, permissions) are deliberately
> left as open questions to be settled by piloting the template against a real
> project in a separate repository and feeding findings back here.
>
> This file documents the *template's* design and is a template-development artifact:
> it lives in the Stemma repository and does not travel into instantiated projects
> (see §8). A project's own overview lives in `PROJECT.md`.

## 1. Purpose

A reusable monorepo template supporting the full research lifecycle — conception,
meetings, literature, proofs, numerics, reusable software, manuscript, and public
release — with AI-assisted work as a first-class workflow rather than an add-on,
usable by collaborators who are not strong programmers.

The design is provider-neutral. Two open standards carry the portable layer:
`AGENTS.md` (read by most agent tools) for project instructions, and the Agent
Skills format (`SKILL.md` files, read across Claude Code, Codex, Cursor, Gemini,
Copilot, and others) for reusable procedures. Only genuinely tool-specific
automation (subagents, slash-command ergonomics) lives in a vendor directory.

Development loop: design the template here → instantiate it in a real project repo →
run real work through it → return findings as feedback → revise.

## 2. Principles

**P1 — The repository is the shared memory.**
Agents are stateless; humans forget; chat scrolls away. Durable state lives in the
repo, where both humans and agents can read it. Agent work should end with a
write-back (a diff), and long-running work keeps its own log so continuity survives
sessions. The repository — not a vendor memory feature — is canonical, because only
the repository is shared, reviewable, and exportable. Durable, inspectable state is
also what makes agent workflows *testable*: a workflow whose output is a diff can be
asserted against; one whose output is only chat cannot.

**P2 — Agent output is unverified by default.**
Agents produce plausible text faster than humans can check it. The template must make
verification status visible and require some gate before agent work reaches
release-facing directories. For investigations the gate is the closing PR (§4);
finer mechanics — statuses, reviewer agents — remain open questions for the
pilot (§6).

**P3 — Second-use rule.**
Add structure only after the need has been felt twice. v0.1 is a skeleton, not a
system. The rule defers structure we are unsure about; it does not forbid structure
whose need is already certain (e.g. detailed per-paper literature notes, §3). It
applies to skills too: ship few, high-signal ones. Recent empirical work finds that
bloated or auto-generated instruction files measurably *degrade* agent performance,
so sparseness is a correctness property, not just tidiness.

## 3. Structure

Three zones, distinguished by what crosses the export boundary.

- **Release** — ships with the paper. On publication these files are copied into a
  fresh public repository.
- **Research** — private; the scientific and exploratory core. Never enters public
  history.
- **Operations** — runs the repository: project overview, agent instructions, and the
  `.stemma/` framework layer. Not exported.

```text
Release
  README.md
  src/project_name/          # real default name; init renames it
  tests/
  data/
  reproduce/
  manuscript/

  pyproject.toml
  .pre-commit-config.yaml
  .github/workflows/ci.yml
  .gitignore
  (CITATION.cff)
  (LICENSE)

Research
  PROJECT.md
  research/
  ├── STATE.md
  ├── FINDINGS.md
  ├── QUESTIONS.md
  ├── SURVEY.md
  ├── investigations/
  │   └── _template/         # question.md, log.md, README.md, review.md
  ├── literature/            # per-paper notes, keyed by cite key
  ├── meetings/
  ├── notes/
  └── workbench/

Operations
  AGENTS.md                  # router: project map + always-apply rules + pointers
  CLAUDE.md                  # points to AGENTS.md (@AGENTS.md import; plain file)
  init.sh                    # root: run-once instantiation entry point
  .stemma/                   # the framework layer (see §5)
```

Parenthesised entries are added before public release, not at project start.

**The `research/` file set.** Sort by rhythm: *now / known / unknown*.
`STATE.md` is the current snapshot (now + next) and carries most of the weight for
v0.1. `FINDINGS.md` accumulates established results and dead ends. `QUESTIONS.md`
holds open questions — scientific or technical — that are not yet sharp enough to
become investigations; the moment a question has a recognisable answer it is a task
(`STATE.md`) or a charter, not a question. `SURVEY.md` is the standing overview of
the literature. `PROJECT.md` — the write-once motivation and context, including the
prior work the project builds on — sits at the zone root. `DECISIONS.md` and
`GLOSSARY.md` are cut for v0.1 (second-use rule).

**Literature.** Three separable jobs, three homes, joined by cite key:
citation *metadata* is `manuscript/references.bib` (a generated artifact — canonical
maintenance happens in a reference manager such as Zotero, which exports the `.bib`;
it is committed so the export compiles standalone, and never hand-edited); the
*library* itself (PDFs, metadata) lives in the reference manager, outside git — PDFs
are never committed (binary, large, mostly copyrighted, and the large-file hook
should block them); *notes* live in `research/`, with `SURVEY.md` as the narrative
and `literature/<citekey>.md` as substantial per-paper notes (theorems, proofs,
methods, results). Per-paper notes separate transcription (what the paper states,
verifiable) from project inference (what we conclude for our problem, revisable and
gate-worthy).

**Agent access to knowledge** follows a hierarchy, cheapest first: project knowledge
(`FINDINGS.md`, investigation READMEs, `STATE.md`) → distilled paper knowledge
(`literature/*.md`) → source PDFs (retrieved on demand via a reference-manager
integration, with findings written back into the note).

## 4. Working assumptions (adopted for now, revisable after the pilot)

- **What needs a PR is defined by consequence and actor, not by zone.** The gate has
  two tiers:
  - *Mechanically enforceable (path-based):* changes to `src/` and `tests/` require a
    PR, for anyone. Enforceable via branch protection (an instantiation-checklist
    step, not a shipped file).
  - *Convention (actor-based, in `AGENTS.md`):* agents never commit to `src/`/`tests/`
    directly; agent edits to `manuscript/` arrive as PRs while human drafting is
    direct; investigations close with one PR; new conclusions reach `FINDINGS.md` only
    through an investigation's closing PR. Git cannot distinguish agent from human, so
    these are conventions the agent follows, not mechanical rules — good enough,
    because the agent is both the party of concern and the party that reads
    `AGENTS.md`, and the unguarded failure (a human committing directly) is the safe
    one.
  - *Direct commit, no PR:* everything else — `notes/`, `workbench/`, `STATE.md`,
    `QUESTIONS.md`, `SURVEY.md`, `literature/`, `meetings/`, and human manuscript
    drafting.
- **Investigations are bounded by construction.** The charter test: could you
  recognize an answer if you saw one? If not, it belongs in `QUESTIONS.md`. A
  long-running inquiry is a *thread* — a sequence of bounded investigations linked by
  `superseded-by`. `workbench/` is the pre-charter escape valve.
- **One branch per investigation; one PR at its conclusion.** The charter
  (`question.md` + stub `README.md`) is committed directly to main at birth, so main
  always knows the investigation exists and which branch holds it (`STATE.md` lists
  in-flight investigations with their branches). The branch touches only its own
  directory; cross-cutting edits go to main via the housekeeping lane. The closing PR
  is the verification gate (P2): `review.md` is written in preparing it.
- **Export is a fail-closed allowlist.** Release is enumerated; everything else is
  private by *not being listed*. A new file defaults to private, so forgetting fails
  safe. `export.sh` copies the Release allowlist into a fresh directory, `git init`s a
  single clean commit, verifies nothing in the copy depends on anything outside it,
  and then stops — it does not push. Publishing is a deliberate manual step.
- **Nothing in Release may depend on anything outside it.** Not just `reproduce/`: no
  Release file may import from or depend on `research/` or any non-exported path, or
  export breaks silently. This is the one invariant whose violation is invisible
  (works locally, breaks only after export), so it is worth a mechanical check
  (§5, `check_zones.py`).
- **Manuscript policy is phase-dependent.** Humans commit directly while drafting;
  agent edits arrive as PRs; everything tightens near submission.
- **Linting scope follows the code, not the repo.** Ruff (code linting) is scoped to
  `src/`/`tests/`; hygiene hooks (whitespace, secret detection, merge-conflict) run
  repo-wide, including `research/` — the ungated housekeeping lane has no human
  backstop, so it needs the machine hygiene most. Content-rewriting formatters
  (`pyproject-fmt`) are *not* run on template files: they mangle placeholders and
  re-add deliberately-omitted metadata; safe only after instantiation.
- Conventions worth having from day one: one-sentence-per-line LaTeX; environments
  from `pyproject.toml` alone (plain `pip`, no `requirements.txt`); figures generated
  only by scripts in `reproduce/`.

## 5. Framework layer: `.stemma/`

Stemma is a **framework the project sits inside**, not merely a scaffold it outgrows.
The instantiated project keeps a live `.stemma/` layer that it uses throughout its
life and can update from upstream (copier-style). This is the reason `.stemma/` is a
dotfile directory: it signals *managed framework machinery, not project content, do
not hand-edit*.

```text
.stemma/
  README.md          # what Stemma is and what this layer holds (framework's own readme)
  export.sh          # copy Release -> fresh repo; verify; stop before pushing
  check_zones.py     # Release must not depend on Research (mechanical, §4)
  skills/            # portable SKILL.md procedures (the agent procedure layer)
  (docs, further tools added on second use — flat until the count warrants subdirs)
  tests/             # tests of the framework tooling — TEMPLATE-REPO-ONLY (§8)
```

Scripts sit directly under `.stemma/` (flat) until the count warrants subdirectories.

**Three tiers of agent instruction, portable-first:**
- **`AGENTS.md` — the router.** Short and high-signal: what the project is, the
  project map, and the always-apply rules (the PR tiers, the export-allowlist
  invariant, "nothing in Release depends on anything outside it", "conclusions reach
  `FINDINGS.md` only through a closing PR"). It points to skills rather than
  containing procedures. Kept sparse: everything here loads every session.
  `CLAUDE.md` is a one-line `@AGENTS.md` import (a plain file, not a symlink).
- **`.stemma/skills/*/SKILL.md` — the procedures.** Portable (read across tools) and
  progressively disclosed (only names/descriptions load at startup; the body loads on
  match). Where workflow logic lives — starting an investigation, the meeting routine,
  verifying a finding.
- **`.claude/` — the vendor remainder** (if present). Only genuinely Claude-specific
  automation: slash-command ergonomics, subagent definitions. Orchestration is not
  portable across tools; only the *guarantees* it must deliver belong in the portable
  layer.

**v0.1 skills.** Ship one — `new-investigation`. Candidates added on second use: a
meeting routine, a self-review checklist. **Skills are a dependency surface**: audits
in 2026 found a substantial fraction of community skills carried prompt-injection or
other issues, and skills can bundle executable scripts. Treat third-party skills like
code dependencies; first-party ones are in-scope for normal review.

**`check_zones.py`** enforces the Release-does-not-depend-on-Research invariant. v0.1:
scan Release-zone Python for imports resolving into non-Release paths; run as a
`local` pre-commit hook scoped to `^(src|tests|reproduce|manuscript)/.*\.py$`. The
definitive version is the export-and-verify test (§6): export, then install and test
in a sandbox with `research/` absent — if Release depended on it, the sandbox fails.

## 6. Testing

Two distinct testing concerns, with different homes:

- **Project code** (`src/`, `tests/`) — the instantiated project's own CI
  (`.github/workflows/ci.yml`): `pip install -e ".[dev]"`, `pytest` across a Python
  matrix, plus `pre-commit run --all-files` (the enforcement copy of the hooks, which
  cannot be bypassed with `--no-verify`). The template ships a real `project_name`
  package and a smoke test, so this CI passes on the template repo itself.
- **Framework tooling** (`.stemma/export.sh`, `check_zones.py`) — tested in the
  **Stemma template repository's own CI**, not in instantiated projects. The tests
  live in `.stemma/tests/` and are template-repo-only (§8). The two highest-value
  tests: an *instantiation test* (run `init` in a sandbox, assert a valid project with
  no surviving placeholders) and an *export-safety test* (plant secrets in `research/`,
  run `export.sh`, assert only Release ships and nothing leaks). Shell → `bats`.

Testing agent *behaviour* is not cheaply CI-able; the tractable substitute is checking
the *world-state a workflow must leave behind* (did `review.md` get written before the
PR? does `STATE.md` list the investigation? did the closing PR touch only its own
directory?) — deterministic assertions about the repo, no LLM-judge required. This is
the payoff of P1: the workflow's output is a diff, so it is a fixture.

## 7. Instantiation

Because `.stemma/` is a live framework layer and files must be rendered (placeholders
filled) or omitted (template-only), instantiation is naturally a copier-style
operation rather than a hand-rolled script; `init.sh` may implement this directly for
v0.1 and migrate to copier as the shape stabilises. Files fall into three buckets:

- **Template-only (never travels):** `DESIGN.md`, the template's own root `README.md`,
  `.stemma/tests/`. Development artifacts; copier omits them.
- **Travels as-is (framework machinery):** `.stemma/` tools, skills, docs, and its own
  `README.md`.
- **Rendered from template (project content):** root `README.md` (from a project-README
  skeleton, name/description filled), `pyproject.toml` (placeholders filled),
  `PROJECT.md`, and `src/project_name/` renamed to the project's package.

The template ships as a working package named `project_name` (import) / `project-name`
(distribution) so it builds and its CI passes before instantiation. Instantiation
renames both forms (they are different strings — replace each) across `pyproject.toml`,
the `src/` directory, and the smoke-test import, fills the metadata, swaps the README,
and afterwards greps for any surviving `project_name` / `project-name` / `{{...}}` and
warns (CI will not catch a wrong-but-consistent rename). The instantiation checklist
also notes enabling branch protection on `src/`/`tests/`.

## 8. Template-only vs travelling artifacts

The single rule: **does a researcher *using* the framework need this, or only someone
*developing* it?** Usage docs and tooling travel (in `.stemma/`); development artifacts
(`DESIGN.md`, `.stemma/tests/`, the template README) stay in the Stemma repo. The
tools travel; the tools' tests do not.

## 9. Open questions (to be answered by the pilot, not by this document)

- Verification mechanics: the closing PR is the gate; open whether finer statuses or a
  reviewer subagent earn their keep.
- Project memory: whether `QUESTIONS.md` earns its place (do questions graduate out of
  it?), and whether a decisions log is needed once challenges route to `FINDINGS.md`.
- Skills in practice: does the investigation procedure work as a portable skill across
  surfaces, or does load-bearing procedure end up trapped in `.claude/`? Does
  progressive disclosure actually fire?
- Framework vs scaffold: does the live-`.stemma/` + `copier update` model hold up, or
  do projects drift from upstream and stop updating?
- Literature pipeline: reference-manager/MCP wiring, citation-verification tooling.
  Observables: drift between `references.bib` and the notes; how often an agent needs a
  raw PDF.
- Task tracking: does "next" in `STATE.md` suffice, or do GitHub Issues get used?
- Data at scale: when to introduce DVC/LFS/Zenodo; the large-file threshold.
- Environments: does plain pip + `pyproject.toml` suffice, or is a lockfile (`uv`)
  eventually needed?
- CI: how much, how path-filtered. Path-filtering finds its first legitimate use in the
  framework-CI (run only when `.stemma/**` changes); project CI stays unfiltered.
- Non-coder entry points: which surface (Cowork, Slack, web) gets used, and whether an
  investigation started there reaches the same end state as one run through Claude Code.
- Zone-check depth: does the grep-level `check_zones.py` suffice, or is AST-level
  import analysis (`import-linter`) needed?
- What's missing entirely — the pilot's job is to surface this.

## 10. v0.1 scope

Scaffold only: the tree above with stub files that establish each convention (a seeded
`STATE.md`, the investigation template, a sparse `AGENTS.md` router, the one
`new-investigation` skill, `check_zones.py`), pre-commit basics, and a minimal CI
workflow that installs the real `project_name` package and runs the smoke test. No
release-script logic beyond copying the allowlist; no framework tests yet (they need
real `export.sh`/`init` logic — post-pilot).

**Pilot plan:** copy the template into an existing project's repo, run one real bounded
investigation through the `new-investigation` skill, and log what worked, what fought
back, and what was missing. Findings return here as issues; v0.2 follows the evidence.
Non-coder surfaces are out of scope for pilot one. The pilot also tracks whether
`log.md` actually gets written every session; P1's write-back rule has no other teeth.

---

*Changes from the prior draft:* introduced the **`.stemma/` framework layer** and the
framework-vs-scaffold decision (Stemma is a live layer the project keeps and updates,
not a scaffold deleted at instantiation) — scripts and skills moved under `.stemma/`
(flat), the Operations zone reorganised around it. Added the **two-tier PR model**
(mechanical path-based for `src`/`tests`; convention actor-based in `AGENTS.md`),
replacing the earlier lane-by-zone framing. Added the **testing section** (project CI
vs framework CI, world-state assertions for agent workflows) and the **template-only
vs travelling** rule (§8), with `DESIGN.md`, the template README, and `.stemma/tests/`
as template-repo-only. Recorded the **linting scope** (ruff on Release, hygiene
repo-wide) and the **pyproject-fmt hazard** on template files. Noted the shipped
`project_name`/`project-name` package and the copier-style instantiation the framework
model implies. `init.sh` stays at root (run-once entry point); `DESIGN.md` no longer
claims to be deleted by it — it simply never travels.
