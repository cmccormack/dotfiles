# Topology and Ownership Map

## Network (UniFi, LAN 192.168.1.0/24)

Source of record: [macknet/inventory/network.yaml](~/Projects/macknet/inventory/network.yaml)
(generated 2026-06-22 from the live controller — regenerate before trusting IPs/versions).

| Device | Model | IP | Notes |
|---|---|---|---|
| "Mack's Place" gateway | UDM Pro | LAN 192.168.1.1 | Controller lives here; WAN eth8 on 192.168.0.79 (upstream 192.168.0.x segment) |
| USW-Lite-16-PoE | USL16LP | 192.168.1.2 | 16-port PoE switch |
| Family Room U6-Lite | UAL6 | 192.168.1.190 | AP |
| Hallway U6-Lite | UAL6 | 192.168.1.237 | AP |
| Laundry Room U6-Lite | UAL6 | 192.168.1.150 | AP |
| Master Bedroom U6-Lite | UAL6 | 192.168.1.144 | AP |

SSIDs: `Mack` (5 GHz), `Mack24` (2.4 GHz), `Mack-Things` (IoT), `Mackprinter`.
A UniFi travel router is used on the road (bookshelf CLAUDE.md; model unverified).

## Hosts

| Host | What | IP | State (2026-07-03) |
|---|---|---|---|
| Mack-NAS | Synology DS918+, DSM 7.1.1-42962, Btrfs `/volume1` | see UniFi clients; DSM API port 5001 | Production — runs CWA ebook stack |
| MackPi4-1 | Pi 4B 4GB | wired 192.168.1.15, wifi .16 | Idle sandbox; being wiped and converted to PiKVM |
| mackpi5 | Pi 5 8GB | wired 192.168.1.145, wifi .18 (fixed) | Dormant Nautobot lab; flagged for reflash (2026-07-02 decision) |
| keylimepi | Pi 4B PiKVM (DIY V2) | `keylimepi.local` | Build in progress (keylimepi repo) |
| Steam Deck OLED | SteamOS handheld | 192.168.1.30 (fixed) | steamdeck repo's target |
| Mack-GamingPC | Windows box | 192.168.1.40 (fixed) | PiKVM's eventual target class |

Real Pi inventory + maintenance history: `macknet/docs/raspberry-pi/fleet.local.md`
(gitignored — real IPs/MACs; never publish).

## Repo ownership

| Repo | Owns | Key entry points |
|---|---|---|
| [macknet](~/Projects/macknet) | Automation hub: UniFi + DSM async clients, Pi fleet playbook, reference docs of record | `src/macknet/{unifi,nas}/client.py`, `docs/INDEX.md`, `scripts/pi/` |
| [bookshelf](~/Projects/bookshelf) | CWA ebook stack on the NAS + Kobo sync | `docker-compose{,.nas}.yml`, `KOBO_SETUP.md`, `setup_cwa.py` |
| [keylimepi](~/Projects/keylimepi) | PiKVM hardware build guide + SD validation | `README.md`, `setup.sh`, `keylimepi.txt` |
| [steamdeck](~/Projects/steamdeck) | Steam Deck troubleshooting, Ansible against the Deck | `playbooks/`, `src/`, `.claude/skills/` |
| [dotfiles](~/Projects/dotfiles) | Global config incl. LIVE `~/.claude` (`Claude/` subtree, symlinked) | `scripts/sync/`, `Claude/` |

## Cross-links (by design, don't duplicate)

- bookshelf defers all NAS platform knowledge (SSH, Docker, DSM, security) to
  `macknet/docs/synology/` — bookshelf CLAUDE.md "Infrastructure" links there directly.
- keylimepi packages the build that `macknet/docs/raspberry-pi/pikvm-upgrade.md` planned
  for MackPi4-1; macknet keeps the decision record, keylimepi the reproducible guide.
- steamdeck notes that subagents inherit only the global dotfiles settings — dotfiles is
  upstream of every repo's Claude behavior.

## Provenance and maintenance
Compiled 2026-07-03 from repo code/docs listed above. Re-verify:
- `head -20 ~/Projects/macknet/inventory/network.yaml` (check `generated_at`; regenerate via `uv run python -m macknet.unifi.inventory` — needs live controller + `.env`)
- `cat ~/Projects/macknet/docs/raspberry-pi/fleet.local.md` (Pi roles/IPs)
- `grep -n "MackNet NAS Docs" ~/Projects/bookshelf/CLAUDE.md` (cross-link intact)
