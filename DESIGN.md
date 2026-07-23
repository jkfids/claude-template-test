# DESIGN.md — Stemma: an AI-assisted research monorepo template

> **Status: living design document, exploratory.**
> This repository is a domain-agnostic *template* for AI-assisted academic research.
> The design below is high-level on purpose: structural commitments are minimal, and
> most mechanics are deliberately left as open questions to be settled by piloting
> the template against a real project and feeding findings back here.
>
> This file documents the *template's* design and is a template-development
> artifact: it lives in the Stemma repository and does not travel into
> instantiated projects (§9). A project's own overview lives in `PROJECT.md`;
> a project's own decision log lives in `research/DECISIONS.md`.

## 1. Purpose

A reusable monorepo template supporting the full research lifecycle — conception,
meetings, literature, proofs, numerics, reusable software, manuscript, and public
release — with AI-assisted work as a first-class workflow rather than an add-on,
usable by collaborators who are not strong programmers.

The design is provider-neutral. Two open standards carry the portable layer:
`AGENTS.md` (read by most agent tools) for project instructions, and the Agent
Skills format (`SKILL.md`) for reusable procedures. Only genuinely tool-specific
automation lives in a vendor directory (`.claude/`).

Development loop: design the template here → instantiate it in a real project →
run real work through it → return findings → revise.

## 2. Principles

**P1 — The repository is the shared memory.**
Agents are stateless; humans forget; chat scrolls away. Durable state lives in the
repo, where both humans and agents read it. Agent work ends with a write-back (a
diff); long-running work keeps its own log. The repository — not a vendor memory
feature — is canonical, because only the repository is shared, reviewable, and
exportable. Durable state is also what makes agent workflows *testable*: a
workflow whose output is a diff can be asserted against.

**P2 — No conclusion enters canonical memory on conversational confidence alone.**
Agents produce plausible text faster than humans can check it. The gate is not
"who did the work" (nearly everything is AI-assisted) but *how knowledge is
accepted*: canonical entries arrive as reviewable diffs, and a human performs the
acceptance. Concretely: agents open PRs and never merge them — **merging is the
human acceptance act** (§5). Auto-merge is acceptable only where the acceptance
criterion is machine-checkable (dependency bumps on green CI), which canonical
knowledge never is.

**P3 — Second-use rule.**
Add structure only after the need is felt twice. It applies to files (DECISIONS
was cut, then revived when a real category emerged), directories (no `writeups/`
until notes/ clutters), subdirectories (`.stemma/` stays flat), branches (no dev
branch — the zone/export model already separates tooling from releases), and
skills (ship few; bloated instruction files measurably degrade agents). Contracts
state bars; prompts state formats; neither demands content whose value varies by
entry ("rationale where it isn't obvious", not mandatory fields). Going
lean→structured later is cheap; walking back unfilled structure is not.

## 3. Structure

Three zones, distinguished by what crosses the export boundary.

```text
Release                              # ships with the paper
  README.md
  src/project_name/                  # real default name; init renames it
  tests/
  data/
  reproduce/
  manuscript/                        # self-contained TeX root (Overleaf/arXiv)
  pyproject.toml
  .pre-commit-config.yaml
  .github/workflows/ci.yml
  .gitignore
  (CITATION.cff)  (LICENSE)          # added before public release

Research                             # private; never exported
  PROJECT.md
  research/
  ├── README.md                      # zone meta-doc
  ├── STATUS.md                      # coordination snapshot
  ├── FINDINGS.md                    # canonical scientific knowledge
  ├── DECISIONS.md                   # project-level choices + rationale
  ├── QUESTIONS.md                   # open unknowns; Resolved routing index
  ├── SURVEY.md                      # literature synthesis
  ├── investigations/  (_template/)  # bounded, branch-per, closed by PR
  ├── literature/      (_template.md)# per-source notes by citekey
  ├── meetings/        (_template.md)
  ├── notes/                         # logbook, writeups, working notes
  └── workbench/                     # scratch; promotable via writeup

Operations                           # runs the repo; not exported
  AGENTS.md                          # router (root: tool-discovered)
  CLAUDE.md                          # @AGENTS.md import (plain file)
  .agents/skills/                    # portable skills (root: tool-discovered)
  .claude/                           # vendor remainder
  init.sh                            # run-once entry point (root: visible)
  .stemma/                           # framework layer (§6)
```

**Placement rule:** if an external tool must *discover* it by scanning
conventional paths, it lives at root (`AGENTS.md`, skills, `.claude/`); if only
our own code invokes it by explicit path, it lives in `.stemma/`.

## 4. Project memory: the epistemic hierarchy

The research files are organised by *evidential status*, which tells a reader
(especially an agent) what to trust:

- **Canonical** — `FINDINGS.md` (what the project is prepared to rely on) and
  `DECISIONS.md` (what it chose to do, and why). FINDINGS records truths;
  DECISIONS records choices; each contract states the boundary from its side.
- **Provenance** — the evidence canonical entries cite: a closed investigation,
  a writeup in `notes/`, a legible `workbench/` directory, or a citation key for
  verified external results. Provenance is heterogeneous by design; the FINDINGS
  entry's link says which kind.
