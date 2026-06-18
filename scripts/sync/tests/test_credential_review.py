import pytest
from pathlib import Path
from unittest.mock import patch
from credential_review import delete_lines, review, DELETED, SKIPPED, ABORTED


@pytest.fixture
def cred_file(tmp_path):
    """A file with some lines, a few of which are 'credentials'."""
    p = tmp_path / "history.txt"
    p.write_text("line one\nexport SECRET=abc123\nline three\nexport TOKEN=xyz789\nline five\n")
    return p


# sample findings matching the file above (line_num, label, line, match)
HITS = [
    (2, "credential assignment", "export SECRET=abc123", "SECRET=abc123"),
    (4, "credential assignment", "export TOKEN=xyz789",  "TOKEN=xyz789"),
]


# --- delete_lines ---

def test_delete_single_line(cred_file):
    delete_lines(cred_file, {2})
    lines = cred_file.read_text().splitlines()
    assert lines == ["line one", "line three", "export TOKEN=xyz789", "line five"]


def test_delete_multiple_lines(cred_file):
    delete_lines(cred_file, {2, 4})
    lines = cred_file.read_text().splitlines()
    assert lines == ["line one", "line three", "line five"]


def test_delete_first_line(cred_file):
    delete_lines(cred_file, {1})
    assert cred_file.read_text().startswith("export SECRET=abc123")


def test_delete_last_line(cred_file):
    delete_lines(cred_file, {5})
    assert "line five" not in cred_file.read_text()


def test_delete_empty_set_is_noop(cred_file):
    original = cred_file.read_text()
    delete_lines(cred_file, set())
    assert cred_file.read_text() == original


def test_delete_preserves_line_endings(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("a\nb\nc\n")
    delete_lines(p, {2})
    assert p.read_text() == "a\nc\n"


# --- review (non-tty path) ---

def test_review_non_tty_returns_aborted(cred_file):
    with patch("sys.stdout.isatty", return_value=False):
        assert review(cred_file, HITS) == ABORTED


# --- review (tty path, mocked curses.wrapper) ---

def test_review_abort_returns_aborted(cred_file):
    with patch("sys.stdout.isatty", return_value=True), \
         patch("curses.wrapper", return_value=None):
        assert review(cred_file, HITS) == ABORTED


def test_review_skip_returns_skipped(cred_file):
    with patch("sys.stdout.isatty", return_value=True), \
         patch("curses.wrapper", return_value="skip"):
        assert review(cred_file, HITS) == SKIPPED


def test_review_delete_removes_lines_and_returns_deleted(cred_file):
    with patch("sys.stdout.isatty", return_value=True), \
         patch("curses.wrapper", return_value=[2, 4]):
        result = review(cred_file, HITS)
    assert result == DELETED
    lines = cred_file.read_text().splitlines()
    assert "export SECRET=abc123" not in lines
    assert "export TOKEN=xyz789" not in lines


def test_review_partial_delete(cred_file):
    with patch("sys.stdout.isatty", return_value=True), \
         patch("curses.wrapper", return_value=[2]):
        review(cred_file, HITS)
    lines = cred_file.read_text().splitlines()
    assert "export SECRET=abc123" not in lines
    assert "export TOKEN=xyz789" in lines
