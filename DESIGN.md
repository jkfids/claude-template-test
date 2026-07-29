# DESIGN.md — Stemma: an AI-assisted research monorepo template

> **This is a logbook, not a specification.** The shipped files are the source
> of truth: `AGENTS.md` and the directory READMEs govern behaviour, and the root
> README's TO DO states what is currently unbuilt. Where this document disagrees
> with them, they win and it is stale. Read it for reasoning — why a choice was
> made, what was rejected, what is still open.
>
> Structural commitments are minimal and provisional; the repository's shape,
> including the investigation structure, is a working form to be settled by
> piloting against a real project. This file is a template-development artifact
> and does not travel into instantiated projects (§9): a project's own overview
> lives in `PROJECT.md`, its decision log in `research/DECISIONS.md`.

## 1. Purpose

A reusable monorepo template supporting the full research lifecycle — conception,
meetings, literature, theory, numerics, reusable software, manuscript, and public
release — with AI-assisted work as a first-class workflow rather than an add-on,
usable by collaborators who are not strong programmers.

Stemma is the layer that holds a project's state, evidence, and acceptance
rules — a control plane living in the repository itself. Everything around it
is a replaceable execution choice: the model, the agent tool that gives it
context and an action loop (Claude Code, Cursor, an IDE plugin), and the
surface a human steers from. Stemma does not choose models, construct context,
or run the agent loop; it defines what agents may do and what counts as
accepted, so a project can move between clients without changing its source of
truth.

Provider neutrality follows from two open standards carrying the portable
interface: `AGENTS.md` (read by most agent tools) for project instructions, and
the Agent Skills format (`SKILL.md`) for reusable procedures. Only genuinely
client-specific adapters live in a vendor directory (`.claude/`).

The neutrality is partial, and the seam is *location, not format*. The Agent
Skills spec defines what goes inside a skill directory but not where skill
directories live; `.agents/skills/` is a cross-client convention rather than a
requirement, and Claude Code discovers skills only under `.claude/skills/`.
`AGENTS.md` has the same shape of problem: Claude Code reads `CLAUDE.md`, not
`AGENTS.md`. So the canonical files stay portable and each client gets a bridge
— an `@AGENTS.md` import, and a symlink for skills. Both are currently shipped
in the template rather than generated at instantiation (§8), which is expedient
rather than principled. Verified: Claude Code does follow a symlinked
`.claude/skills`, so the bridge can stay a symlink and `.agents/skills/` remains
the single source. Symlinks make Unix the supported target; on Windows git
checks a symlink out as a text file containing its target path, which fails
invisibly.

Development loop: design the template here → instantiate it in a real project →
run real work through it → return findings → revise.

## 2. Principles

**P1 — The repository is the shared memory.** Agents are stateless; humans
forget; chat scrolls away. Durable state lives in the repo, where both humans
and agents read it. Agent work ends with a write-back (a diff); long-running
work keeps its own record. The repository — not a vendor memory feature — is
canonical, because only the repository is shared, reviewable, and exportable.
Durable state is also what makes agent workflows *testable*: a workflow whose
output is a diff can be asserted against.

**P2 — No conclusion enters canonical memory on conversational confidence
alone.** Agents produce plausible text faster than humans can check it. The
gate is not "who did the work" (nearly everything is AI-assisted) but *how
knowledge is accepted*: canonical entries arrive as reviewable diffs, and a
human performs the acceptance. Concretely: agents open PRs and never merge
them — **merging is the human acceptance act** (§5). Auto-merge is acceptable
only where the acceptance criterion is machine-checkable (dependency bumps on
green CI), which canonical knowledge never is.

