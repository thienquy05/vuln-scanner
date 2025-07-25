Python Port Scanner

A simple, terminal-based Python script for scanning open ports on target IP addresses to identify network vulnerabilities. This tool uses multithreading to improve scanning speed and saves the results in both a text file and a SQLite database.

Features ✨
Concurrent Scanning: Uses multithreading to scan multiple ports at once, significantly speeding up the process.
Flexible Target Input: Reads a list of target IP addresses from a targets.txt file.
Customizable Port Range: Allows the user to specify a range of ports to scan at runtime.
Banner Grabbing: Attempts to retrieve the banner of any open port to identify the running service.
Dual Output: Saves scan results in a human-readable scan_results.txt file and a structured SQLite database (scanner.db).

How It Works ⚙️
The script reads the target IP addresses from targets.txt. For each IP address, it iterates through the user-defined port range. A new thread is created for each port scan to enable concurrent execution. The script uses a TCP connect scan to determine if a port is open. If a port is open, it attempts to grab the service banner. All results (both open and closed ports) are timestamped and stored in the SQLite database, while open ports are also logged in scan_results.txt.

Requirements 📋
Python 3.x
colorama library

Usage 🚀
Clone the repository:

Bash
git clone https://github.com/thienquy05/vuln-scanner.git
cd vuln-scanner
Install dependencies:

Bash
pip install colorama
Add Target IPs:
Create a targets.txt file and add the IP addresses you want to scan, with one IP per line.
127.0.0.1
8.8.8.8
Run the scanner:

Bash
python scanner.py
Enter the port range when prompted (e.g., 20-80).

Output 📄
scan_results.txt: A text file containing a list of open ports for each scanned IP address.
scanner.db: A SQLite database file containing detailed scan results, including IP, port, status, banner, and timestamp. You can use any SQLite browser to view the contents of this file.

Disclaimer ⚠️
This tool is intended for educational purposes and for use in authorized security testing scenarios only. Unauthorized scanning of networks is illegal. The user is responsible for their own actions.