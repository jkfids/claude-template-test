"""Regression checks for the bundled pager; no network or credentials needed."""

import importlib.util
import io
import json
import sys
import urllib.error
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / ".agents/skills/paper-lookup/scripts"
spec = importlib.util.spec_from_file_location("paper_pager", SCRIPTS / "paginate.py")
pager = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = pager
spec.loader.exec_module(pager)


@pytest.mark.parametrize("failure", ["http", "network", "json"])
def test_fetch_errors_redact_credentials(monkeypatch, failure):
    url = "https://example.org/works?api_key=secret-token&mailto=private-address"

    def open_url(*args, **kwargs):
        if failure == "http":
            raise urllib.error.HTTPError(url, 403, "denied", {}, io.BytesIO(url.encode()))
        if failure == "network":
            raise urllib.error.URLError(url)
        return io.BytesIO(url.encode())

    monkeypatch.setattr(pager.urllib.request, "urlopen", open_url)
    with pytest.raises(RuntimeError) as error:
        pager.fetch(url)
    assert "REDACTED" in str(error.value)
    assert "secret-token" not in str(error.value)
    assert "private-address" not in str(error.value)
    assert error.value.__suppress_context__


def test_openalex_caps_page_size(monkeypatch):
    monkeypatch.setenv("OPENALEX_API_KEY", "test-key")
    params = parse_qs(urlsplit(pager._openalex_url("search=quantum", "*", 200)).query)
    assert params["per-page"] == ["100"]
    assert params["api_key"] == ["test-key"]


@pytest.mark.parametrize("payload", [{}, {"error": "bad query"}, {"meta": {}, "results": {}}])
def test_openalex_rejects_error_payload(payload):
    with pytest.raises(RuntimeError, match="meta or results"):
        pager._openalex_parse(payload, "*")


def test_bounded_walk_and_query_redaction(monkeypatch, capsys):
    monkeypatch.setattr(
        pager,
        "fetch",
        lambda url: {
            "meta": {"count": 50, "next_cursor": "next"},
            "results": [{"id": "W1"}],
        },
    )
    monkeypatch.setattr(pager.time, "sleep", lambda _: None)
    assert (
        pager.main(
            [
                "--api",
                "openalex",
                "--query",
                "search=quantum&api_key=secret-token",
                "--max-calls",
                "1",
                "--max-records",
                "5",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert "secret-token" not in captured.out + captured.err
    result = json.loads(captured.out)
    assert result["reconciliation"]["stopped_at_limit"]
    assert not result["reconciliation"]["complete"]
    assert result["reconciliation"]["retrieved_total"] == 1


def test_unexplained_shortfall_fails(monkeypatch):
    monkeypatch.setattr(
        pager,
        "fetch",
        lambda url: {
            "meta": {"count": 2, "next_cursor": None},
            "results": [{"id": "W1"}],
        },
    )
    with pytest.raises(SystemExit) as error:
        pager.main(["--api", "openalex", "--query", "search=quantum"])
    assert error.value.code == 4


def test_rxiv_advances_by_returned_count():
    page = pager._rxiv_parse(
        {
            "messages": [{"status": "ok", "total": 90, "count": 100}],
            "collection": [{"doi": str(n)} for n in range(30)],
        },
        30,
    )
    assert page.next_state == 60
    assert page.notes


def test_sparse_abstract_index_does_not_allocate_for_gaps():
    spec = importlib.util.spec_from_file_location("abstract", SCRIPTS / "openalex_abstract.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    text, warnings = module.reconstruct({"First": [0], "last": [10**12]})
    assert text == "First last"
    assert any("999999999999 position(s) absent" in note for note in warnings)


@pytest.mark.parametrize("total", [3, None])
def test_oversized_final_page_is_partial(monkeypatch, total):
    api = pager.Api(
        name="fixed-page-size",
        delay=0,
        build_url=lambda query, state, limit: "https://example.org/works",
        parse=lambda payload, state: pager.Page(records=payload, total=total),
    )
    monkeypatch.setattr(pager, "fetch", lambda url: [{"id": n} for n in range(3)])
    records, check, _ = pager.walk(
        api, "query", page_size=1, max_records=1, max_calls=1, verbose=False
    )
    assert records == [{"id": 0}]
    assert check.stopped_at_limit
    assert not check.complete
    assert check.ok
