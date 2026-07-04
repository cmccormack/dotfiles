# Ansible Triage (steamdeck)

Ansible in this portfolio lives only in steamdeck: `playbooks/flatpak.yml`,
`playbooks/remove-launchers.yml`, `inventory/hosts.ini` targeting
`deck@192.168.1.30` with `ansible_python_interpreter=/usr/bin/python3`.
macknet's "Pi maintenance playbook" is bash (`scripts/pi/`), NOT Ansible — see
pi-fleet.md. Interactive runs go through the project `/ansible-run` skill.

## First check

```bash
cd ~/Projects/steamdeck && ansible -i inventory/hosts.ini steamdeck -m ping
```

Green = control node, inventory, SSH, and remote Python all fine — the problem is in the
playbook. UNREACHABLE = stop, fix connectivity first.

## Symptom table

| Symptom | Likely cause | Discriminating check | Fix |
|---|---|---|---|
| `UNREACHABLE!` | Deck asleep/off, SSH not enabled in SteamOS, or IP moved off 192.168.1.30 | `ssh deck@192.168.1.30 true` | Wake Deck, enable SSH on it; if IP moved, check the UniFi client list (api-clients.md) and update hosts.ini |
| `couldn't resolve module/action 'community.general.flatpak'` | Collection not installed | `ansible-galaxy collection list \| grep community.general` | `ansible-galaxy collection install -r requirements.yml` |
| `flatpak_app_id is required` fatal | Playbook pre_task validation | — self-explanatory | Pass `-e "flatpak_app_id=<id>"` or `FLATPAK_APP_ID` env (both supported) |
| `flatpak_state must be present, absent, or latest` | Typo in `-e flatpak_state=...` | — | Use one of the three values |
| `No hosts matched` | Playbooks target `{{ pb_target_host }}` (default group `steamdeck`); an overridden `target_host` isn't in inventory | `grep -A1 '\[steamdeck\]' inventory/hosts.ini` | Fix the group/host name or drop the override |
| `ansible: command not found` | Not installed on the Mac | `which ansible` | `brew install ansible` (per /ansible-run) |
| Task fails writing to system paths on the Deck | SteamOS root filesystem is read-only (unverified beyond the repo's own design choice) | — | Stay in user scope — both playbooks use flatpak `method: user` for exactly this reason; don't add pacman/system-write tasks |

## Traps

- `/ansible-run` recreates a missing `hosts.ini` with
  `ansible_ssh_private_key_file=~/.ssh/id_rsa`; the committed inventory has no key-file
  entry. If auth behavior changes after a "repair", diff the regenerated file against git.
- Run with `-v` (the /ansible-run default) — the flatpak module's real error is often
  only in verbose output.

## Provenance and maintenance

Verified 2026-07-03 against ~/Projects/steamdeck/{inventory/hosts.ini,playbooks/*.yml,requirements.yml,.claude/skills/ansible-run.md}.
Re-verify: `cat ~/Projects/steamdeck/inventory/hosts.ini; ls ~/Projects/steamdeck/playbooks/`
