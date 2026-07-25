#!/usr/bin/env bash
# ==============================================================================
# init.sh – Stemma
#
# Converts the template into a project. Run ONCE, from the repository root,
# immediately after cloning or using the template. Deletes itself when done.
#
#   ./init.sh
#
# STATUS: stub. The spec below is the implementation plan.
#
# What it does:
#   1. Prompt for: project name, description, author name/email, org/user.
#      Sensible defaults: directory name, `git config user.name` / `user.email`.
#   2. Derive two forms of the name:
#        - hyphen form     (distribution):  e.g. spectral-closure
#        - underscore form (package):       e.g. spectral_closure
#   3. Apply the renames below.
#   4. Render the project README; delete template-only paths.
#   5. Install dev deps + pre-commit hooks.
#   6. Warn on leftovers, print the post-init checklist, delete itself.
#
# Renames (pyproject.toml + filesystem):
#   project-name              -> <hyphen form>       # pyproject: name, [project.urls]
#   src/project_name/         -> src/<underscore>/   # package directory (git mv)
#   packages = ["src/project_name"]                  # pyproject: wheel packages
#   src/project_name/__about__.py                    # pyproject: dynamic-version comment
#   import project_name       -> import <underscore> # tests/test_smoke.py
#   "A. Einstein" / email     -> <author>            # pyproject: authors
#   "A short description..."  -> <description>       # pyproject: description
#   https://github.com/user/project-name -> <org>    # pyproject: [project.urls]
#
# NOTE: the hyphen and underscore forms are DIFFERENT strings — replace both
# separately, longest/most specific first. Prefer python3 over sed for the
# substitutions: user input contains slashes, ampersands, and quotes, and
# `sed -i` differs between GNU and BSD.
#
# Template-only paths to delete (keep in sync with DESIGN.md §9):
#   DESIGN.md              # template design doc
#   README.md              # replaced by .stemma/init/README.md, rendered
#   .github/assets/        # Stemma logo — NOTE: .github/workflows/ TRAVELS
#   .stemma/init/          # instantiation templates, consumed here
#   init.sh                # self
#
# Rendering: .stemma/init/README.md carries {{PROJECT_NAME}}, {{DESCRIPTION}},
# {{AUTHOR}}, {{ORG}}. Render the same way when .stemma/init/CITATION.cff and
# the stamped LICENSE arrive.
#
# Verification: after substitution, grep for leftover 'project_name',
# 'project-name', and '{{...}}' and warn. CI will NOT catch a
# wrong-but-consistent rename.
#
# Post-init checklist to print:
#   - Fill in PROJECT.md.
#   - Review pyproject.toml (license, dependencies, URLs).
#   - Enable branch protection on main for src/ and tests/.
#   - Commit the result.
#   - Read research/README.md.
#
# Testing: support non-interactive use so the instantiation test (DESIGN §7)
# can drive it —
#   PROJECT_NAME=... DESCRIPTION=... AUTHOR_NAME=... AUTHOR_EMAIL=... ORG=... \
#   ./init.sh --yes
# ==============================================================================

set -euo pipefail

echo "init.sh is not implemented yet — see the spec in this file."
exit 1
