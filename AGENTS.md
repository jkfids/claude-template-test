# AGENTS.md

An academic research project: literature, theory, analysis, code, and manuscript.
Not every task is a coding task.

## Start here

Read [PROJECT.md](PROJECT.md), then [research/STATUS.md](research/STATUS.md).
Check the branch, worktree, and uncommitted changes before editing; preserve
work left by the researcher or another session.

## Where to work

- **Release:** `src/`, `tests/`, [data/](data/README.md),
  [reproduce/](reproduce/README.md), `manuscript/`, packaging, and CI.
  Nothing here may depend on files excluded from release.
- **Research:** `PROJECT.md` and [research/](research/README.md).
  Private working records and project memory; excluded from release.
- **Operations:** agent instructions, `.agents/`, `.stemma/`, and client config.
  Excluded from release. Run `.stemma/` tools rather than reimplementing them;
  do not modify their internals without permission.

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and checks, and
[research/README.md](research/README.md) for evidence and handoffs.

## Rules

- Release changes, investigations, and canonical claims require PRs. Small
  changes to Operations and provisional notes may be committed directly.
  Agents open and update PRs; never merge them or enable auto-merge.
  A human merges; the merge is acceptance.
- Do not change an investigation's objective, scope, or completion criterion
  without the researcher's approval. Propose the change and wait.
- Investigation branches do not modify Release. Follow the
  [investigation workflow](research/investigations/README.md).
- Do not edit `manuscript/references.bib`; a reference manager generates it.
  Citekeys come from that bibliography. See [literature guidance](research/literature/README.md).
- Unreviewed notes, drafts, and agent output are provisional. Accepted claims
  and choices live in `research/FINDINGS.md` and `research/DECISIONS.md`.
- Follow each memory file's opening contract; do not edit it.
- Write for the reader's next action. Keep rules in one place and link to them.
  Omit editorial history and procedural commentary unless needed to interpret
  the research.

## Investigation registry

```bash
gh pr list --draft
```
