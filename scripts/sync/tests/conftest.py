import sys
from pathlib import Path

import pytest

# Allow tests to import sibling scripts directly
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(autouse=True)
def block_real_home(tmp_path, monkeypatch):
    """Redirect Path.home() to a temp dir so tests can't touch the real home."""
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path / "home"))
