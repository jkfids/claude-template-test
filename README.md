<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.svg">
    <img alt="Stemma" src=".github/assets/logo-light.svg" width="420">
  </picture>
</h1>

> **Status:** pre-v0.1; conventions are still settling.

A monorepository template for AI-assisted academic research, supporting the
full project lifecycle—literature, theory, numerics, reproducible results, and
manuscript writing. Stemma is built around reusable agent workflows, emphasizing
rigorous verification and flexible collaboration. It is designed to fit within a
wider software stack, including AI tools, reference managers, and communication
platforms.

## TO DO
- `init.sh` is a stub—instantiate by hand or via AI.
- No `.stemma/` scripts. `export.sh` is unwritten, so the export boundary has
  no mechanism, and nothing checks that Release avoids non-exported paths.
- No framework tests: instantiation, export safety, agent world-state.
- No Stemma-native skills. `new-investigation` is unwritten; the four installed
  skills are borrowed and vendored unmodified.
- `.claude/` holds only the skills symlink. Without `settings.json`, the
  never-merge rule is convention rather than enforcement.
- No `LICENSE` or `CITATION.cff`, and no templates for them in `.stemma/init/`
  — the rendered project README already links to both.
- No reference manager wired up, so `manuscript/references.bib` is unmanaged.
- Cosmetic pre-commit hooks still run on `research/`.
- This README is incomplete: *In practice*, *Quickstart*, and
  *How to use* will be written for v0.1.
- Poor Windows compatibility.

## In practice

## Structure

The repository is divided into three zones.

**1. Release**\
Standard package files and everything slated for public release alongside a
paper: code, tests, data, reproduction scripts, and manuscript source.

**2. Research [[`README`](research/README.md)]**\
The scientific and exploratory core: literature, investigations, and persistent
project memory. Never exported, and nothing in Release may depend on it.

**3. Operations**\
Agent instructions, workflows, and the tooling for running the repository.

```text
Release
  README.md
  src/project_name/                # Reusable, tested package code
  tests/
  data/                            # Manuscript data; large sets live outside
  reproduce/                       # Scripts producing results and figures
  manuscript/                      # LaTeX source
  pyproject.toml                   # Packaging
  .pre-commit-config.yaml          # Commit checks
  .github/workflows/ci.yml         # Continuous integration
  .gitattributes
  .gitignore
  (CITATION.cff)  (LICENSE)        # Added before public release

Research
  PROJECT.md                       # Durable definition of the project
  research/
  ├── README.md                    # Zone map
  ├── STATUS.md                    # Rough snapshot: current tasks
  ├── FINDINGS.md                  # Canonical scientific knowledge
  ├── DECISIONS.md                 # Project-level choices + rationale
  ├── QUESTIONS.md                 # Unresolved questions
  ├── SURVEY.md                    # Literature synthesis
  ├── investigations/              # Bounded units of research
  ├── literature/                  # Per-source notes by citekey
  ├── meetings/                    # Meeting records
  ├── notes/                       # Logbook and working notes
  └── workbench/                   # User-led scratch workspace

Operations
  AGENTS.md                        # Entry point and router for agents
  CLAUDE.md                        # Points at AGENTS.md
  .agents/skills/                  # Reusable agent workflows (SKILL.md)
  .claude/                         # Claude Code config
  init.sh                          # Sets up the template as a new project
  .stemma/                         # Framework layer: scripts, templates, tools
```

## Quickstart


## How to use