- **Coordination** — `STATUS.md`: tasks, queue, active investigations. A rough
  snapshot, not evidence; rewritten, never appended. Active-investigation lines
  are touched only at charter and close (write-once-per-investigation), so
  branches never contend over it.
- **Identified unknowns** — `QUESTIONS.md`: research-significant open questions,
  phrased so an answer could be recognised. Questions resolve however the answer
  arrives (investigation, promoted work, a decision, the literature); the
  Resolved section is a routing index that points at the *most canonical record*
  of the answer — never at raw provenance or PR numbers — and preserves original
  phrasing so old uncertainties are not re-opened.
- **Raw** — `notes/`, `workbench/`, `meetings/`, investigation logs.
  Direct-commit, no ceremony; capture must stay friction-free.

**Knowledge flows upward, and the promotion path is explicit.** Rough work
(workbench, chat conclusions, collaborator results) becomes canonical via a
*writeup*: a self-contained note (claim, support, scope, caveats, pointers to raw
work) that an agent can draft (`write-up` skill) and that travels in a promotion
PR together with the FINDINGS entry citing it. Merging that PR is the acceptance
(P2). Conclusions with no repo evidence are staged as notes, not filed as
findings. SURVEY holds what the field established; FINDINGS holds what this
project established (including "we verified imported result X in our regime").

**House style for memory files:** a `>` blockquote carries each file's *editing
contract* (visible to humans, distinct from content); HTML comments carry
per-section prompts (invisible when rendered, greppable); no placeholder body
text; ISO dates. The blockquote convention is strict — editing contracts only —
so Release READMEs (which are shipped project documentation, not contracts) use
plain prose.

## 5. Working assumptions (adopted for now, revisable after the pilot)

- **PRs, two tiers.** *Mechanical (path-based, branch protection):* `src/`,
  `tests/` require a PR for anyone. *Convention (actor-based, in `AGENTS.md`):*
  agents never commit those directly; agent edits to `manuscript/` are PRs while
  human drafting is direct; investigations close with one PR; findings entered by
  agent hands arrive by PR even when a human asked. **Agents open PRs; humans
  merge them.** Everything else — notes, workbench, STATUS/QUESTIONS/SURVEY
  housekeeping, DECISIONS entries (recording a decision is making it; the commit
  witnesses it), literature, meetings — is direct commit.
- **Investigations are bounded by construction** (charter test: could you
  recognise an answer?), branch-per-investigation, charter committed to main at
  birth, one closing PR as the gate. Investigations mark *work, not intentions*:
  they are chartered when verification work actually begins, never auto-created
  from conversations — an investigations/ directory of husks would debase the
  provenance the hierarchy depends on.
- **Export is a fail-closed allowlist**; nothing in Release may depend on
  anything not exported (the one silently-violated invariant; mechanically
  checked by `check_zones.py`). Manuscript is a self-contained TeX root: figures
  are generated by `reproduce/` and committed to `manuscript/figures/` so it
  compiles alone (Overleaf, arXiv submission).
- **Release READMEs** are templates: fixed conventions plus HTML-comment prompts,
  written author-facing but reproducer-safe (the export audience vetoes
  framework vocabulary), finalised at export. Soft on preferences (script
  granularity), firm on invariants (figure destination, no non-exported imports).
- **Linting follows the code:** ruff scoped to `src/`/`tests/`; hygiene hooks
  (whitespace, keys, merge-conflict) repo-wide — the ungated housekeeping lane
  has no human backstop, so it needs machine hygiene most. Content-rewriting
  formatters (pyproject-fmt) never run on template files (they mangle
  placeholders); commented in config with a do-not-enable-until-instantiated
  warning.
- Conventions from day one: one-sentence-per-line LaTeX; environments from
  `pyproject.toml` alone; figures only from `reproduce/`.

## 6. Framework layer: `.stemma/`

Stemma is a framework the project keeps and updates (copier-style), not a
scaffold it deletes. `.stemma/` is a dotdir to signal *managed machinery — run
it, don't hand-edit it*. Agents run its scripts when asked (export, checks) but
do not modify its internals in an instantiated project.

```text
.stemma/
  README.md            # the framework's own readme (what this layer is)
  export.sh            # Release → fresh repo; verify; stop before pushing
  check_zones.py       # Release must not depend on non-exported paths
  templates/           # instantiation templates, rendered once at init:
    README.md          #   → root README.md (project/companion README)
    CITATION.cff       #   structured fill-in metadata
  tests/               # framework tests — TEMPLATE-REPO-ONLY (§8)
```

Flat until the script count warrants subdirectories. **Template taxonomy:**
*instantiation templates* (rendered once) live in `.stemma/templates/`; *runtime
templates* (copied repeatedly: investigation `_template/`, literature and meeting
`_template.md`) live in place in `research/`, editable as the project's
methodology evolves; *singleton stubs* (the memory files) ship as the files
themselves, structure and prompts baked in. LICENSE is none of these — a
canonical legal text `init.sh` selects and stamps (copyright line only), never a
hand-maintained skeleton (legal-text drift is not "close enough").

