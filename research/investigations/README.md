# Investigations

Bounded units of research work. Each investigation asks one question with a
recognizable endpoint, lives in its own directory copied from `_template/`, is
worked on its own branch, and is closed by a single pull request.

## Template layout

- `README.md` – The landing page and central directory of the investigation.
- `ANALYSIS.md` – The detailed, working scientific and technical document.
- `REPORT.md` – The final reviewed account and primary exportable artifact.

## Conventions

- Name investigation directories with a short hyphenated title, `short-title/`,
  and the branch `investigation/short-title`. Names are unique for the life of
  the project.
- Nothing touches `main` until close; active investigations are simply the
  `investigation/*` branches.
- Investigation branches do not modify the Release zone (`src/`, `tests/`,
  `manuscript/`, …). If release changes are needed mid-investigation, edit
  and verify them in place, but commit them on a separate branch off `main`,
  then merge `main` back into the investigation branch.
- A human, never an agent, merges the closing pull request—the merge is the
  acceptance.

## Lifecycle

### 1. Charter

Create the investigation branch from `main`, copy the template to a new
directory, and fill in its `README.md`: the question, its scope, and what
would conclude it.

```bash
# In project root.
slug="<short-title>"  # Replace.
git switch main
git switch -c "investigation/${slug}"
mkdir "research/investigations/${slug}"
cp -R research/investigations/_template/. "research/investigations/${slug}/"
```

Fill in `research/investigations/${slug}/README.md`, then commit and push
the investigation branch.

```bash
# Make sure to re-set slug if this is a new shell session:
# slug="<short-title>"
git add "research/investigations/${slug}"
git commit -m "Charter investigation: ${slug}"
git push -u origin "investigation/${slug}"  # Visibility to collaborators.
```

### 2. Work

Commit directly on the branch. Develop the research in `ANALYSIS.md` and
supporting artifacts; keep the investigation `README.md` current. `REPORT.md`
may be drafted as results stabilize, but must not lead the analysis.

### 3. Close

Complete `REPORT.md`, finalize the investigation `README.md`, and open the
closing pull request—the investigation directory together with resulting
updates to `research/`'s memory files. Keep unrelated housekeeping and
release-facing changes out of it. Once merged, delete the branch.
