# Development

[AGENTS.md](AGENTS.md#rules) defines change and acceptance rules.
Research records follow [research/README.md](research/README.md).

## Setup

From the repository root, use Python 3.14 for development (3.12 is the minimum):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . --group dev
pre-commit install
```

Alternatively, [uv](https://docs.astral.sh/uv/) installs the package and dev group
with `uv python pin 3.14` followed by `uv sync`. Install hooks with
`uv run pre-commit install`; prefix the checks below with `uv run`. Add research-only
libraries to an `analysis` dependency group and sync it with `--group analysis`.
For a project using uv, commit its `uv.lock` and `.python-version`; reproduce the
locked environment with `uv sync --locked` (add `--group analysis` when used).
Update the lock deliberately and record non-Python tools in `reproduce/README.md`.
Package CI tests current compatible dependencies.

`AGENTS.md` is the shared instruction entry point. Project skills live in
`.agents/skills/`; `.claude/skills` links there for Claude. Verify that link and
confirm the client loads the instructions and skills. Claude's `AGENTS.md`
discovery is conditional: local or ancestor `CLAUDE.md` / `CLAUDE.local.md` files
and some session settings can suppress it. Check the startup banner and the
[discovery rules](https://code.claude.com/docs/en/memory#agents-md); when keeping
both file types, select `claude-md-and-agents-md` under Project instructions.

## Working and checking

Use a separate worktree when another session owns the checkout. Keep changes
scoped to the task and inspect both committed and working-tree changes:

```bash
git diff --name-only main...HEAD
git status --short
```

Run the checks relevant to the change and report their results and limits:

- **Code:** `python -m pytest`; add tests for changed behavior.
- **Documentation:** check links, commands, and consistency.
- **Manuscript:** compile the active entry point and inspect the output.
- **Analysis:** record reproducible evidence alongside the claims.
- **Packaging:** `python -m build`; inspect the sdist and rebuilt wheel for
  unintended files, then install and test the wheel in a clean environment.

Run `pre-commit run --all-files` and `git diff --check` before review.
A passing build or numerical check does not establish a scientific claim.

Package archives contain code and build/test metadata. Data, reproduction
scripts, and manuscript accompany the paper separately. Follow
[reproduce/README.md](reproduce/README.md) to verify that release.
