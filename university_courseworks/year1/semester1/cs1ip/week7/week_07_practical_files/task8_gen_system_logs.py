from datetime import datetime, timedelta
import random

# Define log file path
log_file_path = "system_logs.txt"

# Log severity levels
severity_levels = ["INFO", "ERROR", "WARNING"]

# Generate log entries with 50-100 entries for each severity level

# Base time for log entries
start_time = datetime.now()

# Collect all log entries
log_entries = []
for severity in severity_levels:
    num_entries_per_level = random.randint(50, 100)
    for _ in range(num_entries_per_level):
        # Generate a random timestamp
        timestamp = start_time.strftime("[%Y-%m-%d %H:%M:%S]")
        log_message = f"{timestamp} {severity} Sample log message."
        log_entries.append(log_message)
        # Increment time for variety
        start_time += timedelta(seconds=random.randint(1, 100))

# Shuffle the log entries to mix severity levels
random.shuffle(log_entries)

# Write the log entries to system_logs.txt
with open(log_file_path, "w") as file:
    file.write("\n".join(log_entries))

