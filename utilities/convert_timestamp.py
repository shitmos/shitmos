from datetime import datetime

# List of timestamps
timestamps = [
    1719718503,
    1718210840,
    1718202063,
    1717612067,
    1717115091,
    1717051987,
    1717051628,
    1716937905
]

# Convert timestamps to human-readable format
readable_times = [datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]

# Print the results
for ts, rt in zip(timestamps, readable_times):
    print(f"Timestamp: {ts} -> Human-readable time: {rt}")