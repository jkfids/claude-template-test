# Tools

## Markdown to PDF

Requires Python, [Pandoc](https://pandoc.org/installing.html), and TeX Live with
LuaLaTeX on `PATH`.

```bash
python .stemma/md2pdf.py path/to/note.md
python .stemma/md2pdf.py path/to/REPORT.md -o /tmp/report.pdf
```

The default output is a PDF beside the source. Relative image paths are resolved
from the Markdown file. An opening blockquote (optionally after the title) is
treated as an editing contract and omitted automatically. Files without a
contract render normally; later quotations remain. The source is unchanged; an
existing PDF is replaced only when rendering succeeds. Missing images or font
glyphs fail the build; other warnings are shown. Bibliography processing and diagram rendering are not
included.
