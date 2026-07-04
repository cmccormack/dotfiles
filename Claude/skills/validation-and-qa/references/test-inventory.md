# Test inventory — verified state as of 2026-07-03

## Suites that exist (run from each repo root)

### macknet — real, structured suite

```
cd ~/Projects/macknet && uv run pytest -m "not integration"
```

Result 2026-07-03: `19 passed, 4 deselected in 0.13s` (Python 3.13.9, pytest-9.0.3,
pytest-asyncio 1.4.0 asyncio_mode=auto, pytest-mock).

- Config lives in `pyproject.toml` `[tool.pytest.ini_options]`: `testpaths = ["tests"]`,
  `asyncio_default_fixture_loop_scope = "session"`, marker `integration: tests that require a live
  UniFi controller`.
- `tests/unit/` mocks aiohttp sessions; `tests/integration/` (the 4 deselected) logs into the live
  controller via a session-scoped `UnifiClient` fixture. Run integration only when the controller
  is reachable and you accept a real login: `uv run pytest -m integration`. Not part of the
  verified core — do not claim it passes without running it.

### dotfiles — two suites, one command

```
cd ~/Projects/dotfiles && uv run pytest scripts/sync/tests/ Claude/tools/tests/ -m "not integration"
```

Result 2026-07-03: `102 passed, 7 deselected, 4 warnings in 6.48s`.

- 7 deselected = web_fetch integration tests (real network; `Claude/tools/tests/conftest.py`
  auto-skips them offline via a socket probe to 8.8.8.8:53).
- 4 warnings = unregistered `@pytest.mark.timeout` in `test_web_fetch.py` (pytest-timeout not
  installed). Pre-existing and benign; if the warning count changes, something else changed.
- No `[tool.pytest.ini_options]` — the two test dirs must be named on the command line.

### steamdeck — passes, but pytest is not a declared dependency

```
cd ~/Projects/steamdeck && uv run --with pytest pytest tests/
```

Result 2026-07-03: `29 passed in 0.08s` (Python 3.14).

- pytest appears nowhere in `pyproject.toml` or `uv.lock` — plain `uv run pytest` fails.
  `--with pytest` is the honest, working invocation. Adding pytest to a dev group is a candidate
  fix; get approval before touching deps.
- Tests are pure-unit (MagicMock'd subprocess, tmp sqlite) — safe to run anywhere.

## No suites

- **bookshelf** — helper scripts only (`setup_cwa.py`, `kobo_set_server.py`, `make_test_pdf.py`).
- **keylimepi** — `setup.sh` + static dashboard; no tooling at all.

## Golden vs untested (2026-07-03)

Verified core: 150 passing tests (macknet 19 + dotfiles 102 + steamdeck 29), all run today.

Untested — treat any claim about these as unevidenced until exercised:
macknet integration (4 tests, live UniFi), web_fetch integration (7 tests, network),
keylimepi `setup.sh`, all bookshelf scripts, steamdeck `playbooks/` (flatpak.yml,
remove-launchers.yml) and its shell scripts, macknet `scripts/pi/*`, dotfiles
`Linux/Raspbian/setup.sh`, dotfiles `vscode/tests/` (node, needs `npm install`).

## Provenance and maintenance

Written 2026-07-03 from live runs of the three commands above (full outputs in
`~/Projects/.claude/research/2026-07-03-skill-validation-and-qa-56e6cb.md`). Re-verify by re-running
the three commands; if counts drift from 19/102/29, update this file and re-date this section.
