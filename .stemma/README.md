# {{PROJECT_NAME}}

A short description of the project.

## Links and abstract

- **DOI** – 
- **arXiv** – 

**Abstract**

> Paper abstract.

## Repository overview

- **`src/`** – Source code.
- **`tests/`** – Tests for **`src/`**.
- **`data/`** – Input data for reproducing results.
- **`reproduce/`** – Scripts for generating the paper's results and figures.
- **`manuscript/`** – LaTeX source files.

## Reproduce

**Clone**
```bash
git clone <repo-url>
cd <project-name>
```

**Install** (in project root)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .  # For devs:  pip install -e ".[dev]"
```

**Run**
```bash
# Commands that regenerate the main results, e.g.:
# python reproduce/experiment1.py
```

## Citation

See [`CITATION.cff`](CITATION.cff).

**BibTeX**
```bibtex

```

## Contact

See paper.

## License

See [`LICENSE`](LICENSE).
