import socket
import pytest


def _has_network() -> bool:
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except OSError:
        return False


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: tests that require real network access"
    )


def pytest_collection_modifyitems(config, items):
    if not _has_network():
        skip = pytest.mark.skip(reason="no network access")
        for item in items:
            if item.get_closest_marker("integration"):
                item.add_marker(skip)
