from pathlib import Path
import hashlib
import json

bad_endings = (".exe", ".img", ".dll", ".bat", ".cmd", ".scr", ".pif", ".com", ".vbs", ".js", ".jar")
def is_suspicious(file_name):
    return file_name.endswith(bad_endings)

def hash_file(path):
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()    


folder = Path(".")

baseline = {}

for item in folder.iterdir():
    if item.is_file():
        baseline[item.name] = hash_file(item)
    if is_suspicious(item.name):
        print(item.name, item.stat().st_size, "bytes", hash_file(item)[:12], "<-- SUSPICIOUS")
    else:
        print(item.name, item.stat().st_size, "bytes", hash_file(item)[:12])
        
with open("baseline.json", "w") as f:
    json.dump(baseline, f, indent=2)