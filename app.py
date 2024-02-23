import re
from collections import Counter, defaultdict
from flask import Flask, jsonify
from datetime import datetime
from app import app


app = Flask(__name__)

logfile_path = "NASA_access_log_Jul95"

# Function to parse the log file and extract requested information
def parse_logfile(logfile_path):
    ip_counter = Counter()
    date_format = "%d/%b/%Y"
    status_code_counter = defaultdict(lambda: {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0})


    with open(logfile_path, "rb") as file:
        for line in file:
            try:
                line = line.decode("ascii")
            except UnicodeDecodeError:
                continue
            # Extracting IP/Host, Status code and Date
            ip_match = re.search(r'^(\S+)', line)
            status_code_match = re.search(r'\" \d{3}', line)
            date_match = re.search(r'\[([^:]+):', line)

            if ip_match and status_code_match:
                ip = ip_match.group(1)
                status_code = int(status_code_match.group(0)[2:])
                date_str = date_match.group(1)
                log_date = datetime.strptime(date_str, date_format).date()

                # Counting requests per IP/Host
                ip_counter[ip] += 1

                if log_date.month == 7 and log_date.day >= 1 and log_date.day <= 7:
                    category = get_category(status_code)
                    status_code_counter[log_date.day][category] += 1

    return ip_counter, dict(status_code_counter)

def get_category(status_code):
    if 200 <= status_code < 300:
        return "2xx"
    elif 300 <= status_code < 400:
        return "3xx"
    elif 400 <= status_code < 500:
        return "4xx"
    elif 500 <= status_code < 600:
        return "5xx"

def top_10_hosts(ip_counter):
    # Sort the dictionary based on values in descending order
    sorted_hosts = sorted(ip_counter.items(), key=lambda item: item[1], reverse=True)[:10]
    return sorted_hosts

@app.route("/")
def index():
    return "Welcome to the Logfile Parser platform!"


@app.route("/requests_per_host")
def requests_per_host():
    ip_counter, _ = parse_logfile(logfile_path)
    top_10 = top_10_hosts(ip_counter)
    return jsonify(top_10)

@app.route("/status_codes")
def status_codes():
    _, status_code_counter = parse_logfile(logfile_path)
    return jsonify(status_code_counter)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)

