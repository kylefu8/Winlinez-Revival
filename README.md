# Winlinez Revival

A portable WinLinez / Color Lines style puzzle game rebuilt with Python and Pygame.

This remake exists because the old Winlinez no longer runs reliably on newer Windows systems, while the game is still loved at home. The goal is to keep the familiar puzzle flow alive in a single-file portable build.

## Download / Release

The portable build is generated at:

```text
dist\Winlinez-Revival\Winlinez-Revival.exe
dist\Winlinez-Revival-portable.zip
```

The exe is self-contained. No installer and no Python installation are required.

## Play from source

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_winlinez.py
```

## Build portable package

```powershell
.\scripts\build_portable.ps1
```

## Save Data

The portable build keeps its best score in `winlinez_high_score.json` beside the exe. Copy that JSON file too only if you want to keep the score record.

## Controls

- Click a ball, then click an empty destination.
- Click `重开` / `New` to start a new game.
- Click `结束` / `Quit` to exit.
- Press `N` or `F2` to start a new game.
- Press `U` or `Backspace` to undo the last valid move.
- Press `Esc` to quit.
- Click `En/中` to switch language.
- Click `i` for the in-game help.
