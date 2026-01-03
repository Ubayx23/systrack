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
from network_check import ping_host, run_ookla_speedtest, format_speedtest_results
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
            output = run_ping() # Run Ookla speedtest
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
ping             - Run network speed test (Ookla Speedtest)
                  Takes 30-60 seconds, shows download/upload speeds
clear, cls       - Clear the terminal screen

Examples:
  summary
  detailed
  ping
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


def run_ping(host=None):
    """Run ping test and Ookla speedtest for detailed network diagnostics."""
    try:
        result_lines = []
        
        # If ping succeeded, run Ookla speedtest for detailed stats
        result_lines.append("Running network speed test...")
        result_lines.append("This may take 30-60 seconds, please wait...")
        result_lines.append("")
        result_lines.append("Note: Results show the test server location, which may differ from your actual location.")
        result_lines.append("")
        
        speedtest_info = run_ookla_speedtest()
        speedtest_output = format_speedtest_results(speedtest_info)
        result_lines.append(speedtest_output)
        
        return "\n".join(result_lines)
    except Exception as e:
        return f"Error running network diagnostics: {str(e)}"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)

