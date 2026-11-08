from pathlib import Path
import shutil
import json

def quarantine(filename):
    Path("quarantine").mkdir(exist_ok=True)
    shutil.move(filename, "quarantine/" + filename)
    with open("quarantine/manifest.json", "a") as f:
        f.write(json.dumps({"file": filename}) + "\n")

def restore(filename):
    shutil.move("quarantine/" + filename, filename)