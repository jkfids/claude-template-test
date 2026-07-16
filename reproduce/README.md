# reproduce

Scripts and tools for regenerating the paper's results and figures.

It is recommended to write at least one script per figure or result. Generated
manuscript figures should be written directly to `manuscript/figures/`.

Scripts may import from `data/` and `src/`. Nothing in `reproduce/` may import
from or depend on `research/`, or anything else that is not exported.

<!-- Script documentation, e.g.:
     reproduce/experiment1.py  ->  manuscript/figures/experiment1_figure.pdf -->
