# Stemma

> **Status:** v0.1: Under active development; conventions are still settling.

A monorepository template for AI-assisted academic research, supporting the full project lifecycle—literature, proofs, numerics, reproducible results, and manuscript writing. Stemma is built around reusable agent workflows, emphasizing rigorous verification and flexible collaboration. It is designed to fit within a wider software stack, including AI tools, reference managers, and communication platforms.

## In practice

## Repository overview

The repository is divided into three zones. **Release** contains standard package files and everything slated for public release alongside a paper: code, data, figures, and manuscript source files. **Research** is the scientific and exploratory core—literature, investigations, and persistent project memory. **Operations** contains the agent instructions, workflows, and general tools for running the repository.

```text
Release
  README.md
  src/project_name/
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
  ├── SURVEY.md
  ├── investigations/
  ├── literature/
  ├── meetings/
  ├── notes/
  └── workbench/

Operations
  AGENTS.md
  CLAUDE.md
  .agents/skills/
  .claude/
  init.sh
  .stemma/

```

### Release
- **`src/`** – Durable, tested code in standard package layout.
- **`tests/`** – Unit, integration, and end-to-end tests for **`src/`**.
- **`data/`** – Main data associated with the manuscript. Large datasets are recommended to be stored outside the repository.
- **`reproduce/`** – Scripts for reproducing the manuscript's results and figures.
- **`manuscript/`** – LaTeX source for the manuscript.
- Configuration files: **`pyproject.toml`** (packaging), **`.pre-commit-config.yaml`** (commit checks), **`.github/workflows/ci.yml`** (continuous integration).

### Research
- **`PROJECT.md`** – General project overview, motivation, and context.
- **`STATE.md`** – Current project snapshot: in-progress and immediate goals.
- **`FINDINGS.md`** – Established results and dead ends accumulated throughout the project.
- **`SURVEY.md`** – Overview of the relevant literature and its relation to the project.
- **`investigations/`** – Agent-led scientific investigations, with one directory per bounded investigation.
- **`literature/`** – Per-paper notes: theory, methods, and results.
- **`meetings/`** – Records and summaries of project meetings.
- **`notes/`** – Researcher logbook and working notes.
- **`workbench/`** – Scratch space for researcher-led exploration and analysis.

### Operations
- **`AGENTS.md`** – The main entry point and router for agents. **`CLAUDE.md`** points here.
- **`.agents/skills/`** – Reusable agent instructions and workflows (`SKILL.md` files).
- **`.claude/`** – Claude Code configuration: slash commands and subagents.
- **`init.sh`** – Sets up the template as a new project (runs once).
- **`./stemma`** – Framework scripts, docs, and tooling (export, checks).

## Quickstart


## How to use
