# keylimepi — PiKVM (KVM-over-IP) build

Repo: `~/Projects/keylimepi`. PiKVM V2 on a Raspberry Pi 4B with an HDMI-to-CSI
capture adapter (Geekworm X630 or Waveshare). Mostly a hardware build guide
(README.md) plus a boot-partition config file and a post-flash validation script.
PiKVM = web UI that gives keyboard/video/mouse control of a headless target machine.

## Boot config: `keylimepi.txt`

Copy from the repo to the root of the flashed SD card's boot partition before first
boot; sourced by the firstboot hook. Keys:

| Key | Notes |
|---|---|
| `KEYLIMEPI_HOSTNAME` | default `keylimepi` |
| `KEYLIMEPI_TIMEZONE` | **required** — `timedatectl list-timezones` |
| `KEYLIMEPI_WIFI_SSID/PASS/COUNTRY` | leave commented for Ethernet |
| `KEYLIMEPI_ADMIN_PASS` | PiKVM web UI password; if commented, defaults stay admin/admin — set it |
| `KEYLIMEPI_SSH_PUBKEY` | pubkey for passwordless SSH on first boot |
| `KEYLIMEPI_CAPTURE_RESOLUTION` | `auto`, or e.g. `1920x1080@60` if detect fails |
| `KEYLIMEPI_ATX_ENABLED` | `1` only with ATX header wiring (see README) |

## Post-flash validation: `setup.sh`

Run from the Mac while the SD card is still mounted. Read-only against the card;
exit 0 = all automated checks passed, exit 1 = fix errors before booting.

```bash
cd ~/Projects/keylimepi
./setup.sh /Volumes/PIBOOT        # macOS; Linux: /media/$USER/PIBOOT
```

Checks, in order: boot partition exists; `config.txt`/`cmdline.txt` present
(pikvm/kvmd markers expected); `keylimepi.txt` present with timezone set and
admin password customized. Then prints manual-checklist warnings: PiKVM **V2**
image (not V3/V4); do NOT use Raspberry Pi Imager customization
(hostname/SSH/Wi-Fi corrupt PiKVM firstboot); X630 hardware-reset jumper in HW
Reset Mode (pins 1-2); USB-C power splitter connected (Pi needs simultaneous OTG +
power); CSI ribbon in the Pi's CAM1 port.

Flashing itself is destructive to the target disk — **STOP: double-check the device
node before writing an image; unattended flashing is out (change-control).**
Flashing procedure lives in macknet `docs/raspberry-pi/os-flashing.md`.

## First boot and day-to-day ops

1. Insert SD, connect cables, power on; wait ~60 s (it reboots once during provisioning).
2. Find it: `ping keylimepi.local` (or router DHCP table if mDNS fails).
3. `http://keylimepi.local` — the KeyLimePi dashboard (`dashboard/index.html`;
   deployment mechanism to the Pi is unverified) -> "Open PiKVM UI".
4. Default PiKVM creds admin/admin — change immediately. For the OS `root/root`
   account, rotate attended with macknet's
   `scripts/ssh/secure-new-ssh-host.sh root@<ip> root --pubkey ~/.ssh/id_ed25519.pub`.

PiKVM UI shortcuts: `F11` fullscreen; `Scroll Lock` twice captures/releases
keyboard+mouse; paste-to-target, Ctrl+Alt+Del, and ATX power are UI buttons.
**STOP — ATX power/reset acts on the attached target machine: explicit human go
before power-cycling anything (change-control).**

Quick triage (deeper: debugging-playbook, macknet `docs/raspberry-pi/pikvm.md` and
`pikvm-upgrade.md`):
- No video: target powered + HDMI seated; X630 jumper position;
  `dmesg | grep tc358743` over SSH on the Pi.
- HID dead: OTG is the USB-C port nearest the SD slot; splitter connected.
- `keylimepi.local` unreachable: use the IP; check Wi-Fi creds in `keylimepi.txt`.

## Provenance and maintenance

Documented 2026-07-03 from `~/Projects/keylimepi` source (`setup.sh`,
`keylimepi.txt`, `README.md`). Nothing executed. Re-verify:

```bash
git -C ~/Projects/keylimepi log -1 --format='%h %cs'
grep -n 'KEYLIMEPI_' ~/Projects/keylimepi/keylimepi.txt
grep -n 'section \"' ~/Projects/keylimepi/setup.sh
```
