# Raspberry Pi Fleet Triage (macknet fleet + keylimepi/PiKVM)

Fleet rule: **always target the wired IP** — eth0 holds the default route; wlan0 DHCP
can renumber on reboot. Host inventory lives in macknet
`docs/raspberry-pi/devices.md` + gitignored `fleet.local.md`; every fix gets a
maintenance-log entry. Routine maintenance procedure → `homelab-operations`
(macknet `scripts/pi/`: recon → backup-config → update → harden-ssh →
enable-auto-security-updates; backup BEFORE update, always).

## Unreachable Pi — triage order

1. Host down vs network: from the Mac,
   `cd ~/Projects/macknet && uv run python -m macknet.unifi.query` — if the Pi's MAC is
   absent from the controller, it's power/boot/SD; if present on a different IP, DHCP
   renumbered it (was it the wifi IP?).
2. `ping <wired-ip>` then `ssh -o BatchMode=yes chris@<wired-ip> true`.
3. Fix that needs a DHCP reservation or any UniFi change → `change-control` first.
4. Still dead → console (monitor/keyboard) or pull SD.

## Symptom table

| Symptom | Likely cause | Discriminating check | Fix |
|---|---|---|---|
| `Host key verification failed` | Host reimaged, or IP reused by another device | Compare ed25519 fingerprint across its wired+wifi IPs | Confirm same host, then `ssh-keygen -R <ip>` and re-add via `ssh-keyscan` |
| SSH refuses password | Expected post-hardening (`PasswordAuthentication no`) | — | Use the key; key lost → console |
| Locked out after an SSH change | Bad sshd drop-in | — | Console: `sudo rm /etc/ssh/sshd_config.d/99-macknet-hardening.conf && sudo systemctl reload ssh` (harden-ssh.sh gates on `sshd -t` to prevent this) |
| `apt list --upgradable` shows 0 but box is old | **The 0 is a lie** — apt lists frozen; `APT::Periodic` never configured. Real case: both fleet Pis showed 0 while 9 months behind (research a69fef, 2026-06-28) | `stat -c %y /var/lib/apt/lists/*Packages \| sort \| tail -1` — old date = frozen | `sudo apt-get update` first, re-check; ensure `/etc/apt/apt.conf.d/20auto-upgrades` exists (enable-auto-security-updates.sh) |
| "Update pending" after `apt full-upgrade` | New rpi-eeprom firmware staged | `sudo rpi-eeprom-update` (CURRENT vs LATEST) | Reboot to flash; note `/run/reboot-required` is NOT set by firmware updates — reboot anyway |
| Containers gone after reboot | `RestartPolicy=no` by design on the fleet | `docker ps -a` shows Exited | Bring the stack up manually |
| Filesystem read-only / I/O errors | SD card dying | `sudo dmesg \| grep -iE 'mmc\|i/o error'` (standard Linux check, not fleet-specific) | Back up, reflash to a high-endurance card (fleet standard per keylimepi parts list) |
| Fresh flash still has vendor creds | New appliance boot | — | `~/Projects/macknet/scripts/pi/secure-new-ssh-host.sh <user>@<host> <default-pw> --pubkey ~/.ssh/id_ed25519.pub`; password lands in macOS keychain: `security find-generic-password -a <user> -s macknet-ssh-<user>@<host> -w` |

## PiKVM / keylimepi

| Symptom | Likely cause | Discriminating check | Fix |
|---|---|---|---|
| No video / black screen | Target off or unplugged; Geekworm X630 reset jumper wrong | `ssh` to the Pi: `dmesg \| grep tc358743` | X630 jumper must be HW Reset Mode (pins 1–2); reseat CSI ribbon in CAM1 |
| Keyboard/mouse not seen by target | Wrong Pi port or no power splitter | Cable must be in the USB-C OTG port (closest to SD slot) | Add/verify the power splitter — without it, no boot or no HID |
| `keylimepi.local` unreachable | mDNS flaky on some networks | Try the IP from the router DHCP table | Use IP directly; wifi creds live in `keylimepi.txt` |
| Broken first boot after flashing | Raspberry Pi Imager customizations corrupt PiKVM's firstboot | — | Reflash WITHOUT Imager customizations; configure only via `keylimepi.txt`; validate with `./setup.sh /Volumes/PIBOOT` |
| Default creds active | PiKVM ships admin/admin (web) and root/root (SSH) | — | Change web creds in UI; rotate SSH via secure-new-ssh-host.sh |

## Provenance and maintenance

Verified 2026-07-03 against ~/Projects/macknet/{docs/raspberry-pi/troubleshooting.md,scripts/pi/README.md,.claude/research/2026-06-28-pi-adversarial-review-a69fef.md} and ~/Projects/keylimepi/README.md.
Re-verify: `cat ~/Projects/macknet/docs/raspberry-pi/troubleshooting.md; ls ~/Projects/macknet/scripts/pi/`
