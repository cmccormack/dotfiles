import pytest
from pathlib import Path
from check_credentials import scan_file, scan, highlight, filter_file


@pytest.fixture
def tmp_file(tmp_path):
    """Helper that writes content to a temp file and returns its Path."""
    def _write(content: str) -> Path:
        p = tmp_path / "test.txt"
        p.write_text(content)
        return p
    return _write


# --- scan_file ---

def test_clean_file_has_no_findings(tmp_file):
    assert scan_file(tmp_file("export EDITOR=vim\nalias ll='ls -la'\n")) == []


def test_aws_access_key_detected(tmp_file):
    hits = scan_file(tmp_file("export AWS_KEY=AKIAIOSFODNN7EXAMPLE\n"))
    assert any(label == "AWS access key ID" for _, label, _, _ in hits)


def test_github_token_detected(tmp_file):
    hits = scan_file(tmp_file("TOKEN=ghp_abcdefghijklmnopqrstuvwxyz12345678\n"))
    assert any(label == "GitHub token" for _, label, _, _ in hits)


def test_bearer_token_detected(tmp_file):
    hits = scan_file(tmp_file("Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\n"))
    assert any(label == "Bearer token" for _, label, _, _ in hits)


def test_url_with_credentials_detected(tmp_file):
    hits = scan_file(tmp_file("DATABASE_URL=postgres://admin:s3cr3tpassword@db.example.com/mydb\n"))
    assert any(label == "credential in URL" for _, label, _, _ in hits)


def test_pem_key_detected(tmp_file):
    hits = scan_file(tmp_file("-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA...\n"))
    assert any(label == "PEM private key" for _, label, _, _ in hits)


def test_generic_credential_assignment_detected(tmp_file):
    hits = scan_file(tmp_file("api_key=supersecretvalue123\n"))
    assert any(label == "credential assignment" for _, label, _, _ in hits)


def test_stripe_key_detected(tmp_file):
    # Split literal so static secret scanners don't flag this source file
    hits = scan_file(tmp_file("STRIPE_KEY=" + "sk_live_" + "abcdefghijklmnopqrstuvwx\n"))
    assert any(label == "Stripe key" for _, label, _, _ in hits)


def test_slack_token_detected(tmp_file):
    # Split literal so static secret scanners don't flag this source file
    hits = scan_file(tmp_file("SLACK_TOKEN=" + "xoxb-" + "123456789012-abcdefghijklmnop\n"))
    assert any(label == "Slack token" for _, label, _, _ in hits)


def test_match_is_captured(tmp_file):
    hits = scan_file(tmp_file("TOKEN=ghp_abcdefghijklmnopqrstuvwxyz12345678\n"))
    _, _, _, match = hits[0]
    assert match == "ghp_abcdefghijklmnopqrstuvwxyz12345678"


def test_only_one_finding_per_line(tmp_file):
    # A line matching multiple patterns should still produce one finding
    hits = scan_file(tmp_file("api_key=AKIAIOSFODNN7EXAMPLE\n"))
    assert len(hits) == 1


def test_line_number_is_correct(tmp_file):
    content = "name=chris\npassword=hunter2\nalias ll='ls -la'\n"
    hits = scan_file(tmp_file(content))
    assert hits[0][0] == 2  # line 2


def test_template_placeholders_not_flagged(tmp_file):
    # ${VAR} and $VAR substitutions are not real credentials
    hits = scan_file(tmp_file("password=${DB_PASSWORD}\ntoken=$MY_TOKEN\n"))
    assert hits == []


def test_json_escaped_sudo_prompt_not_flagged(tmp_file):
    # "Password:\n0" in JSON history is a sudo prompt, not a credential value
    hits = scan_file(tmp_file(r'{"display":"Password:\n0\n\n[Pasted text]"}' + "\n"))
    assert hits == []


def test_unreadable_file_returns_empty(tmp_path):
    p = tmp_path / "locked.txt"
    p.write_text("secret=abc123\n")
    p.chmod(0o000)
    try:
        assert scan_file(p) == []
    finally:
        p.chmod(0o644)


# --- highlight ---

def test_highlight_wraps_match_in_ansi(tmp_file):
    result = highlight("api_key=supersecret", "supersecret")
    assert "\033[1;31m" in result
    assert "supersecret" in result
    assert result.index("\033[1;31m") < result.index("supersecret")


def test_highlight_only_replaces_first_occurrence():
    result = highlight("token=abc token=abc", "abc")
    assert result.count("\033[1;31m") == 1


# --- scan (directory) ---

def test_scan_directory_finds_all_files(tmp_path):
    (tmp_path / "a.txt").write_text("TOKEN=ghp_abcdefghijklmnopqrstuvwxyz12345678\n")
    (tmp_path / "b.txt").write_text("nothing sensitive here\n")
    (tmp_path / "c.txt").write_text("AKIA1234567890ABCDEF\n")

    results = scan(tmp_path)
    assert len(results) == 2
    assert tmp_path / "b.txt" not in results


def test_scan_single_file(tmp_path):
    p = tmp_path / "creds.txt"
    p.write_text("api_key=topsecret\n")
    results = scan(p)
    assert p in results


def test_scan_clean_directory_returns_empty(tmp_path):
    (tmp_path / "a.sh").write_text("echo hello\n")
    (tmp_path / "b.sh").write_text("export PATH=$HOME/bin:$PATH\n")
    assert scan(tmp_path) == {}


# --- filter_file ---

def test_filter_file_removes_flagged_lines(tmp_path):
    p = tmp_path / "history"
    p.write_text("echo hello\ncurl -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' api.example.com\necho done\n")
    removed = filter_file(p)
    assert len(removed) == 1
    assert removed[0][0] == 2  # line 2
    lines = p.read_text().splitlines()
    assert lines == ["echo hello", "echo done"]


def test_filter_file_clean_file_unchanged(tmp_path):
    p = tmp_path / "history"
    p.write_text("echo hello\nalias ll='ls -la'\n")
    removed = filter_file(p)
    assert removed == []
    assert p.read_text() == "echo hello\nalias ll='ls -la'\n"


def test_filter_file_returns_findings(tmp_path):
    p = tmp_path / "history"
    p.write_text("export AWS_KEY=AKIAIOSFODNN7EXAMPLE\n")
    removed = filter_file(p)
    assert any(label == "AWS access key ID" for _, label, _, _ in removed)
    assert p.read_text() == ""
