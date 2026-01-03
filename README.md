# SysTrack

## Overview

SysTrack is a lightweight system diagnostic and reporting tool designed for IT support professionals and system administrators. It provides essential insights into your system’s CPU, memory, disk usage, and network connectivity. Built as a working prototype, SysTrack aims to streamline routine system checks through automation and scripting, serving as a practical foundation for further development.

## Features

- **Comprehensive System Metrics:** Gather real-time CPU, memory, disk, and OS information using `psutil`.
- **Network Connectivity Testing:** Perform ping tests to verify network status and latency.
- **Flexible Reporting:** Generate timestamped reports in both human-readable text and JSON formats.
- **Interactive Web Interface:** Access a terminal-like web UI for real-time diagnostics and command execution.
- **Command-Line Interface:** Use simple commands and flags for quick system summaries or detailed reports.
- **Robust Error Handling:** Gracefully manage issues like no internet connection, permission errors, and missing dependencies.

## Installation

### Recommended: Virtual Environment Setup

1. Clone or download the repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Verify installation:
   ```bash
   python src/systrack.py --summary
   ```
6. Deactivate when finished:
   ```bash
   deactivate
   ```

### Alternative Installation Options

- **User Installation:**
  ```bash
  pip3 install --user -r requirements.txt
  ```
- **Quick Setup Script (macOS/Linux):**
  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```

> **Note:** Using a virtual environment is highly recommended to avoid environment conflicts, especially on macOS with Homebrew Python.

## Usage

### Web Interface (Recommended)

Start the Flask server:
```bash
python app.py
```
Open your browser to `http://localhost:8080` and interact with SysTrack via the terminal-like interface. Use commands like:

- `help` — List available commands
- `summary` — Generate a quick system report
- `detailed` — Generate a comprehensive system report
- `ping [host]` — Test network connectivity
- `clear` — Clear the terminal display

### Command-Line Interface

Generate reports directly from the terminal:

- Summary report:
  ```bash
  python3 src/systrack.py --summary
  ```
- Detailed report:
  ```bash
  python3 src/systrack.py --detailed
  ```
- Export as JSON:
  ```bash
  python3 src/systrack.py --summary --json
  ```
- Specify output directory:
  ```bash
  python3 src/systrack.py --detailed --output /path/to/reports
  ```
- Custom ping host:
  ```bash
  python3 src/systrack.py --summary --host 8.8.8.8
  ```

## Example Output

**Summary Report:**
```
SysTrack Diagnostic Report - 2026-01-02
----------------------------------------
OS: macOS 15.1
CPU Usage: 37.0%
Memory Usage: 68.0%
Disk Usage: 55.0%
Network: Online (Ping google.com: 43ms)

Report saved: reports/sysreport_2026-01-02_14-32.txt
```

**Detailed Report:**
```
SysTrack Diagnostic Report - 2026-01-02
----------------------------------------

=== System Information ===
Operating System: macOS 15.1
OS Version: Darwin Kernel Version 24.1.0
Platform: macOS-15.1-x86_64-i386-64bit

=== CPU Information ===
CPU Usage: 37.0%
CPU Cores: 8

=== Memory Information ===
Memory Usage: 68.0%
Total Memory: 16.0 GB
Used Memory: 10.88 GB
Available Memory: 5.12 GB

=== Disk Information ===
Disk Usage: 55.0%
Total Disk Space: 500.0 GB
Used Disk Space: 275.0 GB
Free Disk Space: 225.0 GB

=== Network Diagnostics ===
Host Tested: google.com
Status: Online
Latency: 43.00 ms
Message: Online (Ping google.com: 43ms)

Report saved: reports/sysreport_2026-01-02_14-32.txt
```

## Project Structure

```
systrack/
├── app.py                # Flask web application entry point
├── src/
│   ├── systrack.py       # CLI entry point
│   ├── system_info.py    # Collects CPU, memory, disk stats
│   ├── network_check.py  # Performs network connectivity tests
│   ├── report_writer.py  # Saves reports to /reports
│   └── __init__.py
├── templates/
│   └── index.html        # Web terminal interface
├── static/
│   ├── css/
│   │   └── terminal.css  # Terminal styling
│   └── js/
│       └── terminal.js   # Terminal interaction logic
├── reports/              # Auto-generated reports
├── requirements.txt
├── setup.sh              # Setup script (macOS/Linux)
├── setup.bat             # Setup script (Windows)
└── README.md
```

## Tech Stack

- **Language:** Python 3
- **Web Framework:** Flask
- **Core Libraries:**
  - `psutil` — System metrics (CPU, memory, disk)
  - `platform` — Operating system details
  - `subprocess` — Network ping commands
  - `json` — Report serialization

## Known Limitations

- **Ping Accuracy:** Network latency measurements depend on the underlying OS ping utility and may vary. Results should be interpreted as approximate.
- **Detailed Report Accuracy:** Some system information, especially platform-specific details, may not be fully accurate or available on all operating systems.
- **Prototype Status:** SysTrack is a work in progress. Features and interfaces may change, and some edge cases are still under refinement.
- **Permissions:** Certain metrics may require elevated permissions; lack thereof can limit data collection.

## Next Steps

- Enhance network diagnostics with multi-host ping and traceroute capabilities.
- Improve web interface with session persistence and enhanced command history.
- Add automated scheduling and alerting features.
- Expand OS compatibility and detailed hardware profiling.
- Implement comprehensive unit and integration tests.

---

SysTrack provides a solid foundation for system monitoring and diagnostics, combining automation with ease of use. Contributions and feedback are welcome as the project evolves.
