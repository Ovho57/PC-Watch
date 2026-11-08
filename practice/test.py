file_info = {
    "name": "b.exe",
    "size": "32MB",
    "owner": "Claude",
    "suspicious": "True",
}

print(file_info["name"])
print(file_info["size"])
print(file_info["owner"])
print(file_info["suspicious"])

bad_endings = (".exe", ".img", ".dll", ".bat", ".cmd", ".scr", ".pif", ".com", ".vbs", ".js", ".jar")
def is_suspicious(file_name):
    return file_name.endswith(bad_endings)
files = ["a.txt", "b.exe", "c.img", "d.bat", "e.doc", "f.dll", "g.jpg", "h.cmd", "i.scr", "j.pif", "k.com", "l.vbs", "m.js", "n.jar"]

while True:
    print("===PC WATCH===")
    print("1. create baseline")
    print("2. scan")
    print("3. exit")

    choice = input("pick an option: ")

    if choice == "1":
        print("Creating baseline...")
    elif choice == "2":
        print("Scanning files...")
        for f in files:
            if is_suspicious(f):
                print("Scanning", f, "<-- SUSPICIOUS")
            else:
                print("Scanning", f)
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid option. Please try again.")