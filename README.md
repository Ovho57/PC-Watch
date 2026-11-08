# PC Watch

PC Watch is a simple, local file and folder change monitor. It watches a folder you select and quickly reports added, modified, or missing files and folders, including their modified date and time.

It is a basic change-monitoring tool, not a full antivirus product. It does not upload, delete, or change your files.

## Features

- Simple 3-option terminal menu.
- Fast checks using file/folder metadata (size and modified time); no SHA-256 hashing.
- Detects newly added, modified, and missing files and folders.
- Shows the path and modification date/time for detected items.
- Saves reports locally in JSON format.
- Works on Windows, macOS, and Linux.

## Requirements

- Python 3.10+
- Git (if cloning the repository)

## Install on Windows

Install Python from https://www.python.org/downloads/ and enable **Add Python to PATH**.

Open PowerShell and run:

```powershell
git clone https://github.com/Ovho57/PC-Watch.git
cd PC-Watch
python -m pip install -r requirements.txt
python main.py
```

For later updates, run these commands from inside the PC-Watch folder:

```powershell
git pull origin main
python -m pip install -r requirements.txt
python main.py
```

## How to use

1. Run `python main.py`.
2. On first launch, choose the folder you want monitored.
3. PC Watch records a quick starting snapshot.
4. Use the menu:
   - **1 — View changes:** display added, modified, and missing files/folders with dates and times.
   - **2 — Change monitored folder / reset starting point:** select a folder and establish a new snapshot.
   - **3 — Exit.**

Reports are saved under `~/.pcwatch/reports` (on Windows, inside your user profile).

## Important limitations

- This version uses file size and modified time, not file contents. A change that preserves both size and modification time may not be detected.
- If you select option 2, it replaces the starting snapshot. Review changes before doing this if you want to keep the previous baseline.
- PC Watch does not prove a file is malicious and is not a replacement for Windows Security or another antivirus.
- Start by monitoring a folder you understand. Avoid selecting the entire Windows drive.

## Project structure

```
PC-Watch/
├── main.py
├── pcwatch/
│   ├── __init__.py
│   └── scanner.py
├── requirements.txt
├── README.md
└── .gitignore
```

## License

Educational and personal defensive use. Add a formal license before redistribution.
