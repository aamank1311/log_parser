import re
from collections import Counter
from flask import Flask, jsonify

app = Flask(__name__)

logfile_path = "NASA_access_log_Jul95"

# Function to parse the log file and extract requested information
def parse_logfile(logfile_path):
    ip_counter = Counter()
    status_code_counter = {"2xx": Counter(), "3xx": Counter(), "4xx": Counter(), "5xx": Counter()}

    with open(logfile_path, "rb") as file:
        for line in file:
            try:
                line = line.decode("ascii")
            except UnicodeDecodeError:
                continue
            # Extracting IP/Host and Status code
            ip_match = re.search(r'^(\S+)', line)
            status_code_match = re.search(r'\" \d{3}', line)

            if ip_match:
                ip = ip_match.group(1)
                status_code = int(status_code_match.group(0)[2:])

                # Counting requests per IP/Host
                ip_counter[ip] += 1

                # Counting status codes per category
                if 200 <= status_code < 300:
                    status_code_counter["2xx"][ip] += 1
                elif 300 <= status_code < 400:
                    status_code_counter["3xx"][ip] += 1
                elif 400 <= status_code < 500:
                    status_code_counter["4xx"][ip] += 1
                elif 500 <= status_code < 600:
                    status_code_counter["5xx"][ip] += 1


    return ip_counter, status_code_counter


def all_nodes(ip_counter):
    return (ip_counter)


def top_10_hosts(ip_counter):
    # Sort the dictionary based on values in descending order
    sorted_hosts = sorted(ip_counter.items(), key=lambda item: item[1], reverse=True)[:10]
    return sorted_hosts


@app.route("/")
def index():
    return "Welcome to Logfile Parser!"

@app.route("/total")
def total():
    ip_counter, _ = parse_logfile(logfile_path)
    total = all_nodes(ip_counter)
    return jsonify(total)

@app.route("/requests_per_host")
def requests_per_host():
    ip_counter, _ = parse_logfile(logfile_path)
    top_10 = top_10_hosts(ip_counter)
    return jsonify(top_10)

@app.route("/status_codes")
def status_codes():
    _, status_code_counter = parse_logfile(logfile_path)
    status_codes_info = status_codes_per_category(status_code_counter)
    return jsonify(status_codes_info)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

