import paramiko
import time
from datetime import datetime

# Cowrie listens on port 2222 of localhost (DONT FORGET VirtualBox port forwarding!)
HOST = "127.0.0.1"
PORT = 2222
LOG_FILE = "simulation_results.txt"

# A list of fake username/password pairs to simulate an attack
credentials = [
    ("admin", "admin123"),
    ("root", "toor"),
    ("test", "testpass"),
    ("user", "letmein"),
    ("ubuntu", "password"),
    ("cowrie", "123456"),
    ("admin", "qwerty"),
    ("oracle", "oracle123"),
]

def log_and_print(message):
    """Print to console and write to log file"""
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def attempt_login(username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(HOST, port=PORT, username=username, password=password, timeout=3)
    except paramiko.AuthenticationException:
        log_and_print(f"[FAIL] {username}:{password}")
    except Exception as e:
        log_and_print(f"[ERROR] {username}:{password} -> {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    log_and_print("🚀 Starting attack simulation...")
    for username, password in credentials:
        attempt_login(username, password)
        time.sleep(1)  # Delay to mimic attack (not a must but realistic)
    log_and_print("✅ Attack simulation completed.")
