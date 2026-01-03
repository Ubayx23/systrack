"""
SysTrack - System Diagnostic and Reporting Tool

A lightweight monitoring and reporting tool for system administrators.
"""

__version__ = "1.0.0"
__author__ = "SysTrack Team"

from .system_info import get_system_info
from .network_check import ping_host
from .report_writer import format_report, save_text_report, save_json_report

__all__ = [
    'get_system_info',
    'ping_host',
    'format_report',
    'save_text_report',
    'save_json_report',
]

