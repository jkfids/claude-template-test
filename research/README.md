# Research

The project's private scientific workspace and shared memory: the context,
working records, evidence, and accumulated understanding needed to continue
the research across collaborators and agent sessions. Nothing here is exported
or published, and nothing in the Release zone may depend on this directory.

## Project memory

[`../PROJECT.md`](../PROJECT.md) – Durable definition of the project, what it
is, why it exists, who is involved.

[`STATUS.md`](STATUS.md) – Rough project snapshot: current tasks and priorities.

[`FINDINGS.md`](FINDINGS.md) – Canonical scientific knowledge that the project
is prepared to rely on.

[`DECISIONS.md`](DECISIONS.md) – Project-level methodological, technical, and
strategic choices.

[`SURVEY.md`](SURVEY.md) – Synthesis of relevant literature.

[`QUESTIONS.md`](QUESTIONS.md) – Unresolved questions of research significance.

## Working directories

[**[README]**](investigations/README.md) [`investigations/`](investigations/) –
Bounded units of research; conventions and operating notes in its README.

[**[README]**](literature/README.md) [`literature/`](literature/) – Per-source
notes on the external literature, one file per bibliography citekey.

[**[README]**](meetings/README.md) [`meetings/`](meetings/) – Project meeting
records; one directory per meeting.

[`notes/`](notes/) – Durable, free-form research records: derivations, logbook
entries, writeups, collaborator material.

[`workbench/`](workbench/) – Scratch workspace for exploratory analysis,
temporary scripts, notebooks, and raw derivations.

## How to use

Begin with PROJECT.md for stable context and STATUS.md for the current
state, then follow links into the material relevant to the work at hand.

Raw notes, conversational conclusions, meeting transcripts, workbench outputs,
and active investigations are provisional—they may support a conclusion, but
they are not canonical knowledge by themselves. Important conclusions are
promoted into a legible record stating the claim, its support, scope,
limitations, and pointers to the underlying evidence. This will typically
be an investigation's report, or a self-contained writeup in `notes/`.
Entries in `FINDINGS.md` and `DECISIONS.md` link to that provenance rather
than reproducing it.

A conclusion becomes canonical through a pull request. A human, never an
agent, merges it; the merge is the acceptance. Other work in `research/` is
committed directly, including on active investigation branches. Write for
the next researcher or agent who must understand, assess, and continue the
work.
