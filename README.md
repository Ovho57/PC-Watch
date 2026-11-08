# PC Watch

PC Watch is a local file-integrity monitoring utility. It records a SHA-256 baseline for a folder you choose, then compares later scans to identify files that were added, modified, or missing.

It is an early defensive tool, not a full antivirus product. It does not upload your files, delete files, or silently change your system. A suspicious-looking file extension is only a review hint and is not proof of malware.

## Features

- Create a SHA-256 baseline of a user-selected directory.
- Detect added, modified, and missing files compared with the baseline.
- Flag selected executable/script extensions for manual review.
- Save JSON scan reports locally.
- Skip symbolic links and report inaccessible-file counts.
- Runs on Windows, macOS, and Linux with Python.

## Requirements

- Python 3.10 or newer
- Internet connection only for downloading the repository and Python packages
- No administrator privileges required for normal use

## Install on Windows

### 1. Install Python

Download Python from [python.org](https://www.python.org/downloads/). During setup, enable **Add Python to PATH**.

Check the installation in Command Prompt or PowerShell:

```powershell
python --version
```

### 2. Download PC Watch

**Option A — Git:**

Install Git from [git-scm.com](https://git-scm.com/downloads), then run:

```powershell
git clone https://github.com/Ovho57/PC-Watch.git
cd PC-Watch
```

**Option B — ZIP:**

1. Open the repository page: https://github.com/Ovho57/PC-Watch
2. Click **Code**.
3. Select **Download ZIP**.
4. Extract the ZIP.
5. Open the extracted `PC-Watch` folder.

### 3. Install dependencies

Run in the repository folder:

```powershell
python -m pip install -r requirements.txt
```

### 4. Start PC Watch

```powershell
python main.py
```

## Install on macOS or Linux

Make sure Python 3.10+ is installed, then:

```bash
git clone https://github.com/Ovho57/PC-Watch.git
cd PC-Watch
python3 -m pip install -r requirements.txt
python3 main.py
```

## First use

1. Choose **Create or replace baseline**.
2. Paste the full path to a folder you want to monitor. Start with a small test folder.
3. Confirm the baseline creation.
4. Later, choose **Scan against baseline**.
5. Review the added, modified, missing, and extension-review results.
6. PC Watch writes JSON reports under `~/.pcwatch/reports` (Windows: your user profile's `.pcwatch\reports` folder).

### Example test

Create a new folder such as `PCWatch-Test`, put a few harmless text files inside, and make a baseline. Then add or edit a text file and run a scan. PC Watch should report the change.

## Important notes

- A baseline represents the folder at the time you created it. If you intentionally update files, create a new baseline after checking those changes.
- File changes can be legitimate software updates. Always review results before taking action.
- Extension-based review is not antivirus detection. A file with an executable extension may be completely legitimate.
- PC Watch currently does not scan memory, network traffic, browser activity, startup persistence, or running processes.
- Do not baseline your entire Windows drive at first. Choose a small folder you understand.
- Keep the baseline and reports private if they reveal filenames from your computer.

## Project structure

```text
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

This project is currently provided for educational and personal defensive use. Add a formal license before redistributing it.