**P3 — Second-use rule.** Add structure only after the need is felt twice. It
applies to files (DECISIONS was cut, then revived when a real category
emerged), directories (no `writeups/` until notes/ clutters), subdirectories
(`.stemma/` stays flat), branches (no dev branch — the zone/export model
already separates tooling from releases), and skills (ship few; bloated
instruction files measurably degrade agents). Contracts state bars; prompts
state formats; neither demands content whose value varies by entry ("rationale
where it isn't obvious", not mandatory fields). Going lean→structured later is
cheap; walking back unfilled structure is not.

**P4 — Friction scales with epistemic weight, not with actor or ceremony.**
Research is open-ended; the Research zone is frictionless by design, and
code-base change hygiene is not imposed on it. Strict hygiene (PRs, CI,
branch protection) belongs to the Release zone, where correctness is the bar.
In the Research zone there is exactly one gate — acceptance into canonical
memory (P2) — and everything before it is direct, ungated work. The
corollary is **readable over auditable**: the engaged researcher, not an
audit trail, is the integrity mechanism. Research documents are written to be
read; no file or section exists whose purpose is procedural rather than
scientific, because artifacts maintained dutifully rather than for a reader
train the eye to skim. Researcher ownership — steering the work, and
genuinely understanding what is accepted at merge — is what P2's gate relies
on, and it is a stated assumption of this design (§10).

## 3. Structure

Three zones, distinguished by what crosses the export boundary. The tree
below is the current working shape; the pilot may reshape it.

```
Release                              # ships with the paper
  README.md
  src/project_name/                  # real default name; init renames it
  tests/
  data/
  reproduce/
  manuscript/                        # self-contained TeX root (Overleaf/arXiv)
  ├── main.tex                       # replaceable default; swap in journal class
  ├── references.bib                 # shared bibliography; one citekey space
  └── figures/                       # generated by reproduce/; never hand-edited
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
  ├── investigations/
  │   ├── README.md                  # conventions + lifecycle
  │   ├── _template/                 # README.md, ANALYSIS.md, REPORT.md
  │   └── <short-title>/             # bounded dossier; branch-per, closed by PR
  ├── literature/      README.md     # per-source notes by citekey; template in README
  ├── meetings/        README.md     # one dir per meeting; template in README
  ├── notes/                         # logbook, writeups, working notes
  └── workbench/                     # scratch; promotable via writeup

Operations                           # shared control plane; not exported
  AGENTS.md                          # portable router (root: tool-discovered)
  CLAUDE.md                          # Claude adapter: @AGENTS.md import
  .agents/skills/                    # portable procedures (tool-discovered)
  .claude/                           # Claude adapter: permissions, skills bridge
  init.sh                            # run-once entry point (root: visible)
  .stemma/                           # managed framework machinery (§6)
```

**Placement rule:** if an external tool must *discover* it by scanning
conventional paths, it lives at root (`AGENTS.md`, skills, `.claude/`); if only
our own code invokes it by explicit path, it lives in `.stemma/`. Discovery
paths are per-client and not standardised (§1), so "at root" means the
canonical copy is at root and a client bridge points at it.

## 4. Project memory: the epistemic hierarchy

The research files are organised by *evidential status*, which tells a reader
(especially an agent) what to trust:

- **Canonical** — `FINDINGS.md` (what the project is prepared to rely on) and
`DECISIONS.md` (what it chose to do, and why). FINDINGS records truths;
DECISIONS records choices; each contract states the boundary from its side.
- **Provenance** — the evidence canonical entries cite: a closed investigation,
a writeup in `notes/`, a legible `workbench/` directory, or a citation key for
verified external results. Provenance is heterogeneous by design; the
canonical entry's link says which kind. A closed investigation is a
self-contained dossier: `README.md` carries the objective, scope, completion
criterion, and final state; `ANALYSIS.md` is the technical record sufficient
to understand, check, and reproduce the work; `REPORT.md` is the final,
self-contained account — FINDINGS provenance links land on the report.
While an investigation is active, everything in it is provisional; merging
its closing PR accepts the completed dossier as project provenance.
- **Coordination** — `STATUS.md`: current and queued tasks. A rough snapshot,
not evidence; rewritten, never appended. It may note active work but is not a
ledger of it — the open draft PRs are the registry.
- **Identified unknowns** — `QUESTIONS.md`: research-significant open questions,
phrased so an answer could be recognised. Questions resolve however the answer
arrives (investigation, promoted work, a decision, the literature); the
Resolved section is a routing index that points at the *most canonical record*
of the answer — never at raw provenance or PR numbers — and preserves original
phrasing so old uncertainties are not re-opened.
- **Raw** — `notes/`, `workbench/`, `meetings/`, and everything inside an
*active* investigation. Direct-commit, no ceremony; capture must stay
friction-free. Raw records may support a conclusion but are not canonical by
themselves.

**Investigations are organised by kind of knowledge, not by lifecycle
moment.** Each investigation directory holds three files with distinct roles:

- `README.md` — the control center: objective, scope, completion criterion,
  and current state. Concise, current, and high-level; a researcher or agent
  should grasp where things stand without reading the analysis.
- `ANALYSIS.md` — the living technical record: synthesis, derivations,
  figures, interpretation. Rewritten and reorganised freely as understanding
  improves; materially useful history, including negative results and dead
  ends, is preserved as content (a characterized dead end is a result).
  Structure is free — the file's organisation is the science's own.
- `REPORT.md` — the final concise account, completed when preparing the
  closing PR. Self-contained like a short scientific report, and the primary
  investigation artifact shared with collaborators. **No new science**: every
  claim must be supported by `ANALYSIS.md` or the artifacts it cites.

No fixed subdirectories for scripts, figures, data, or scratch are created by
default; an investigation adds supporting artifacts only when the work
requires them, organising them however suits. There is no chronological log
file: git history is the incidental chronology, and commit messages should say
what changed scientifically. Reusable code, manuscript changes, and other
release-facing artifacts follow their normal repository workflows rather than
being hidden inside the investigation dossier.

**Knowledge flows upward through a legible record.** A conclusion becomes
canonical only when something in the repo states the claim, its support, scope,
and caveats — and a human merges the PR entering it (P2). In v0.1 that record
is always an investigation's `REPORT.md`: everything routes through
investigations, and the closing PR is the only promotion path. The alternative
route — a self-contained writeup in `notes/`, drafted by a `write-up` skill and
promoted in its own PR — is deferred until small conclusions are seen to strand
with nowhere to go (§10). Conclusions with no repo evidence are staged as
notes, not filed as findings. SURVEY holds what the field established; FINDINGS
holds what this project established, including "we verified imported result X
in our regime".

**House style:** a `>` blockquote carries a file's *editing contract* (visible
to humans, distinct from content) and marks a genuine editing regime — gates,
rewrite-vs-append rules, close-and-recharter. HTML comments carry per-section
prompts (invisible when rendered, greppable); no placeholder body text; ISO
dates. Raw-tier instance templates (literature notes, meeting records) carry
prompts only — no blockquote, since a write-once raw file has no regime to
enforce. Documentation READMEs (Release, zone, directory) are plain prose, not
contracts. **Single ownership:** every convention has one owning file; other
files point at it, never paraphrase it.

