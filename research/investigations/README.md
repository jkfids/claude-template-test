# Investigations

Bounded research with a stated objective and recognizable endpoint. Each has
its own directory, branch, and PR:

- `README.md`: objective, scope, completion criterion, and current state.
- `ANALYSIS.md`: working technical record and reproduction details.
- `REPORT.md`: concise final account supported by the analysis.

## Charter

Use a unique, short hyphenated name. From the repository root:

```bash
slug="<short-title>"
git fetch origin
git worktree add -b "investigation/${slug}" "../investigation-${slug}" origin/main
cd "../investigation-${slug}"
mkdir "research/investigations/${slug}"
cp -R research/investigations/_template/. "research/investigations/${slug}/"
```

Fill in the investigation README, then register it with a draft PR:

```bash
git add "research/investigations/${slug}"
git commit -m "Charter investigation: ${slug}"
git push -u origin "investigation/${slug}"
gh pr create --draft --title "Investigation: ${slug}" --fill
```

Nothing enters `main` until close. This draft becomes the closing PR.

## Work

Commit on the investigation branch. Keep its README current and develop the
evidence in `ANALYSIS.md`. Add supporting files as needed; keep the directory
flat until subdirectories help. For computations, record commands runnable
from the repository root, environment, inputs, and seeds.

If Release changes are needed, implement and verify them in a separate worktree
on a branch from `main`, with their own PR. Track that dependency in the
investigation README. After human merge, fetch and merge updated `main` into
the investigation branch; do not rebase a shared branch.

## Close

Complete `REPORT.md`, finalize the README, and propose the resulting memory
updates in the same PR. Keep its scope to this investigation and affected
memory files. Mark it ready for review; delete the branch after human merge.
Acceptance and charter changes follow [AGENTS.md](../../AGENTS.md#rules).
