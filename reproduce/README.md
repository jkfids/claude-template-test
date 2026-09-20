# Reproduction

Scripts for the paper's results and figures. Write generated figures to
`manuscript/figures/`; use only code and data included in the release.

Document each result's command, working directory, inputs, outputs, seeds, and
resolved environment. Declare dependencies in `pyproject.toml`; record the
source revision, immutable Git dependency revisions, and any local changes.

Separate figure regeneration from full simulation. For expensive runs, give
runtime and hardware requirements, scheduler settings where applicable, and a
small validation command. Verify the documented commands in a clean release
checkout, without private research files or sibling repositories.

<!-- Commands and output paths, grouped by figure or result. -->
