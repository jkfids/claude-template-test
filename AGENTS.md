# AGENTS.md

An academic research project kept end to end in one repository: literature and
investigation records, project memory, analysis code, and the manuscript. Not
every task is a coding task.

## Start here

Read [`PROJECT.md`](PROJECT.md), then
[`research/STATUS.md`](research/STATUS.md). Follow the links below for anything
more specific.

## Zones

**1. Release** – The public package and paper: `src/`, `tests/`, `data/`,
`reproduce/`, `manuscript/`, and the packaging and CI config. Nothing in this
zone may depend on anything that is not exported.

- [`manuscript/main.tex`](manuscript/main.tex) – The project's central
  artifact and the paper's entry point.
- [`data/README.md`](data/README.md) – Input data; large sets live externally.
- [`reproduce/README.md`](reproduce/README.md) – Scripts regenerating results
  and figures.

**2. Research** – `research/` and [`PROJECT.md`](PROJECT.md): private working
knowledge and project memory. Never exported.

- [`research/README.md`](research/README.md) – Zone map: memory files and
  working directories.
- [`research/investigations/README.md`](research/investigations/README.md) –
  Investigation conventions and instructions.
- [`research/literature/README.md`](research/literature/README.md) – Citekeys
  and per-source notes.
- [`research/meetings/README.md`](research/meetings/README.md) – Meeting
  records.

**3. Operations** – This file, `CLAUDE.md`, `.agents/`, `.stemma/`, and client
configuration. Not exported.

- `.agents/skills/` – Reusable agent procedures.
- `.stemma/` – Framework scripts: run rather than reimplement; do not modify
  without permission.

## Always apply

- Open and update pull requests; never merge them. A human merges, and the
  merge is acceptance.
- Do not change an investigation's question, scope, or completion criterion
  without the researcher's approval. Propose the change and wait.
- Investigation branches do not modify the Release zone. Branch such changes
  from `main` as their own pull request.
- Do not edit `manuscript/references.bib`; a reference manager generates it.
  Never invent a citekey.
- Do not treat unreviewed notes, analyses, or your own output as accepted
  knowledge. Canonical claims live in `research/FINDINGS.md` and
  `research/DECISIONS.md`.
- Follow a memory file's opening blockquote; do not edit it.
- When writing documentation, link to instructions that exist elsewhere rather
  than copying them.

## Commands

```bash
gh pr list --draft  # In-flight investigations: this is the registry
git diff --name-only main...HEAD  # Confirm a branch is confined to its own scope
```

## Working principles

Prefer the smallest change that completes the task at hand. Show your working,
keep uncertainty visible, and leave consequential decisions to the researcher.