## 5. Working assumptions (adopted for now, revisable after the pilot)

- **PRs, two tiers.** *Mechanical (path-based, branch protection):* `src/`,
`tests/` require a PR for anyone. *Convention (actor-based, in `AGENTS.md`):*
agents never commit those directly; agent edits to `manuscript/` are PRs while
human drafting is direct; each investigation closes with one PR; and entries to
`FINDINGS.md` or `DECISIONS.md` made by agent hands arrive by PR even when a
human asked — a human writing down a decision they have already taken commits
it directly, since the commit witnesses a choice rather than proposing a claim.
**Agents open PRs; humans merge them.** Everything else — notes, workbench,
STATUS/QUESTIONS/SURVEY housekeeping, literature, meetings, and all work inside
an active investigation — is direct commit.
- **Investigations are bounded by construction.** The charter test is: could
someone else tell when this is done? An investigation states an *objective*
and a *completion criterion*, and neither has to be question-shaped. Answering
a question qualifies; so does a characterization with stated uncertainty, a
decision-enabling comparison, "cannot be determined, because…", and — the case
that forced this wording — orientation work, where the objective is to
understand a topic and the criterion states the ground that must be covered.
What does not qualify is a criterion only its author can evaluate ("until we
feel we understand it"); that work stays in workbench/ or notes/ until a
recognisable endpoint crystallizes. Investigations mark *work, not intentions*:
they are created when substantive work begins, never automatically from
conversations or merely because a question exists.

  The lifecycle — charter, work, close — is deliberately light: one gate, at
  the end, where the human merges and the merge is the acceptance.
  `research/investigations/README.md` owns the steps; only the reasoning is
  here.

  The draft PR does the work a registry file would: it makes in-flight
  investigations visible on `main`'s pull request list, gives collaborators a
  place to comment mid-flight, and becomes the closing PR — so nothing enters
  `main` early and there is still exactly one merge.

  A closing PR should be confined to its own investigation directory and the
  directly affected memory files — no unrelated housekeeping, no other
  investigations, no release-facing implementation work. Investigation
  branches do not modify the Release zone: a needed `src/`/`tests/` change is
  edited and verified in place but committed on a separate branch off `main`
  through the normal PR lane, then `main` is merged — not rebased, since the
  branch is pushed with an open PR — back into the investigation branch. An
  investigation abandoned early with nothing established simply deletes its
  branch; one abandoned with something worth
  keeping closes normally, with a short report recording what was established
  and why work stopped.

- **Charter changes are consent-gated, not ceremony-gated.** There is no
amendment trail, no frozen charter, and no mid-flight visibility on main —
readable over auditable (P4). The protection is an actor rule in `AGENTS.md`:
**agents do not modify an investigation's objective, scope, or completion
criterion without the researcher's explicit go-ahead** — propose the change,
then wait. The researcher edits their own charter freely. A further duty —
noticing when incremental refinement has become replacement, since scope creep
is the failure mode neither party sees from inside — was drafted into
`AGENTS.md` and cut for length; whether its absence is felt is a pilot
question (§10).
- **Export is a fail-closed allowlist**; nothing in Release may depend on
anything not exported. This is the one silently-violated invariant — nothing
fails locally, CI stays green, and it surfaces only at export — and it is
currently enforced by nothing: `check_zones.py` is written but unshipped, on
the grounds that the pilot had no evidence to offer it. Its trigger is the
first Release file found referencing a non-exported path. Manuscript is a
self-contained TeX root: figures
are generated by `reproduce/` and committed to `manuscript/figures/` so it
compiles alone (Overleaf, arXiv submission).
- **Release READMEs** are templates: fixed conventions plus HTML-comment prompts,
written author-facing but reproducer-safe (the export audience vetoes
framework vocabulary), finalised at export. Soft on preferences (script
granularity), firm on invariants (figure destination, no non-exported imports).
They exist where a directory needs orienting — `data/`, `reproduce/` — not by
default: `manuscript/` ships source (`main.tex`, `references.bib`, `figures/`)
and no README, since LaTeX source explains itself to its reader and the export
would only delete it.
- **Linting follows the code, as an allow-list.** Ruff runs on `src/`,
`tests/`, and `reproduce/`; a new directory of Python is never linted until
deliberately added. This needs both halves — `include` in `pyproject.toml`
(governs `ruff check .` and editors) and `files:` on the pre-commit hooks (the
commit path): `include` does not constrain paths passed explicitly, and
pre-commit always passes them explicitly. The rule set favours correctness
over style, since the formatter owns layout: `E4/E7/E9` rather than all of
`E`, and `E501` omitted because it cannot be autofixed for comments, URLs, or
strings. Safety hygiene (large files, private keys, merge conflicts, TOML
validity) stays repo-wide — the ungated research lane has no human backstop,
so it needs machine hygiene most — while *cosmetic* hygiene is the friction P4
warns about and is scoped away from `research/` before release. Line endings
are normalised by `.gitattributes` (`* text=auto eol=lf`), not by a
commit-time hook. Content-rewriting formatters (pyproject-fmt) never run on
template files (they mangle placeholders); commented in config with a
do-not-enable-until-instantiated warning.
- Conventions from day one: one-sentence-per-line LaTeX; environments from
`pyproject.toml` alone; figures only from `reproduce/`; one citekey space
across `literature/`, investigations, and `manuscript/`, generated by the
reference manager and never hand-edited. Owners, per single ownership: figure
destination → `reproduce/README.md`; bibliography and citekey provenance
(keys come from the bibliography; never invent one) → `literature/README.md`;
the never-hand-edit rule → `AGENTS.md`. Source PDFs are untracked
(`research/literature/**/*.pdf`) — the notes are the durable record, not the
papers they distil. The LaTeX conventions have **no
traveling owner** since `manuscript/README.md` was dropped — a known gap, with
a comment header in `main.tex` or an `AGENTS.md` line as candidates (§10).
- **Deferred with named triggers** (second-use rule): a chronological
`LOG.md` returns if session-level history proves to have no home or the
analysis bloats with it; a curated "investigation record" section inside
ANALYSIS is the preferred reinstatement form. A `render_report.sh`
(pandoc-based md→PDF for REPORT.md, stripping the contract blockquote) is
built when the shareable PDF is wanted in practice, not before. Fixed
section skeletons for ANALYSIS and REPORT (paper-style numbered sections,
verification checklists) were drafted and set aside; they return
section-by-section as the pilot shows each earns its place.

## 6. Framework layer: `.stemma/`

Stemma is a framework the project keeps and updates (copier-style), not an
agent runtime and not a scaffold it deletes. Agent tools consume its
`AGENTS.md`, skills, and client adapters; `.stemma/` holds the deterministic
machinery they invoke. The dotdir signals *managed machinery — run it, don't
hand-edit it*: agents run its scripts when asked (export, checks) but do not
modify its internals in an instantiated project.

```
.stemma/
  init/                # instantiation templates, rendered once at init:
    README.md          #   → root README.md (project/companion README)
    CITATION.cff       #   not yet written
  README.md            # not yet written — the framework's own readme
  export.sh            # not yet written — Release → fresh repo; verify
  check_zones.py       # not yet written — Release must not depend on
                       #   non-exported paths
  tests/               # not yet written — TEMPLATE-REPO-ONLY (§9)
```

Only `DESIGN.md` and `init/README.md` exist; the root README's TO DO is
authoritative on what is unbuilt.

Flat until the script count warrants subdirectories. **Template taxonomy —
form follows instance shape:** *instantiation templates* (rendered once) live under
`.stemma/`; *runtime templates* live in place in `research/`, editable as the
project's methodology evolves, in two forms — multi-file instances ship a
`_template/` directory (investigations), while single-file instances embed
their template in the directory's README (literature notes, meeting records);
*singleton stubs* (the memory files) ship as the files themselves, structure
and prompts baked in. LICENSE is none of these — a canonical legal text
`init.sh` selects and stamps (copyright line only), never a hand-maintained
skeleton (legal-text drift is not "close enough").

**Agent instruction, three tiers:** `AGENTS.md` the sparse router; then skills,
the procedures; then `.claude/`, the vendor remainder. Facts sort by scope:
everywhere → AGENTS.md; named-task procedure → skill; this-directory-only →
its README; and each memory file's own contract governs itself.

No Stemma-native skill has been written. `new-investigation` was the intended
first — artifact-producing, hence world-state-testable (§7) — but chartering by
hand during the pilot is what will show which parts want automating. What ships
instead is four third-party skills vendored unmodified, which tests the skills
*mechanism* without committing to a procedure. `.claude/` holds only the skills
symlink; its other candidate jobs (merge permissions, disabling client-side
memory) wait on evidence.

`AGENTS.md` shipped at ~70 lines: a framing line, a two-file entry point, the
three zones with their export boundary and links to the owning READMEs, the
always-apply rules, two commands, and a closing principle. `AGENTS.md` itself
is authoritative for the current rules; what follows is why it has the shape it
does.

- **No repository tree, and no general theory of precedence.** Both were
drafted and cut. Directory layouts are discoverable, and the available evidence
is that instruction files do not function as repository overviews; what stays is
what an agent cannot infer, which is *policy* (what is exported, what may depend
on what) rather than *layout*. Precedence prose resolves conflicts that
shouldn't exist between files with one author, and would not reliably resolve
them anyway.
- **Every prohibition carries its action.** A bare "don't" makes agents
conservative and exploratory; the paired form is what makes the rule usable.
Rationale is kept only where it helps an agent generalise to a case the rule
didn't anticipate ("the merge is acceptance" forecloses clever equivalents),
and cut where the instruction is already complete.
- **Commands earn their place by being non-obvious.** `pytest` and
`pre-commit` are guessable and left out. `gh pr list --draft` is in because the
draft-PR registry (§5) exists nowhere an agent would look — `STATUS.md` says
outright that it is not a ledger of active work.
- **Rules 1 and 2 are the load-bearing ones, and they live in the softest
layer.** Instruction files are context, not enforcement; a client can be told
not to merge but not thereby prevented from merging. Durable enforcement is a
client permission rule, which is a job for `.claude/` once the pilot shows it
is needed.

## 7. Testing

- **Project code** — `ci.yml` (travels): install `.[dev]` across a small Python
matrix (floor and current — a research project runs on one interpreter, and
wide matrices are a library posture), pytest, plus `pre-commit run --all-files`
as the unbypassable enforcement copy of the hooks. The template ships a working `project_name` package and smoke
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
must leave*. For investigations, deterministic checks can assert that the
dossier's README contains a recognisable objective and completion criterion,
that an
open draft PR exists while the investigation is active (the registry, and
queryable via the API), that `REPORT.md` is non-empty when the PR is marked
ready, and that its changed paths are confined to the investigation's own
directory plus the affected root memory files. P1's payoff is that
output-is-a-diff makes these workflows testable without an LLM judge.

## 8. Instantiation

The template ships as a working package `project_name` (import) /
`project-name` (distribution) so it builds pre-instantiation. `init.sh` is a
stub; instantiation is by hand for now, which is the spec's dry run. The spec
follows, since the stub no longer carries it.

1. **Gather** — project name, description, author name/email, org/user;
   defaults from the directory name and `git config user.name`/`user.email`.
   Support a non-interactive form (`PROJECT_NAME=… ./init.sh --yes`) so the
   instantiation test (§7) can drive it.
2. **Derive and validate** — hyphen form (distribution) and underscore form
   (package) are *different strings*, substituted separately, longest-first.
   Validate that the underscore form is a legal Python identifier and the
   hyphen form a legal PEP 508 name: a wrong-but-consistent rename is the one
   failure CI cannot catch.
3. **Rename** — in `pyproject.toml`: `name`, `packages`, the dynamic-version
   path to `__about__.py`, `authors`, `description`, `[project.urls]`. On disk:
   `git mv src/project_name/`. In `tests/test_smoke.py`: the import.
4. **Render** — `.stemma/init/README.md` → root `README.md`, substituting
   `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, `{{AUTHOR}}`, `{{ORG}}`. Likewise
   `CITATION.cff` and a stamped LICENSE when those templates exist; until they
   do, the rendered README links to two files that will not be there.
5. **Delete** the template-only paths (§9) — including itself.
6. **Environment** — `pip install -e ".[dev]"`, then `pre-commit install`.
7. **Verify** — grep for surviving `project_name`, `project-name`, `{{…}}`;
   warn loudly rather than failing silently.
8. **Report** — fill `PROJECT.md`; review `pyproject.toml`; enable branch
   protection on `src/`/`tests/`; commit; read `research/README.md`.

Prefer `python3` over `sed` for the substitutions: user input contains slashes,
ampersands, and quotes, and `sed -i` differs between GNU and BSD. Since the work
is mostly string handling and validation, the implementation is likely Python
despite the `.sh` name.

Instantiation configures the research project, not a permanent AI stack. It
does not pin a model, agent tool, or work surface: those remain user- and
task-level choices. Client adapters may be detected or generated — currently
they are shipped in the template instead (§1) — but canonical rules stay in the
portable layer and personal credentials stay outside the repository.

## 9. Template-only vs travelling

One rule: **does a researcher *using* the framework need it, or only someone
*developing* it?** Travels: `.stemma/` tools and their docs; all zone content
and stubs. Template-repo-only: `DESIGN.md`, the template's root README,
`.github/assets/` (the Stemma logo — note `.github/workflows/` travels),
`.stemma/init/` (instantiation templates, consumed at init), `.stemma/tests/`,
and `init.sh` itself. So `.stemma/` travels *except* `init/` and `tests/`.
This list is authoritative and `init.sh` implements it; the previous arrangement
kept a second copy in the stub's comments and the two drifted within days.

## 10. Open questions (for the pilot)

- v0.1 routes **everything through investigations** — `write-up` is deferred,
so the closing PR is the only promotion path. Does that hold, or do small
conclusions strand with nowhere to be promoted (the trigger to build `write-up`
and the `notes/` writeup route)? Does the humans-merge rule hold?
- **The ownership assumption:** the frictionless investigation model assumes an
engaged researcher steering the work — that is its integrity mechanism (P4).
If an investigation runs in low-touch mode, does the objective drift without
anyone noticing? Does close-time review alone suffice to catch it?
- Does the investigation README stay a concise control center, or drift into
duplicating the analysis? Does ANALYSIS hold its boundary with the README?
- Does free-form ANALYSIS/REPORT structure stay reviewable and readable, or
do closing PRs turn out to need fixed sections (verification, limitations)
back?
- Does REPORT's self-containment drift into disagreement with ANALYSIS
(the same result stated twice, diverging)? Does the no-new-science rule
survive real closes?
- Is the absence of a chronological log ever actually felt (session history
with no home; analysis bloating with narrative)?
- Does the draft PR work as the registry — do collaborators actually find and
comment on in-flight investigations there, and does the draft survive to become
the closing PR rather than being opened late?
- Does DECISIONS fill, or was its revival premature? Does QUESTIONS' Resolved
section fill (working) or stay empty while Open grows (graveyard → fold into
STATUS)?
- Does STATUS stay a snapshot, or drift into a backlog that GitHub Issues
should hold? Does its Summary stay current, or does an inline why-per-task
prove more self-maintaining?
- Is `workbench/` used, or does routing everything through investigations
absorb it — the trigger to drop it from the instantiated template?
- Skills across surfaces; progressive disclosure; whether `new-investigation`
alone suffices, or `add-source` and a meeting routine earn their place.
- Does the completion-criterion framing hold for orientation work — do survey
investigations state a criterion someone else can evaluate, or drift back to
"until we feel done"?
- Does the absence of the scope-creep duty (cut from `AGENTS.md` for length,
§5) get felt — does an agent refine an objective into a different one without
anyone saying so?
- Framework model: do projects actually `copier update`, or drift?
- Literature wiring (reference manager/MCP); grep-level vs AST-level zone check;
lockfiles (uv); Issues vs STATUS for tasks; data at scale (DVC/Zenodo);
non-coder entry points; the md→PDF render path for reports.
- Do the LaTeX conventions (one-sentence-per-line, self-contained TeX root)
need a traveling home, or does the manuscript's own shape teach them?
- Does the portable extension layer work across clients without duplicated
policy? The format is portable and the location is not (§1). Answered so far:
Claude Code follows a symlinked `.claude/skills`, so one symlink suffices for
that client. Open: whether a second client needs more than a symlink, and
whether the bridge should ship in the template or be generated at init.
- Vendored third-party skills have no pinned upstream commit, so a local edit
and an upstream release are indistinguishable. Two of four drifted within days
of vendoring. Does a provenance record earn its place, or is re-pulling
deliberately before each investigation enough?
- Client-side memory features write an unreviewed record outside the
repository, parallel to the one this design makes reviewable (P1, P2). Disable
by default in `.claude/`, or does it prove useful enough to keep and ignore?

## 11. v0.1 scope

Shipped: the tree above with its stubs (five memory files plus `PROJECT.md`
in house style; the zone README as map and gate; investigation `_template/`,
deliberately minimal — contract blockquotes plus prompts, structure otherwise
free; literature and meeting templates embedded in their directory READMEs;
Release READMEs for `data/` and `reproduce/`; a manuscript skeleton compiling
standalone), pre-commit + CI green on the shipped package, `AGENTS.md` (§6),
`CLAUDE.md` importing it, and four vendored third-party skills.

**The root README's TO DO is authoritative on what is unbuilt.** What follows
is only why, since status drifts and reasoning does not. Almost everything
deferred shares one criterion — *the pilot cannot exercise it, so building it
returns no evidence*: `check_zones.py` (written but unshipped; trigger in §5),
`new-investigation` (chartering by hand shows what wants automating),
`add-source` (its shape depends on how literature intake settles, so building
it first means building it twice), `.claude/` contents beyond the symlink,
framework tests, and `init.sh` — where instantiating by hand is itself the
spec's dry run. No log file, no render script, no fixed report skeleton, no
`write-up`: each has a named trigger (§5, §10).

**Before tagging v0.1:** implement `init.sh` against §8; write `export.sh`,
without which the export boundary is a claim rather than a mechanism; add the
`LICENSE` and `CITATION.cff` templates the rendered README already links to;
scope the cosmetic hygiene hooks away from `research/` — deferred so the
template's own files stay clean while it is the product; and fill the root
README's empty sections with one concrete end-to-end walkthrough, written
*from* the pilot rather than before it.

**Pilot:** run one real bounded investigation end to end — charter, draft PR,
literature, analysis, report, merge, FINDINGS and QUESTIONS updates. Log what
fought back; findings return here as issues; v0.2 follows the evidence. The
next useful information about this design comes from using it, not from
extending this document.

---

*Changes from the prior draft.* **Status.** Demoted to a logbook: the shipped
files govern, and the root README's TO DO — not §11 — is authoritative on what
is unbuilt. §11 keeps only the reasoning. Two overlapping status paragraphs in
the header merged into one.

**Investigations.** The charter test no longer requires a question. An
investigation states an **objective** and a **completion criterion**, and
orientation or survey work qualifies when the criterion states the ground to be
covered. The prior framing — "could you recognise an answer if you saw one",
with anything else sent to `notes/` — would have disqualified the pilot's own
first investigation. Vocabulary changed throughout: *answer criterion* →
*completion criterion*, *question* → *objective* where the charter is meant
(§4, §5, §7). The restart trigger is a changed objective, not a changed scope.
The lifecycle steps were cut from §5, which was restating what
`investigations/README.md` owns.

**Agent instruction.** `AGENTS.md` shipped; §6 now records why it has the shape
it does rather than specifying it. Provider neutrality is qualified: the skills
*format* is portable, the *location* is not, and Claude Code is confirmed to
follow a symlinked `.claude/skills` (§1, §10). Instruction files are context
rather than enforcement, so the never-merge rule's durable form is a client
permission rule (§6). No Stemma-native skill was written; four third-party
skills ship vendored instead, which tests the mechanism without committing to a
procedure.

**Corrections.** `check_zones.py` was described as enforcing the export
invariant; it does not exist, and §5 now says so and names its trigger. Ruff's
scope is `src`, `tests`, `reproduce`. `DESIGN.md` moved to `.stemma/`, and §9
now carves it out of the travelling set. The `init.sh` spec moved from the
stub's comments into §8 — the two copies had already drifted, which is the
argument for one owner.
