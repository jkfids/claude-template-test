# Investigations

Bounded units of research work. Each investigation pursues one stated
objective with a recognizable endpoint, lives in its own directory copied
from `_template/`, is worked on its own branch, and is closed by a single
pull request.

## Template layout

- `README.md` – The landing page and central directory of the investigation.
- `ANALYSIS.md` – The detailed, working scientific and technical document.
- `REPORT.md` – The final reviewed account and primary exportable artifact.

## Conventions

- Name investigation directories with a short hyphenated title,
  `<short-title>/`, and the branch `investigation/<short-title>`. Names are
  unique for the life of the project.
- Nothing enters `main` until close. Chartering opens a **draft pull request**
  as the visible registry of active investigations, and it becomes the closing
  pull request at the end.
- Investigation branches do not modify the Release zone (`src/`, `tests/`,
  `manuscript/`, …). If release changes are needed mid-investigation, edit
  and verify them in place, but commit them on a separate branch off `main`,
  then merge (rather than rebase) `main` back into the investigation branch.
- A human merges the closing pull request—the merge is the acceptance.
- Prefer flat investigation directories; add subdirectories (`figures/`,
  `data/`) only once files accumulate.
- Results quoted in `ANALYSIS.md` and `REPORT.md` trace to scripts in the
  investigation directory, runnable from the repository root; fix and record
  any seeds.

## Lifecycle

### 1. Charter

Create the investigation branch from `main`, copy the template to a new
directory, and fill in its `README.md`: its objective, its scope, and its
completion criterion.

```bash
# In project root.
slug="<short-title>"  # Replace.
git switch main
git switch -c "investigation/${slug}"
mkdir "research/investigations/${slug}"
cp -R research/investigations/_template/. "research/investigations/${slug}/"
```

Fill in `research/investigations/${slug}/README.md`, then commit and push
the investigation branch, and open the draft pull request.

```bash
# Make sure to re-set slug if the previous shell session was closed:
# slug="<short-title>"
git add "research/investigations/${slug}"
git commit -m "Charter investigation: ${slug}"
git push -u origin "investigation/${slug}"
gh pr create --draft --title "Investigation: ${slug}" --fill  # Or open a draft PR from GitHub.
```

### 2. Work

Commit directly on the branch. Develop the research in `ANALYSIS.md` and
supporting artifacts; keep the investigation `README.md` current. `REPORT.md`
may be drafted as results stabilize, but must not lead the analysis.

### 3. Close

Complete `REPORT.md`, finalize the investigation `README.md`, and add the
resulting updates to `research/`'s memory files. Then mark the draft pull
request ready for review. Keep unrelated housekeeping and release-facing
changes out of it. Once merged, delete the branch.
