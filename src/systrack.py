#!/usr/bin/env python3
"""
SysTrack - System Diagnostic and Reporting Tool

Main entry point for the CLI application.
"""

import sys
import argparse
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from system_info import get_system_info
from network_check import ping_host
from report_writer import format_report, save_text_report, save_json_report, generate_date_header


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SysTrack - System Diagnostic and Reporting Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 systrack.py --summary
  python3 systrack.py --detailed
  python3 systrack.py --summary --json
  python3 systrack.py --detailed --output reports/
        """
    )
    
    # Report mode options (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--summary',
        action='store_true',
        help='Generate a summary report'
    )
    mode_group.add_argument(
        '--detailed',
        action='store_true',
        help='Generate a detailed report'
    )
    
    # Output format options
    parser.add_argument(
        '--json',
        action='store_true',
        help='Export report as JSON instead of text'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='reports',
        help='Output directory for reports (default: reports)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='google.com',
        help='Host to ping for network diagnostics (default: google.com)'
    )
    
    args = parser.parse_args()
    
    # Determine report mode
    mode = "detailed" if args.detailed else "summary"
    
    try:
        print("Collecting system information...")
        system_info = get_system_info()
        
        print("Checking network connectivity...")
        network_info = ping_host(host=args.host)
        
        # Generate report
        if args.json:
            # Create JSON report
            report_data = {
                'date': generate_date_header(),
                'system': system_info,
                'network': network_info
            }
            report_path = save_json_report(report_data, reports_dir=args.output)
            print(f"\nReport saved: {report_path}")
        else:
            # Create text report
            report_content = format_report(system_info, network_info, mode=mode)
            report_path = save_text_report(report_content, reports_dir=args.output)
            
            # Display report to console
            print("\n" + report_content)
            print(f"\nReport saved: {report_path}")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

