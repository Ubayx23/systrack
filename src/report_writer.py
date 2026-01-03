"""
Report Writer Module

Handles saving diagnostic reports to files with timestamps.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


def ensure_reports_directory(reports_dir: str = "reports") -> Path:
    """
    Ensure the reports directory exists.
    
    Args:
        reports_dir: Path to reports directory (default: "reports")
        
    Returns:
        Path object for the reports directory.
    """
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)
    return reports_path


def generate_timestamp() -> str:
    """
    Generate a timestamp string for filenames.
    
    Returns:
        Timestamp string in format: YYYY-MM-DD_HH-MM
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M")


def generate_date_header() -> str:
    """
    Generate a date header string for reports.
    
    Returns:
        Date string in format: YYYY-MM-DD
    """
    return datetime.now().strftime("%Y-%m-%d")


def save_text_report(
    content: str,
    reports_dir: str = "reports",
    prefix: str = "sysreport"
) -> str:
    """
    Save a text report to a file.
    
    Args:
        content: Report content as a string
        reports_dir: Directory to save reports (default: "reports")
        prefix: Filename prefix (default: "sysreport")
        
    Returns:
        Path to the saved report file.
    """
    try:
        reports_path = ensure_reports_directory(reports_dir)
        timestamp = generate_timestamp()
        filename = f"{prefix}_{timestamp}.txt"
        filepath = reports_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    except Exception as e:
        raise RuntimeError(f"Failed to save text report: {str(e)}")


def save_json_report(
    data: Dict[str, Any],
    reports_dir: str = "reports",
    prefix: str = "sysreport"
) -> str:
    """
    Save a JSON report to a file.
    
    Args:
        data: Report data as a dictionary
        reports_dir: Directory to save reports (default: "reports")
        prefix: Filename prefix (default: "sysreport")
        
    Returns:
        Path to the saved report file.
    """
    try:
        reports_path = ensure_reports_directory(reports_dir)
        timestamp = generate_timestamp()
        filename = f"{prefix}_{timestamp}.json"
        filepath = reports_path / filename
        
        # Add timestamp to data
        data['timestamp'] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    except Exception as e:
        raise RuntimeError(f"Failed to save JSON report: {str(e)}")


def format_report(
    system_info: Dict[str, Any],
    network_info: Dict[str, Any],
    mode: str = "summary"
) -> str:
    """
    Format a complete diagnostic report.
    
    Args:
        system_info: System information dictionary
        network_info: Network information dictionary
        mode: Report mode - "summary" or "detailed" (default: "summary")
        
    Returns:
        Formatted report string.
    """
    from system_info import format_system_info_summary, format_system_info_detailed, generate_summary_line
    from network_check import format_network_info_summary, format_network_info_detailed
    
    date_header = generate_date_header()
    
    if mode == "detailed":
        system_text = format_system_info_detailed(system_info)
        network_text = format_network_info_detailed(network_info)
    else:
        system_text = format_system_info_summary(system_info)
        network_text = format_network_info_summary(network_info)
    
    header = f"SysTrack Diagnostic Report - {date_header}"
    separator = "-" * len(header)
    
    # Generate summary line
    summary_line = generate_summary_line(system_info, network_info)
    
    lines = [
        header,
        separator,
        "",
        f"System Status: {summary_line}",
        "",
        separator,
        "",
        system_text,
        "",
        network_text
    ]
    
    return "\n".join(lines)