**Agent instruction, three tiers:** `AGENTS.md` the sparse router (map,
always-apply rules, precedence over local READMEs, pointer to `.stemma/`
scripts); skills the procedures (v0.1: `new-investigation`, plus `write-up` for
the promotion path — both artifact-producing, hence world-state-testable);
`.claude/` the vendor remainder. Facts sort by scope: everywhere → AGENTS.md;
named-task procedure → skill; this-directory-only → its README; and each
memory file's own contract governs itself.

## 7. Testing

- **Project code** — `ci.yml` (travels): install `.[dev]` across 3.12/3.13/3.14,
  pytest, plus `pre-commit run --all-files` as the unbypassable enforcement copy
  of the hooks. The template ships a working `project_name` package and smoke
  test, so this CI passes on the template repo itself.
- **Framework tooling** — tested in the Stemma repo's own CI (`stemma.yml`,
  path-filtered to `.stemma/**` — path-filtering's first legitimate use), tests
  in `.stemma/tests/`, template-repo-only. Highest value: instantiation test
  (init in a sandbox; assert a valid project, no surviving placeholders) and
  export-safety test (plant secrets in research/; assert only Release ships and
  the export installs/tests green with research/ absent). Shell → bats. Deferred
  until the scripts have real logic; scripts should take args (not only
  interactive prompts) so tests can drive them.
- **Agent behaviour** — not cheaply CI-able; test the *world-state a workflow
  must leave* (was the writeup written? does STATUS list the investigation? did
  the closing PR touch only its directory?). P1's payoff: output-is-a-diff means
  the fixture is free.

## 8. Instantiation

The template ships as a working package `project_name` (import) /
`project-name` (distribution) so it builds pre-instantiation. `init.sh` (root,
run-once; v0.1 may just print the checklist) renames both forms — different
strings, separate substitutions — across `pyproject.toml`, `src/`, and the smoke
test; fills metadata; renders `.stemma/templates/` (project README → root,
replacing the template's own README, which never travels); writes the stamped
LICENSE; installs pre-commit; then greps for surviving
`project_name`/`project-name`/`{{...}}` and warns — CI cannot catch a
wrong-but-consistent rename. Checklist includes enabling branch protection on
`src/`/`tests/`.

## 9. Template-only vs travelling

One rule: **does a researcher *using* the framework need it, or only someone
*developing* it?** Travels: `.stemma/` tools, templates, docs, its README; all
zone content and stubs. Template-repo-only: `DESIGN.md`, the template's root
README, `.stemma/tests/`. The tools travel; the tools' tests do not.

## 10. Open questions (for the pilot)

- Does the promotion path get used, or routed around (FINDINGS entries appearing
  without writeups)? Does the humans-merge rule hold?
- Does DECISIONS fill, or was its revival premature? Does QUESTIONS' Resolved
  section fill (working) or stay empty while Open grows (graveyard → fold into
  STATUS)?
- Does STATUS's Summary (which now carries the "why" for the task list) stay
  current, or does the inline-why-per-task pattern prove more self-maintaining?
- Skills across surfaces; progressive disclosure; whether `write-up` and
  `new-investigation` suffice or a meeting routine earns its place.
- Framework model: do projects actually `copier update`, or drift?
- Literature wiring (reference manager/MCP); grep-level vs AST-level zone check;
  lockfiles (uv); Issues vs STATUS for tasks; data at scale (DVC/Zenodo);
  non-coder entry points.
- Exact skills scan path (`.agents/skills/` vs `.claude/skills/`) — verify
  against current Agent Skills docs at scaffold time.

## 11. v0.1 scope

The tree above with its stubs (five memory files in house style, investigation
`_template/`, literature/meeting templates, Release READMEs, manuscript skeleton
compiling green), pre-commit + CI green on the shipped package, a sparse
`AGENTS.md`, two skills (`new-investigation`, `write-up`), `check_zones.py` at
grep level, and stub `export.sh`/`init.sh` carrying their spec in comments. No
framework tests yet. **Pilot:** run one real bounded investigation and one real
workbench→FINDINGS promotion through the skills; log what fought back; findings
return here as issues; v0.2 follows the evidence.

---

*Changes from the prior draft:* renamed STATE→**STATUS** and revived
**DECISIONS**; recast the memory files as an **epistemic hierarchy**
(canonical / provenance / coordination / unknowns / raw) replacing the
now/known/unknown rhythm framing; added the **promotion path** (workbench →
writeup → promotion PR) and sharpened P2 into "**agents open PRs; humans
merge**" — acceptance is the merge act, uniform across actors; QUESTIONS'
Resolved became a **layered routing index** (points at canonical records, never
raw provenance); FINDINGS provenance made **heterogeneous by design**; no
`findings/`/`writeups/` directory (second-use; writeups are notes); added the
**house style** (blockquote = editing contract, strictly), the **template
taxonomy** (instantiation vs runtime vs singleton; LICENSE excluded), and the
no-dev-branch decision; corrected the placement rule (agent-discovered files at
root, only invoked-by-path machinery in `.stemma/`).
