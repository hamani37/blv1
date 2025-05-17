from datetime import datetime

def log_message(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)

    with open("logs.txt", "a") as f:
        f.write(line + "\n")
