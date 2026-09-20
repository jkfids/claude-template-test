import base64
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "md2pdf.py"
spec = importlib.util.spec_from_file_location("md2pdf", SCRIPT)
md2pdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(md2pdf)

PDF_TOOLS = ("pandoc", "lualatex", "pdftotext", "pdfinfo")
pdf_test = pytest.mark.skipif(
    not all(shutil.which(tool) for tool in PDF_TOOLS), reason="PDF tools not installed"
)


def run_cli(source, *args, cwd):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(source), *map(str, args)],
        cwd=cwd,
        text=True,
        capture_output=True,
    )


def pdf_text(path):
    return subprocess.check_output(["pdftotext", str(path), "-"], text=True)


@pytest.mark.parametrize("with_title", [False, True])
def test_strip_only_opening_quote(with_title):
    heading = {"t": "Header", "c": [1, ["", [], []], []]}
    contract = {"t": "BlockQuote", "c": [{"t": "Para", "c": []}]}
    body = {"t": "Para", "c": [{"t": "Str", "c": "Evidence"}]}
    quote = {"t": "BlockQuote", "c": [{"t": "Para", "c": [{"t": "Str", "c": "Quote"}]}]}
    document = {"blocks": ([heading] if with_title else []) + [contract, body, quote]}
    md2pdf.strip_contract(document)
    assert document["blocks"] == ([heading] if with_title else []) + [body, quote]


@pytest.mark.parametrize("blocks", [[], [{"t": "Para", "c": []}], [{"t": "Header", "c": []}]])
def test_missing_contract_leaves_document_unchanged(blocks):
    document = {"blocks": blocks.copy()}
    md2pdf.strip_contract(document)
    assert document["blocks"] == blocks


def test_refuse_to_overwrite_source(tmp_path):
    source = tmp_path / "note.md"
    source.write_text("Keep the original")
    result = run_cli(source, "-o", source, cwd=tmp_path)
    assert result.returncode != 0
    assert "separate .pdf" in result.stderr
    assert source.read_text() == "Keep the original"


def test_missing_tool_message(tmp_path, monkeypatch):
    source = tmp_path / "note.md"
    source.write_text("# Note")
    monkeypatch.setenv("PATH", "")
    result = run_cli(source, cwd=tmp_path)
    assert result.returncode != 0
    assert "pandoc not found" in result.stderr
    assert not source.with_suffix(".pdf").exists()


@pdf_test
def test_report_render_and_relative_image(tmp_path):
    folder = tmp_path / "notes with spaces"
    folder.mkdir()
    # A small PNG fixture; the test checks figure resolution from another cwd.
    (folder / "figure.png").write_bytes(
        base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNQaDgAAAIkAWHdFJqQAAAAAElFTkSuQmCC"
        )
    )
    source = folder / "report.md"
    content = """# A report

> Editing contract to omit.
> A second contract line.

## Result

A visible claim with $x^2$ and a footnote.[^1]

$$
\\sum_{k=1}^{n} k = \\frac{n(n+1)}{2}
$$

| Case | Result |
| --- | --- |
| Reference | Agreement |

![A visible figure caption](figure.png){width=1cm}

> A quotation to retain.

[^1]: A visible footnote.
"""
    source.write_text(content)
    output = tmp_path / "exports" / "report.pdf"
    result = run_cli(source, "-o", output, cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    text = pdf_text(output)
    for expected in [
        "A report",
        "visible claim",
        "Reference",
        "Agreement",
        "visible figure caption",
        "quotation to retain",
        "visible footnote",
    ]:
        assert expected in text
    assert "Editing contract" not in text
    assert "second contract" not in text
    assert source.read_text() == content
    info = subprocess.check_output(["pdfinfo", str(output)], text=True)
    assert "A4" in info
    assert not list(output.parent.glob(".md2pdf-*"))


@pdf_test
def test_no_contract_renders_and_writes_beside_source(tmp_path):
    source = tmp_path / "note.md"
    source.write_text("# Note\n\nUseful text.\n\n> A later quotation.\n")
    result = run_cli(source, cwd=tmp_path.parent)
    assert result.returncode == 0, result.stderr
    assert "A later quotation" in pdf_text(source.with_suffix(".pdf"))


@pdf_test
@pytest.mark.parametrize(
    "body", ["![Missing figure](does-not-exist.png)", "Missing glyph: \U0010ffff"]
)
def test_failed_render_preserves_previous_pdf(tmp_path, body):
    source = tmp_path / "broken.md"
    source.write_text(f"# Broken\n\n{body}\n")
    output = source.with_suffix(".pdf")
    output.write_bytes(b"previous output")
    result = run_cli(source, cwd=tmp_path)
    assert result.returncode != 0
    assert output.read_bytes() == b"previous output"
    assert not list(tmp_path.glob(".md2pdf-*"))
