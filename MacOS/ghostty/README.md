# Ghostty (macOS)

[View on GitHub](https://github.com/cmccormack/dotfiles/tree/main/MacOS/ghostty)

Reference for Ghostty 1.3.x on macOS, used with tmux. Everything here is the default: the config at `~/Library/Application Support/com.mitchellh.ghostty/config` is the untouched template. Open it with Cmd+, and reload with Cmd+Shift+,. If `~/.config/ghostty/config` also exists, both load (XDG first).

Check live values with `ghostty +list-keybinds --default`, `ghostty +show-config --default --docs`, `ghostty +list-actions`. Official docs: https://ghostty.org/docs/config/reference and https://ghostty.org/docs/config/keybind/reference.

## Tabs and swipe

There is no native two-finger swipe to switch tabs. Next and previous tab are Cmd+Shift+] and Cmd+Shift+[ (also Ctrl+Tab and Ctrl+Shift+Tab). To get iTerm2-style swipes, map a trackpad gesture in BetterTouchTool to those shortcuts, scoped to Ghostty (unverified for Ghostty; TabSwipe lists iTerm2 but not Ghostty).

| Shortcut | Action |
| --- | --- |
| Cmd+T | New tab |
| Cmd+1 to Cmd+8, Cmd+9 | Go to tab N, last tab |
| Cmd+W | Close split, else tab, else window |
| Cmd+Opt+W | Close tab |
| Cmd+Z or Cmd+Shift+T | Reopen recently closed tab, split, or window (`undo-timeout`, 5s) |

## Splits and windows

| Shortcut | Action |
| --- | --- |
| Cmd+D / Cmd+Shift+D | Split right / down |
| Cmd+[ / Cmd+] | Previous / next split |
| Cmd+Opt+Arrow | Focus split in direction |
| Cmd+Ctrl+Arrow | Resize split |
| Cmd+Ctrl+= | Equalize splits |
| Cmd+Shift+Enter | Zoom split |
| Cmd+N | New window |
| Cmd+Enter | Fullscreen |
| Cmd+Shift+P | Command palette |
| Cmd+Opt+I | Inspector |

## Editing, scrollback, search

| Shortcut | Action |
| --- | --- |
| Cmd+Up / Cmd+Down | Jump to previous / next prompt (needs shell integration) |
| Cmd+Left / Cmd+Right | Line start / end |
| Cmd+Backspace | Kill line |
| Opt+Left / Opt+Right | Word back / forward |
| Cmd+K | Clear screen and scrollback |
| Cmd+Home / Cmd+End | Scroll to top / bottom |
| Cmd+F, Cmd+G, Cmd+Shift+G | Search, next, previous |
| Cmd+= / Cmd+- / Cmd+0 | Font size up / down / reset |
| Cmd+Shift+J | Dump screen to a temp file and paste its path |

`toggle_quick_terminal` has no default keybind. Bind it yourself (see below).

## Mouse

| Gesture | Behavior |
| --- | --- |
| Drag | Select; copied on select (`copy-on-select`) |
| Double / triple click | Word / line |
| Cmd+triple-click | Select a command's output (shell integration) |
| Opt+click at a prompt | Move the cursor there (shell integration) |
| Middle click | Paste selection |
| Right click | Context menu (`right-click-action`) |
| Cmd+click | Open URL |
| Shift+drag | Select natively when an app (tmux, vim) has captured the mouse |

## Settings worth setting

Syntax is `key = value`, comments on their own line. Defaults shown.

| Option | Default | Notes |
| --- | --- | --- |
| `font-family`, `font-size` | system, 13 | `ghostty +list-fonts` |
| `theme` | unset | `light:NAME,dark:NAME`; `ghostty +list-themes` |
| `macos-option-as-alt` | true on US layouts | Needed for tmux and readline Meta keys |
| `macos-titlebar-style` | transparent | `native`, `tabs`, `hidden` |
| `window-inherit-working-directory` | true | Needs shell integration |
| `background-opacity`, `background-blur` | 1, false | Blur applies below opacity 1 |
| `scrollback-limit` | 10000000 bytes | Per surface |
| `confirm-close-surface` | true | |
| `notify-on-command-finish` | never | `unfocused` or `always` |
| `clipboard-read` | ask | OSC 52 read prompt |
| `shell-integration-features` | cursor,no-sudo,title,... | Add `no-cursor` to keep your cursor style |

Keybind syntax is `keybind = [prefix:]trigger=action`. Prefixes: `global:` (system wide, needs Accessibility permission), `all:`, `unconsumed:` (key still reaches the program), `performable:`. Remove a default with `keybind = super+d=unbind`. Example:

```
keybind = global:ctrl+grave_accent=toggle_quick_terminal
macos-option-as-alt = true
```

## tmux

| If you see | Check | Fix |
| --- | --- | --- |
| `missing or unsuitable terminal: xterm-ghostty` on a remote host | Remote lacks the terminfo | `infocmp -x xterm-ghostty \| ssh HOST -- tic -x -`, or `SetEnv TERM=xterm-256color` in `~/.ssh/config` |
| `unknown terminal type` under sudo | sudo dropped TERMINFO | `shell-integration-features = sudo` |
| Drag selects in tmux, not Ghostty | tmux `mouse on` owns the mouse | Hold Shift, or `mouse-reporting = false` |
| tmux yanks do not reach the macOS clipboard | OSC 52 | tmux `set -g set-clipboard on`; Ghostty `clipboard-write = allow` (default) |
| Meta keys (`M-b`) fail in tmux | Option not sent as Esc | `macos-option-as-alt = true` |
| Cmd+D, Cmd+T, Cmd+W never reach tmux | Ghostty consumes Cmd combos | `keybind = super+d=unbind`, or `unconsumed:` |
| New Ghostty tab opens in the wrong directory | Ghostty sees the tmux client's cwd, not the pane's | Use tmux splits with `pane_current_path` |
| Scrolling does not show tmux history | tmux owns the alternate screen | Use tmux copy-mode (`prefix [`) and `history-limit` |
| No true color in tmux | tmux unaware of outer RGB | `set -as terminal-features ',xterm-ghostty:RGB'` |

The last five rows are inferred from documented behavior, not stated in Ghostty's docs.
