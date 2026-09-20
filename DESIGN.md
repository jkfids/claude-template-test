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

Stemma keeps research state, evidence, and acceptance rules in a repository
that humans and agents can share. The model and client are replaceable. The
full layout fits a paper with supporting code; a library or existing project
may adopt only the useful pieces.

## 2. Attention is the constraint

Human reading time and agent context are both limited. Every paragraph, rule,
and file creates a maintenance obligation. Optimize for useful information per
unit of attention, not for procedural completeness or minimum word count.

- Write what helps a reader act, understand a result, or assess its limits.
  Remove commentary about the writing process and the template's evolution
  from files that travel into projects. Design history belongs here.
- Preserve scientific substance: assumptions, definitions, reasoning, negative
  results, and uncertainty. Compress framing, repetition, and routine algebra.
- Give each rule one owner. Other files link to it. Keep always-loaded agent
  instructions short; load task-specific material when needed.
- Add structure after a repeated need. Prefer updating an existing record to
  adding another log, checklist, index, wrapper, or skill.
- State the current procedure directly. Do not accumulate explanations of
  earlier versions, unused alternatives, or compatibility paths for old clients.

This applies to this logbook too: retain consequential rationale and evidence,
not a transcript of each editing pass.

## 3. Ownership

| Concern | Owning record |
| --- | --- |
| Zones, acceptance, agent boundaries | `AGENTS.md` |
| Installation and verification commands | `CONTRIBUTING.md` |
| Memory routing and handoffs | `research/README.md` |
| Editing regime for a memory file | Its opening blockquote |
| Investigation lifecycle | `research/investigations/README.md` |
| Source-note conventions | `research/literature/README.md` |
| Figure generation and reproducibility | `reproduce/README.md` |
| Input provenance and retrieval | `data/README.md` |

Blockquotes carry editing contracts; HTML comments prompt content. Avoid
requiring fields whose value varies by entry. Template bodies remain empty
until a project has something to record.

## 4. Shared memory and acceptance

The repository is the durable, reviewable record. Client memory may help an
individual resume work, but cannot be the only source of project context.
`PROJECT.md` defines purpose and scope; `STATUS.md` identifies current work,
review state, and next steps. Neither is a transcript or evidence ledger.

`FINDINGS.md` records accepted claims; `DECISIONS.md` records accepted choices.
Entries point to readable evidence, including notes, reports, or verified
literature. A human accepts an agent's proposed entries by merging their PR.
Compilation, numerical agreement, and polished prose are useful checks, not
substitutes for scientific review.

Capture stays lightweight. A self-contained note can support acceptance
without being retrofitted into an investigation. Handoffs update existing
records and distinguish accepted work from provisional drafts. A separate
manuscript draft is a researcher choice, not a default directory convention.

## 5. Investigations

A charter makes work bounded: another researcher must be able to recognize its
endpoint. Objectives can include a derivation, comparison, characterization,
or survey; they need not be question-shaped. The researcher controls scope.

The three files serve distinct readers: README for coordination, ANALYSIS for
checking the work, REPORT for the final account. REPORT introduces no new
science. Supporting artifacts have no mandatory directory structure.
A draft PR exposes active work and becomes its acceptance PR.

Separate worktrees keep release implementation out of investigation changes
and avoid switching a checkout another session is using. Small notes and
Operations edits do not need the same ceremony as scientific acceptance.

## 6. Clients and skills

Target current clients. `AGENTS.md` is shared by Codex and supported Claude
sessions; setup guidance links to Claude's conditional discovery rules. The
`CLAUDE.md` import added no project information and was removed. Skill discovery
is a separate concern: `.claude/skills` links to `.agents/skills` so there is
one editable copy. Unix symlinks remain a portability constraint.

