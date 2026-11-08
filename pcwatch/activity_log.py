from datetime import datetime

def log(message):
    with open("activity_log.txt", "a") as f:
        f.write(str(datetime.now()) [:19] + "  " + message + "\n")
        