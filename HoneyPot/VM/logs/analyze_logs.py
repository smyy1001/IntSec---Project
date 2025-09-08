import json
import os
from collections import Counter
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

logfile = "log/cowrie.json"
if not os.path.exists(logfile):
    print(f"Log file {logfile} not found!")
    exit(1)

usernames = []
passwords = []
timestamps = []
src_ips = []

with open(logfile, "r") as f:
    for line in f:
        try:
            event = json.loads(line.strip())
            if event.get("eventid") == "cowrie.login.failed":
                usernames.append(event.get("username"))
                passwords.append(event.get("password"))
                src_ips.append(event.get("src_ip"))
                timestamps.append(event.get("timestamp"))
        except json.JSONDecodeError:
            continue

# Prepare DataFrame and export to CSV
df = pd.DataFrame(
    {
        "timestamp": timestamps,
        "username": usernames,
        "password": passwords,
        "src_ip": src_ips,
    }
)
df.to_csv("login_attempts.csv", index=False)
print("✅ CSV exported as 'login_attempts.csv'")

# Display top attackers
print("\nTop 5 Usernames:")
print(Counter(usernames).most_common(5))

print("\nTop 5 Passwords:")
print(Counter(passwords).most_common(5))

# Plotting
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
pd.Series(usernames).value_counts().head(5).plot(kind="bar", title="Top Usernames Used")
plt.xlabel("Username")
plt.ylabel("Attempts")

plt.subplot(1, 2, 2)
pd.Series(passwords).value_counts().head(5).plot(
    kind="bar", title="Top Passwords Used", color="orange"
)
plt.xlabel("Password")
plt.ylabel("Attempts")

plt.tight_layout()
plt.savefig("login_attempts_plot.png")
print("📊 Bar chart saved as 'login_attempts_plot.png'")
