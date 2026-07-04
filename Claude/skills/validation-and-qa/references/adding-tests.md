# Adding tests to house conventions

Stdlib + pytest only — no new test dependencies without explicit approval (portfolio-wide rule).
Mirror the existing layout of the repo you're in; do not invent a new structure.

## Layout per repo

- **macknet**: `tests/unit/test_<module>.py` and `tests/integration/test_<thing>.py`. Config is in
  `pyproject.toml` `[tool.pytest.ini_options]` — extend markers there, not in a new ini file.
  Anything touching the live controller goes in `tests/integration/` marked `integration`.
- **dotfiles**: tests live NEXT TO the code — `scripts/sync/tests/` and `Claude/tools/tests/` —
  not in a root `tests/`. New tooling gets its own sibling `tests/` dir with its own conftest.
- **steamdeck**: flat `tests/test_<module>.py` importing `src.<module>` from repo root. Remember
  pytest is not a declared dep — runs need `uv run --with pytest pytest tests/`.

## House fixture patterns (copy these, they exist for reasons)

- **Env loading**: macknet root `tests/conftest.py` is just `load_dotenv()` — tests read config
  from `.env`, never hardcode hosts/creds.
- **Live-service fixtures are session-scoped**: macknet's integration `client` fixture wraps
  `async with UnifiClient()` at `scope="session"` to avoid login rate limits. Any new live-client
  fixture must do the same.
- **Protect the real machine**: dotfiles sync tests use an autouse fixture monkeypatching
  `Path.home()` to a tmp_path — any test that could write to `~` needs this pattern.
- **Auto-skip integration when offline**: dotfiles web_fetch conftest probes 8.8.8.8:53 in
  `pytest_collection_modifyitems` and skips `integration`-marked tests without network. Reuse it
  rather than letting integration tests error offline.
- **Script imports**: script dirs (no package) use `sys.path.insert(0, str(Path(__file__).parent.parent))`
  in conftest to import siblings.
- **CLI tools are tested as subprocesses**: web_fetch tests run the tool via a `run_tool()` helper
  and assert the JSON output contract — test the interface users hit, not internals.

## Async

macknet sets `asyncio_mode = "auto"` — write plain `async def test_...`, no decorator. Match
`asyncio_default_fixture_loop_scope = "session"` expectations when adding async fixtures.

## Definition of done for a new test

Predict the new collected count before running; then run the repo's command from
[test-inventory.md](test-inventory.md) and paste output showing old-count → new-count, 0 failed.
Also run the FULL suite once, not just your file.

## Provenance and maintenance

Written 2026-07-03 from direct reads of every conftest.py and test file head in macknet, dotfiles,
and steamdeck. Re-verify: `find ~/Projects/{macknet,dotfiles,steamdeck} -name conftest.py -not
-path '*.venv*' -not -path '*worktree*'` and re-read any that changed since this date.
