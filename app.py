"""
SysTrack Web Application
Flask-based web interface with terminal-like UI
"""

from flask import Flask, render_template, jsonify, request
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from system_info import get_system_info
from network_check import ping_host
from report_writer import format_report, save_text_report, save_json_report, generate_date_header

app = Flask(__name__)


@app.route('/')
def index():
    """Main page with terminal interface."""
    return render_template('index.html')


@app.route('/api/command', methods=['POST'])
def execute_command():
    """Execute a command and return the result."""
    data = request.get_json()
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'output': '', 'error': 'No command provided'}), 400
    
    # Parse command
    parts = command.split()
    cmd = parts[0].lower() if parts else ''
    args = parts[1:] if len(parts) > 1 else []
    
    try:
        if cmd == 'help' or cmd == '?':
            output = get_help_text()
        elif cmd == 'summary':
            output = run_summary_report()
        elif cmd == 'detailed':
            output = run_detailed_report()
        elif cmd == 'ping':
            host = args[0] if args else 'google.com'
            output = run_ping(host)
        elif cmd == 'clear' or cmd == 'cls':
            output = 'CLEAR_SCREEN'
        else:
            output = f"Unknown command: {cmd}\nType 'help' for available commands."
        
        return jsonify({'output': output, 'error': None})
    except Exception as e:
        return jsonify({'output': '', 'error': str(e)}), 500


def get_help_text():
    """Return help text for available commands."""
    return """SysTrack Terminal Commands
========================
help, ?          - Show this help message
summary          - Generate summary system report
detailed         - Generate detailed system report
ping [host]      - Test network connectivity (default: google.com)
clear, cls       - Clear the terminal screen

Examples:
  summary
  detailed
  ping 8.8.8.8
  clear
"""


def run_summary_report():
    """Run and return summary report."""
    try:
        system_info = get_system_info()
        network_info = ping_host()
        report = format_report(system_info, network_info, mode="summary")
        
        # Save report
        report_path = save_text_report(report)
        
        return f"{report}\n\nReport saved: {report_path}"
    except Exception as e:
        return f"Error generating report: {str(e)}"


def run_detailed_report():
    """Run and return detailed report."""
    try:
        system_info = get_system_info()
        network_info = ping_host()
        report = format_report(system_info, network_info, mode="detailed")
        
        # Save report
        report_path = save_text_report(report)
        
        return f"{report}\n\nReport saved: {report_path}"
    except Exception as e:
        return f"Error generating report: {str(e)}"


def run_ping(host):
    """Run ping test and return result."""
    try:
        network_info = ping_host(host)
        if network_info['online']:
            latency = network_info['latency_ms']
            if latency:
                return f"Ping {host}: {latency:.2f}ms - Online"
            else:
                return f"Ping {host}: Success - Online"
        else:
            return f"Ping {host}: {network_info['message']}"
    except Exception as e:
        return f"Error pinging {host}: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