Check client behavior against primary documentation when changing this setup:
[Claude instructions](https://code.claude.com/docs/en/memory),
[Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude skills](https://code.claude.com/docs/en/skills),
[Codex skills](https://learn.chatgpt.com/docs/build-skills), and the
[Agent Skills format](https://agentskills.io/specification).
These were checked during the September 2026 review.

Keep repository-specific procedures local; obtain general tools from personal
collections or plugins where practical. Vendored skills need license and
upstream provenance. Start updates from current upstream, preserving its
entrypoints, references, and helpers; reapply only justified local fixes.
References load on demand, so deleting them does not inherently save context.

The bundled skills are `liteparse`, `paper-lookup`, `scientific-visualization`,
and `sympy`, pinned to upstream revision `330c8e7` in their metadata. Local
changes address pager redaction and completeness, sparse abstract indexes,
current OpenAlex and LiteParse behavior, batch output collisions, runnable
plotting/math examples, and mathematical assumptions. Citation suggestions
follow the reference-manager workflow instead of editing generated bibliographies.
Licenses are retained. These skills are replaceable conveniences, not intrinsic
template functionality. Check local changes when updating them; ongoing skill
test suites belong upstream.

`skill-creator` was a large client-specific development toolkit;
`verification-before-completion` duplicated contribution guidance. Both were
removed from the template. Avoid adding a catalog or orchestrator merely because
it is available. Instruction files express policy; hosting permissions and required
reviews provide enforcement.

## 7. Build and release

Hatchling is the default backend, with explicit wheel and sdist contents and a
literal `__version__` read from the package without importing it. `corrqec2` v3
informs package scope and dependency organization, but its setuptools backend
reflected an older starting configuration rather than a new template preference.
No separate version module, VCS plugin, or environment orchestrator is required.

Development tools use [standard dependency groups](https://packaging.python.org/en/latest/specifications/dependency-groups/);
extras are reserved for user-installable package features. Pip is sufficient;
uv offers convenient project locking. Research projects should record their
resolved environment, while package CI also checks fresh compatible dependencies.
A template lockfile would freeze placeholder choices before a project has its
scientific dependencies. Python 3.12 is the compatibility floor; 3.14 is the
current stable development target, avoiding a prerelease dependency requirement.

The September 20 review checked PyPI and upstream releases: Hatchling 1.32.3,
Ruff 0.16.8, pytest 9.1.1, pre-commit 4.6.2 and build 1.6.1. Build/dev dependencies
have lower bounds; Ruff is pinned to match its hook so formatting agrees.
Configuration keeps compact Stemma banners and a few actionable optional tools.
See [Hatch file selection](https://hatch.pypa.io/latest/config/build/),
[version sources](https://hatch.pypa.io/latest/plugins/version-source/regex/), and
[uv environment locking](https://docs.astral.sh/uv/concepts/projects/sync/).

A package archive and a paper release serve different purposes. The sdist and
wheel contain package/build material; data, reproduction scripts, and manuscript
belong to the paper release. Inspect actual archives and test a wheel rebuilt
from the sdist. The September build check confirmed those contents and installation;
it is not a guarantee against future build-configuration changes.

The public repository boundary is still unenforced. Publishing the working
repository would publish its tracked research. A future exporter should use an
allow-list and verify the release without private files or sibling checkouts.
It must make an explicit choice about release history rather than assuming a
package configuration filters GitHub archives.

Ruff follows an allow-list in both `pyproject.toml` and pre-commit: hooks pass
explicit paths, so both filters matter. Cosmetic hooks spare research records;
safety checks remain repository-wide.

## 8. Instantiation

Manual setup is documented in the root README; `init.sh` is a stub. An initializer
should automate a settled manual workflow, accept noninteractive arguments,
validate distribution and import names separately, and test its output in a
temporary directory. Rename package paths, metadata, and both names in the smoke
test. Render the project README and remove template-only material (§9).

Do not silently choose a license or rewrite scientific memory. Configure a
project, not a permanent model or agent stack. An instantiation test should
check for surviving placeholders, install/build the result, and run its tests.

## 9. Template-only vs travelling

Template-only: this `DESIGN.md`, the root template README, `.github/assets/`,
`.stemma/init/`, `.stemma/tests/`, and `init.sh`. Replace the
root README with the project README. Other zone content and runtime tooling
travel with the project; only Release material is intended for publication.

## 10. Pilot evidence and next questions

The September 2026 tour inspected these local snapshots:

| Project | Revision | Useful evidence |
| --- | --- | --- |
| `memory-aware-rb` | `9ead6dab2bf1` | Technical literature notes, accepted memory, provisional dossiers, active manuscript pointers. |
| `process-tensor` | `bb3b76e43c9e` | Contribution guidance, PR evidence, focused package contents. |
| `corrqec2` v3 | `96f38ae644b1` | Lean build configuration, pinned Git dependency, archived data versus cluster reruns. |
| `corrqec2-dev` | `b19dbbe98883` | Development counterpart, not an independent template pilot. |

`memory-aware-rb` is the direct workflow pilot. Its literature conventions
retain enough technical detail to use results without reopening PDFs, while
keeping project relevance tentative. Its status file separates accepted
findings from unreviewed dossiers and manuscript variants. Those observations
support richer content prompts, not more memory files. The other repositories
support partial adoption and explicit reproduction environments. This was a
workflow review, not verification of their scientific results.

Priorities beyond the root README's implementation gaps:

- Can another researcher or client resume work from the same compact records?
- Do standalone notes stay reviewable as provisional drafts accumulate?
- Automate chartering or source ingestion only when repeated use establishes a
  useful procedure and a checkable output.

Report rendering is a single `.stemma/md2pdf.py` command using Pandoc and
LuaLaTeX. These handle scientific Markdown without a parallel renderer, style
package, or Python dependency. An opening blockquote is always treated as an editing
contract and omitted; files without one still render and later quotes remain.
Source files are never rewritten. Tests and a rendered specimen cover math,
tables, figures, footnotes, and failed-build preservation.
