#!/usr/bin/env python3
"""Render Markdown with Pandoc and LuaLaTeX. Requires both executables on PATH."""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def strip_contract(document):
    """Remove one opening blockquote, optionally preceded by a title."""
    blocks = document["blocks"]
    index = 1 if blocks and blocks[0]["t"] == "Header" else 0
    if len(blocks) > index and blocks[index]["t"] == "BlockQuote":
        del blocks[index]


def convert(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_file():
        raise ValueError(f"input file not found: {source}")
    if source == output or output.suffix.lower() != ".pdf":
        raise ValueError("output must be a separate .pdf file")
    for tool in ("pandoc", "lualatex"):
        if not shutil.which(tool):
            raise ValueError(f"{tool} not found; install Pandoc and TeX Live with LuaLaTeX")

    parsed = subprocess.run(
        ["pandoc", "--from=markdown", "--to=json", str(source)],
        cwd=source.parent,
        text=True,
        capture_output=True,
        check=True,
    )
    document = json.loads(parsed.stdout)
    strip_contract(document)

    output.parent.mkdir(parents=True, exist_ok=True)
    # Publish only a successful render; a failed build preserves any existing PDF.
    with tempfile.TemporaryDirectory(prefix=".md2pdf-", dir=output.parent) as temp:
        rendered = Path(temp) / "document.pdf"
        log = Path(temp) / "pandoc.json"
        result = subprocess.run(
            [
                "pandoc",
                "--from=json",
                "--pdf-engine=lualatex",
                "--resource-path=.",
                "--log",
                str(log),
                "-V",
                "geometry:margin=25mm",
                "-V",
                "fontsize=11pt",
                "-V",
                "papersize=a4",
                "-o",
                str(rendered),
            ],
            input=json.dumps(document),
            cwd=source.parent,
            text=True,
            capture_output=True,
            check=True,
        )
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr)
        for message in json.loads(log.read_text()):
            if message["type"] in {"CouldNotFetchResource", "MissingCharacter"}:
                raise ValueError(message["pretty"])
        rendered.replace(output)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Markdown file")
    parser.add_argument(
        "-o", "--output", type=Path, help="default: beside the source, with .pdf suffix"
    )
    args = parser.parse_args(argv)
    try:
        output = convert(
            args.source,
            args.output or args.source.with_suffix(".pdf"),
        )
    except (ValueError, OSError) as error:
        print(f"md2pdf: {error}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(f"md2pdf: {error.stderr.strip() or str(error)}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
