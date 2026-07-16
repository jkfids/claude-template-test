#!/usr/bin/env bash
# ==============================================================================
# init.sh – Stemma
#
# Converts the template into a project. Run ONCE, immediately after cloning /
# using the template. Removes itself (and DESIGN.md, the template README) when
# done.
#
# What it does:
#   1. Prompt for: project name, description, author name/email, org/user.
#   2. Derive two forms of the name:
#        - hyphen form   (distribution):  e.g. spectral-closure
#        - underscore form (package):     e.g. spectral_closure
#   3. Apply the renames below.
#   4. Install dev deps + pre-commit hooks.
#   5. Replace this README with the project README; delete template-only files.
#   6. Delete itself.
#
# Renames (pyproject.toml + filesystem):
#   project-name              -> <hyphen form>      # pyproject: name, [project.urls]
#   src/project_name/         -> src/<underscore>/  # package directory (git mv)
#   packages = ["src/project_name"]                 # pyproject: wheel packages
#   src/project_name/__about__.py                   # pyproject: dynamic-version comment
#   import project_name       -> import <underscore> # tests/test_smoke.py
#   "A. Einstein" / email     -> <author>           # pyproject: authors
#   "A short description..."   -> <description>      # pyproject: description
#   user                       -> <org>             # pyproject: [project.urls] Source
#
# NOTE: the hyphen and underscore forms are DIFFERENT strings — replace both
# separately. After running, grep for leftover 'project_name' / 'project-name'
# and warn if any remain (CI will NOT catch a wrong-but-consistent rename).
#
# Template-only files to delete on completion:
#   DESIGN.md, init.sh (self), and swap README.md for the project README.
# ==============================================================================

set -euo pipefail
