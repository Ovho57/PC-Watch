from colors import title, good, bad, header
from terminal_report import show_report
from progress import scan_progress
from quarantine_manager import quarantine
from html_report import make_html
from activity_log import log

header()
input()

results = {
    "added": ["evil.bat"],
    "modified": ["test.py"],
    "missing": ["fake.exe"],
    "suspicious": ["evil.bat"]
}

while True:
    title("-" * 50)
    print("1) Scan  2) Quarantine  3) HTML report  4) Exit")
    choice = input("Pick: ")

    if choice == "1":
        scan_progress(["a.txt", "b.exe", "c.pdf"])
        show_report(results)
        log("scan run")
    elif choice == "2":
        name = input("File to quarantine: ")
        quarantine(name)
        good("Quarantined " + name)
        log("quarantined " + name)
    elif choice == "3":
        make_html(results)
        good("Saved report.html")
        log("html report made")
    elif choice == "4":
        break
    else:
        bad("Invalid option")