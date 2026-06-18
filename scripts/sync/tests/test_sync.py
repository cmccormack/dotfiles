import pytest
from pathlib import Path
from unittest.mock import patch
from sync import parse_manifest, link_entry


@pytest.fixture
def repo(tmp_path):
    """Minimal fake repo with a scripts/ dir."""
    (tmp_path / "scripts").mkdir()
    return tmp_path


@pytest.fixture
def home(tmp_path):
    h = tmp_path / "home"
    h.mkdir(exist_ok=True)
    return h


# --- parse_manifest ---

def test_parse_manifest_basic(tmp_path):
    m = tmp_path / "manifest.conf"
    m.write_text("~/.zshrc:MacOS/home/.zshrc\n~/.gitconfig:MacOS/home/.gitconfig\n")
    assert parse_manifest(m) == [
        ("~/.zshrc", "MacOS/home/.zshrc"),
        ("~/.gitconfig", "MacOS/home/.gitconfig"),
    ]


def test_parse_manifest_skips_comments_and_blanks(tmp_path):
    m = tmp_path / "manifest.conf"
    m.write_text("# comment\n\n~/.zshrc:MacOS/home/.zshrc\n")
    assert parse_manifest(m) == [("~/.zshrc", "MacOS/home/.zshrc")]


def test_parse_manifest_warns_on_malformed_line(tmp_path, capsys):
    m = tmp_path / "manifest.conf"
    m.write_text("no-colon-here\n")
    result = parse_manifest(m)
    assert result == []
    assert "malformed" in capsys.readouterr().out


def test_parse_manifest_handles_colons_in_dest(tmp_path):
    # only split on first colon
    m = tmp_path / "manifest.conf"
    m.write_text("~/.zshrc:MacOS/home/.zshrc\n")
    src, dest = parse_manifest(m)[0]
    assert dest == "MacOS/home/.zshrc"


# --- link_entry ---

def test_already_linked_is_noop(repo, home, capsys):

    real_file = repo / "MacOS" / "home" / ".zshrc"
    real_file.parent.mkdir(parents=True)
    real_file.write_text("# zshrc\n")

    link = home / ".zshrc"
    link.symlink_to(real_file)

    # Pass the absolute path — ~ expansion would resolve to the real $HOME
    action = link_entry(
        str(link),
        "MacOS/home/.zshrc",
        dry_run=False,
        skip_cred_check=True,
        repo_root=repo,
    )
    assert action == "ok"
    assert link.is_symlink()  # unchanged


def test_real_file_is_moved_and_linked(repo, home):

    src = home / ".gitconfig"
    src.write_text("[user]\n\tname = Chris\n")

    action = link_entry(
        str(src),
        "MacOS/home/.gitconfig",
        dry_run=False,
        skip_cred_check=True,
        repo_root=repo,
    )

    assert action == "linked"
    assert src.is_symlink()
    assert src.resolve() == (repo / "MacOS/home/.gitconfig").resolve()
    assert (repo / "MacOS/home/.gitconfig").read_text() == "[user]\n\tname = Chris\n"


def test_dry_run_makes_no_changes(repo, home):

    src = home / ".zshrc"
    src.write_text("# zshrc\n")

    link_entry(
        str(src),
        "MacOS/home/.zshrc",
        dry_run=True,
        skip_cred_check=True,
        repo_root=repo,
    )

    assert src.is_file()          # still a plain file, not moved
    assert not src.is_symlink()
    assert not (repo / "MacOS/home/.zshrc").exists()


def test_dest_exists_without_src_creates_symlink(repo, home):

    dest = repo / "MacOS" / "home" / ".zshrc"
    dest.parent.mkdir(parents=True)
    dest.write_text("# zshrc\n")

    src = home / ".zshrc"

    action = link_entry(
        str(src),
        "MacOS/home/.zshrc",
        dry_run=False,
        skip_cred_check=True,
        repo_root=repo,
    )

    assert action == "linked"
    assert src.is_symlink()


def test_wrong_symlink_is_skipped(repo, home, capsys):

    elsewhere = home / "other_file"
    elsewhere.write_text("other\n")

    src = home / ".zshrc"
    src.symlink_to(elsewhere)

    action = link_entry(
        str(src),
        "MacOS/home/.zshrc",
        dry_run=False,
        skip_cred_check=True,
        repo_root=repo,
    )

    assert action == "warn"
    assert src.readlink() == elsewhere  # unchanged


def test_missing_src_and_dest_is_skipped(repo, home):

    action = link_entry(
        str(home / ".nonexistent"),
        "MacOS/home/.nonexistent",
        dry_run=False,
        skip_cred_check=True,
        repo_root=repo,
    )
    assert action == "skip"


def test_credential_check_blocks_move(repo, home):

    src = home / ".zshrc"
    src.write_text("api_key=topsecretvalue123\n")

    action = link_entry(
        str(src),
        "MacOS/home/.zshrc",
        dry_run=False,
        skip_cred_check=False,
        repo_root=repo,
    )

    assert action == "blocked"
    assert src.is_file()  # not moved
    assert not (repo / "MacOS/home/.zshrc").exists()


def test_skip_cred_check_allows_move(repo, home):

    src = home / ".zshrc"
    src.write_text("api_key=topsecretvalue123\n")

    action = link_entry(
        str(src),
        "MacOS/home/.zshrc",
        dry_run=False,
        skip_cred_check=True,
        repo_root=repo,
    )

    assert action == "linked"
