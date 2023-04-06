import pandas as pd
import re
import csv
with open("ue2.txt", "r") as f:
    logs = f.readlines()

# Define a regex pattern to match the timestamp format
timestamp_regex = r'\b\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\b'

# Extract the timestamp, log level, module name, STA, WLAN, and remaining text from each string
data = []
prev_line = ""
for log in logs:
    # check if the line starts with the specified timestamp format
    if re.match(timestamp_regex, log):
        # if the previous line exists, append it to the data list
        if prev_line:
            data.append(prev_line)
        prev_line = log.strip()
    else:
        # append the current line to the previous line (if it exists)
        if prev_line:
            prev_line += " " + log.strip()
        else:
            prev_line = log.strip()

# append the last line (if it exists) to the data list
if prev_line:
    data.append(prev_line)

# Write the updated data to the same file
with open("ue2.txt", "w") as f:
    for line in data:
        f.write(line + "\n")

pd.set_option("display.max_colwidth", 1000)

# Read the log file into a list of strings, appending lines that do not start with a timestamp to the previous line
with open("ue2.txt", "r") as f:
    lines = []
    prev_line = ""
    for line in f:
        if re.match(r"^\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}", line):
            if prev_line:
                lines.append(prev_line.strip())
                prev_line = ""
            lines.append(line.strip())
        else:
            prev_line += " " + line.strip()
    if prev_line:
        lines.append(prev_line.strip())

# Extract the timestamp, log level, module name, STA, WLAN, and remaining text from each string
data = []
sta_regex = r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b'
timestamp_regex = r'^\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}'
for log in lines:
    timestamp_match = re.match(timestamp_regex, log)
    if timestamp_match:
        timestamp = timestamp_match.group(0)
        log = log.split("RuckusAP ")[1]
        log_level, module_name_and_string = log.split(" ", 1)
        module_name, string_left = module_name_and_string.split(None, 1)
        sta_match = re.search(sta_regex, string_left)
        sta = sta_match.group(0) if sta_match else ""
        wlan_match = re.search(r"wlan\d+", string_left)
        wlan = wlan_match.group(0) if wlan_match else ""
        remaining_text = string_left.replace(sta, "").replace(wlan, "").strip()
        data.append([timestamp, log_level, module_name, sta, wlan, remaining_text])

# Store the data in a Pandas DataFrame and print it
df = pd.DataFrame(data, columns=["Timestamp", "Log level", "Module name", "STA", "WLAN", "Text"])
df.to_csv("ue_2up.csv", index=False)

with open('ue_2up.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    sta_data = {}
    
    for row in reader:
        sta = row['STA']
        if sta not in sta_data:
            sta_data[sta] = []
        sta_data[sta].append(row)

with open('ue_2up.csv', 'w', newline='') as csvfile:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, (sta, data) in enumerate(sta_data.items()):
        if i > 0:
            # Add a few blank rows to separate different "sta" values
            writer.writerow({})
            writer.writerow({})
            writer.writerow({})
        for row in data:
            writer.writerow(row)
#print(df)


