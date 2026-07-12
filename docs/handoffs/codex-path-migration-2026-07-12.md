# Codex Path Migration Handoff — 2026-07-12

## Project identity

| Field | Value |
| --- | --- |
| Version | `1.0.2` |
| Remote | `https://github.com/kylefu8/Winlinez-Revival.git` |
| Migrated HEAD | `166a76ddafc2f966840b77e622224dec7cfef6c3` |
| Prior Codex thread | `019e5ee1-74d6-7f71-9c30-1bd28f4c953b` |

## Path handoff

- Old path: `E:\SynologyDrive\AI\Projects\Winlinez`
- New canonical Windows path: `E:\AI\Projects\Winlinez`
- The old worktree was clean at migration time.
- The new copy was cloned from the remote and verified at the exact migrated HEAD above.

Do not modify, move, clean, or delete the old Synology worktree. Continue Windows development and verification only from the new canonical path. The supported verification commands are recorded in the repository-root `AGENTS.md`.

## Windows verification

- Interpreter: CPython `3.12.10` at `E:\AI\Projects\Winlinez\.venv\Scripts\python.exe`.
- Dependency install used the `pygame-2.6.1-cp312-cp312-win_amd64.whl` wheel and completed successfully.
- Direct test run: `20 passed in 1.94s`.
- `scripts\build_portable.ps1` completed successfully and repeated the suite with `20 passed in 1.10s`.
- Portable executable: `dist\Winlinez-Revival\Winlinez-Revival.exe` (`13,919,774` bytes; SHA-256 `7DD7F85C2F0E12B7AE3CDF43FB8DEEF99B2CE563B815E04293E9CED106CECAA5`).
- Portable archive: `dist\Winlinez-Revival-portable.zip` (`13,721,113` bytes; SHA-256 `2DC9B1500DB84791ECC8D70C0BA9AAD28D9C4AE48E479A7E549F96B5CD32CDFA`).
