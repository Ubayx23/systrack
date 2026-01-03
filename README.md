# SysTrack

**SysTrack** is a local system diagnostic and reporting tool designed to simulate the type of lightweight monitoring and reporting scripts used by IT support teams and system administrators. It collects essential system information — CPU, memory, disk usage, and network connectivity — then outputs a structured report in both human-readable and file-based formats.

## Overview

This project was built to strengthen technical fundamentals in:

- **System diagnostics** - Interacting with the system through Python
- **File I/O and data logging** - Writing and reading files programmatically
- **Error handling and automation scripting** - Handling edge cases gracefully
- **Command-line interface design** - Building user-friendly CLI tools
- **Git workflow and clean project documentation** - Professional development practices

SysTrack's goal is to demonstrate how automation and scripting can make IT work more efficient — the kind of tool an IT intern or junior systems engineer could realistically build and use.

## Features

✅ **System Information**
- Collect CPU usage, memory usage, disk usage, and OS info using `psutil`

✅ **Network Diagnostics**
- Ping a known host (e.g., google.com) to verify connectivity and latency

✅ **Report Generation**
- Save all collected data into a timestamped file under `/reports`
- Support for both text and JSON output formats

✅ **CLI Commands**
- Simple command flags (`--summary`, `--detailed`)
- Optional JSON export with `--json` flag

✅ **Error Handling**
- Handle cases like no internet, missing permissions, or failed modules gracefully

## Installation

### Option 1: Using a Virtual Environment (Recommended)

This is the recommended approach, especially on macOS with Homebrew Python:

1. **Clone or download this repository**

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify installation:**
   ```bash
   python src/systrack.py --summary
   ```

6. **When done, deactivate the virtual environment:**
   ```bash
   deactivate
   ```

### Option 2: User Installation (Alternative)

If you prefer not to use a virtual environment:

```bash
pip3 install --user -r requirements.txt
```

### Option 3: Quick Setup Script

Run the setup script to automate the process:

```bash
# Make setup script executable (macOS/Linux)
chmod +x setup.sh
./setup.sh

# Or run directly
bash setup.sh
```

**Note:** On macOS with Homebrew Python, you may encounter an "externally-managed-environment" error. Using a virtual environment (Option 1) is the recommended solution.

## Usage

### Basic Usage

**Summary Report:**
```bash
python3 src/systrack.py --summary
```

**Detailed Report:**
```bash
python3 src/systrack.py --detailed
```

### Advanced Options

**Export as JSON:**
```bash
python3 src/systrack.py --summary --json
```

**Custom output directory:**
```bash
python3 src/systrack.py --detailed --output /path/to/reports
```

**Custom ping host:**
```bash
python3 src/systrack.py --summary --host 8.8.8.8
```

### Example Output

**Summary Mode:**
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

**Detailed Mode:**
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
├── src/
│   ├── systrack.py       # main entry point for CLI
│   ├── system_info.py    # collects CPU, memory, disk stats
│   ├── network_check.py  # tests network connectivity
│   ├── report_writer.py  # saves results to /reports
│   └── __init__.py
├── reports/              # auto-generated reports
├── requirements.txt
└── README.md
```

## Tech Stack

- **Language:** Python 3
- **Libraries:**
  - `psutil` - System stats (CPU, memory, disk)
  - `platform` - OS info
  - `subprocess` - Ping commands
  - `json` - JSON file export

## Error Handling

SysTrack handles various error scenarios gracefully:

- **No internet connection** - Reports network as offline with appropriate message
- **Missing permissions** - Provides clear error messages
- **Failed modules** - Catches and reports module import errors
- **Ping command unavailable** - Handles missing ping utility gracefully

## Learning Objectives

By completing this project, you will:

- ✅ Strengthen your confidence with Python scripting for IT tasks
- ✅ Understand how to gather and structure system data
- ✅ Learn how to write and read files programmatically
- ✅ Practice error handling in real scripts
- ✅ Get comfortable with Git feature branches and commits
- ✅ End with a resume-ready technical project that directly maps to IT support responsibilities

## Development

### Running Tests

To test the individual modules:

```python
# Test system info
python3 -c "from src.system_info import get_system_info; print(get_system_info())"

# Test network check
python3 -c "from src.network_check import ping_host; print(ping_host())"
```

### Git Workflow

This project follows a professional Git workflow:

- Each feature (system info, network check, reporting) built in its own branch
- Meaningful commit messages
- Clean README with setup instructions and examples

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Built as a learning project to demonstrate system administration automation skills.

