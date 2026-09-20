<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.svg">
    <img alt="Stemma" src=".github/assets/logo-light.svg" width="420">
  </picture>
</h1>

A repository template for AI-assisted academic research: literature, theory,
analysis, reproducible results, and manuscript. Use the full layout for a paper
with supporting code, or adopt selected parts in an existing project.

**Status:** pre-v0.1. The layout and working tools are usable; initialization and
release export are still manual.

## In practice

Start with a project definition and a current status, then record work at the
scale it needs. A short calculation can stay a note; a bounded research question
can become an investigation with a charter, analysis, and report. Literature
notes retain the technical details needed to use a source, with links back to it.

Agents and humans share the same files. Draft work remains provisional until a
researcher accepts it; findings and decisions retain links to their evidence.
The manuscript and reusable code draw on that accepted work. See
[the research workflow](research/README.md) and [acceptance rules](AGENTS.md#rules).

## Structure

| Zone | Contents | Entry point |
| --- | --- | --- |
| **Release** | `src/`, `tests/`, `data/`, `reproduce/`, `manuscript/`, packaging and CI | [Development](CONTRIBUTING.md), [reproduction](reproduce/README.md) |
| **Research** | Project definition, status, accepted knowledge, investigations, literature, notes and meetings | [PROJECT.md](PROJECT.md), [research/README.md](research/README.md) |
| **Operations** | Agent instructions, shared skills, client configuration and `.stemma/` tools | [AGENTS.md](AGENTS.md) |

Research and Operations are excluded from the intended public release. Keep the
working repository private when those records are private: an automated exporter
does not yet enforce that boundary. A Python package archive contains only the
package and build/test material; the paper's data and reproduction bundle are
separate release artifacts.

## Quickstart

1. Copy the template or adopt selected parts into an existing repository.
   Fill in `PROJECT.md` and `research/STATUS.md`; leave unused memory sections empty.
2. Rename `src/project_name/`, the import and distribution name in
   `tests/test_smoke.py`, and the package name and Hatch paths in `pyproject.toml`.
   Set the author, description, dependencies, and package `__version__`.
3. Adapt [the project README starter](.stemma/init/README.md), add the chosen
   license and citation metadata, and remove the
   [template-only files](DESIGN.md#9-template-only-vs-travelling).
4. Follow [CONTRIBUTING.md](CONTRIBUTING.md) to install, configure the client,
   and run checks. Set required reviews and checks on the repository host.
5. Connect the reference manager to `manuscript/references.bib` and document the
   environment and inputs needed to regenerate results in `reproduce/README.md`.

## Build and tools

- **Hatchling** builds a wheel from `src/` and an explicitly scoped source archive.
  The literal package `__version__` is the single version source.
- **Python 3.12+** is supported; CI covers 3.12 and 3.14. Development dependencies
  use standard groups; pip and uv can install them. See [setup](CONTRIBUTING.md#setup).
- **Ruff, pytest and pre-commit** provide the default checks. Optional notebook,
  shell and analysis tools are commented in the configuration; enable what the
  project uses. Scientific libraries are chosen by each project.
- **Agent skills** cover literature lookup and document extraction. Shared
  instructions live in `AGENTS.md`; `.claude/skills` links to `.agents/skills`.

## Template checks

After [development setup](CONTRIBUTING.md#setup), run `python -m pytest .stemma/tests`
for the tool regressions.
Package checks are documented in [CONTRIBUTING.md](CONTRIBUTING.md#working-and-checking).

## TO DO

- **Initialization:** replace the `init.sh` stub with a tested initializer that
  renames package paths and metadata, renders the project README, and removes
  template-only material without rewriting scientific records.
- **Release export:** implement an allow-list exporter and check that Release
  works without private records, Operations, or sibling checkouts. Define how
  release history and the paper's data/reproduction bundle are published.
- **Release metadata:** supply license and `CITATION.cff` starters, and check for
  placeholders and broken links before publication.
- **Template CI:** run instantiation, archive-boundary and `.stemma/` regression
  checks. Current CI checks the package.
- **Reproduction:** exercise a complete pilot release from a recorded environment
  and archived inputs, including the manuscript. Verify a lockfile workflow for
  analysis dependencies and document any cluster-specific setup.
- **Integrations:** document a concrete reference-manager setup, test client
  permissions for the never-merge rule, and resolve Windows skill-link setup.

Template rationale and open design questions live in [DESIGN.md](DESIGN.md).
