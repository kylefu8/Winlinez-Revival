# Winlinez Repository Guidance

## Canonical workspace

- Use `E:\AI\Projects\Winlinez` as the Windows working copy.
- Treat `E:\SynologyDrive\AI\Projects\Winlinez` as a read-only legacy source. Do not modify, move, clean, or delete it.

## Supported environment and verification

- Use Python `>=3.12` on Windows. The verified packaging interpreter is CPython 3.12.
- Create the local environment with `py -3.12 -m venv .venv`, then install `requirements.txt`.
- Run the test suite with `.\.venv\Scripts\python.exe -m pytest -q`.
- Run the supported portable-package verification with `.\scripts\build_portable.ps1`.

Keep local environments and generated `build/` and `dist/` outputs untracked; the repository `.gitignore` already excludes them.
