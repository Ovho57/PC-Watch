import time
from rich.progress import track

def scan_progress(files):
    for f in track(files, description="Scanning..."):
        time.sleep(0.2)  