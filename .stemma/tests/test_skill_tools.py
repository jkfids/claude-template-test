"""Offline integration checks for vendored skills; dependencies are optional."""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


SKILLS = Path(__file__).resolve().parents[2] / ".agents/skills"


def run_script(skill, script, *args):
    return subprocess.run(
        [sys.executable, str(SKILLS / skill / "scripts" / script), *map(str, args)],
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "MPLBACKEND": "Agg"},
    )


def make_pdf(path, text):
    pytest.importorskip("matplotlib")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(3, 2))
    fig.text(0.1, 0.5, text)
    fig.savefig(path)
    plt.close(fig)


def test_liteparse_batch_preserves_nested_names_and_existing_outputs(tmp_path):
    pytest.importorskip("liteparse")
    source = tmp_path / "input"
    output = tmp_path / "output"
    make_pdf(source / "first/paper.pdf", "Alpha specimen")
    make_pdf(source / "second/paper.pdf", "Beta specimen")
    args = (source, output, "--recursive", "--format", "json", "--no-ocr", "--quiet")
    result = run_script("liteparse", "batch_parse_dir.py", *args)
    assert result.returncode == 0, result.stderr
    first = output / "first/paper.json"
    second = output / "second/paper.json"
    assert "Alpha specimen" in json.loads(first.read_text())["text"]
    assert "Beta specimen" in json.loads(second.read_text())["text"]
    first.write_text("existing result")
    before = second.read_bytes()
    result = run_script("liteparse", "batch_parse_dir.py", *args)
    assert result.returncode == 1
    assert first.read_text() == "existing result"
    assert second.read_bytes() == before


def test_liteparse_batch_reports_colliding_extensions(tmp_path):
    pytest.importorskip("liteparse")
    pytest.importorskip("PIL")
    from PIL import Image

    source = tmp_path / "input"
    output = tmp_path / "output"
    source.mkdir()
    for extension in ("jpg", "png"):
        Image.new("RGB", (30, 30), "white").save(source / f"same.{extension}")
    result = run_script(
        "liteparse", "batch_parse_dir.py", source, output, "--no-ocr", "--quiet"
    )
    assert result.returncode == 1
    assert "1 succeeded, 1 failed" in result.stdout
    assert "File exists" in result.stderr


def test_scientific_figure_export_and_metadata(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("PIL")
    pytest.importorskip("pypdf")
    result = run_script(
        "scientific-visualization", "figure_export.py",
        "--demo", tmp_path / "figure", "--formats", "pdf,png,svg", "--manifest",
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert len(report["outputs"]) == 3
    assert json.loads((tmp_path / "figure.export.json").read_text())["provenance"]
    from PIL import Image
    from pypdf import PdfReader

    with Image.open(tmp_path / "figure.png") as im:
        assert im.size == (1050, 750)
    page = PdfReader(tmp_path / "figure.pdf").pages[0]
    assert float(page.mediabox.width) == pytest.approx(252)
    assert float(page.mediabox.height) == pytest.approx(180)
    assert "Amplitude" in page.extract_text()
    result = run_script(
        "scientific-visualization", "image_metadata.py", tmp_path / "figure.pdf"
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["metadata"]["format"] == "PDF"


def test_scientific_figure_export_refuses_overwrite(tmp_path):
    pytest.importorskip("matplotlib")
    output = tmp_path / "figure.pdf"
    output.write_bytes(b"existing figure")
    result = run_script(
        "scientific-visualization", "figure_export.py", "--demo", tmp_path / "figure"
    )
    assert result.returncode == 2
    assert output.read_bytes() == b"existing figure"


@pytest.mark.parametrize(
    "rotation,width_pt,height_pt",
    [(0, 72, 144), (90, 144, 72), (180, 72, 144), (270, 144, 72)],
)
def test_pdf_metadata_uses_displayed_dimensions(tmp_path, rotation, width_pt, height_pt):
    pytest.importorskip("pypdf")
    from pypdf import PdfWriter

    path = tmp_path / "rotated.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=144).rotate(rotation)
    writer.write(path)
    result = run_script("scientific-visualization", "image_metadata.py", path)
    assert result.returncode == 0, result.stderr
    metadata = json.loads(result.stdout)["metadata"]
    assert metadata["first_page_width_pt"] == width_pt
    assert metadata["first_page_height_pt"] == height_pt
    assert metadata["width_mm"] == pytest.approx(width_pt / 72 * 25.4)
    assert metadata["height_mm"] == pytest.approx(height_pt / 72 * 25.4)
