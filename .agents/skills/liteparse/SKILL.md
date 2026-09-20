---
name: liteparse
description: Extract text, Markdown, or spatial JSON from local PDFs and documents; OCR scans, batch-parse paper collections, or render pages to PNG. Use when reading source documents requires layout or page coordinates.
license: Apache-2.0
metadata:
  skill-author: K-Dense Inc.
  modified-by: Stemma
  upstream: https://github.com/K-Dense-AI/scientific-agent-skills/tree/0e451065e3308e9902d8229e17d2028359b2bbaf/skills/liteparse
  tested-version: "2.14.6"
---

# LiteParse

Install with `uv pip install liteparse`. PDFs and images are handled locally;
Office formats require LibreOffice (`soffice` on PATH). OCR is enabled by
default; language data may need downloading on first use. For offline OCR,
provide trained data through `--tessdata-path`.

## Extract or render

```bash
lit parse paper.pdf --no-ocr -o paper.txt
lit parse paper.pdf --format markdown -o paper.md
lit parse paper.pdf --format json --target-pages "1-5,10" -o paper.json
lit screenshot paper.pdf --target-pages "1,3" -o screenshots
lit parse scan.pdf --ocr-language eng -o scan.txt
```

Use `--no-ocr` for text-native PDFs. JSON exposes per-page `text_items` with
text and bounding boxes; add `--extract-text-metadata` when font information is
needed. Inspect page images when equations, tables, or reading order matter:
extracted text alone does not establish that these survived correctly.

```python
from liteparse import LiteParse

parser = LiteParse(ocr_enabled=False, quiet=True)
result = parser.parse("paper.pdf")
for page in result.pages:
    for item in page.text_items:
        print(page.page_num, item.text, item.x, item.y, item.width, item.height)
```

## Batch

```bash
lit batch-parse papers parsed --format json --recursive --extension .pdf --no-ocr
```

The CLI preserves subdirectories. Process different input extensions into
separate output directories when basenames repeat: `paper.pdf` and
`paper.docx` would both map to `paper.json`.

Use `lit <command> --help` for installed options and the
[upstream documentation](https://developers.llamaindex.ai/liteparse/) for
advanced parsing, OCR servers, and language bindings.
