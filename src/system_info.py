"""
System Information Collection Module

Collects CPU, memory, disk usage, and OS information using psutil.
"""

import psutil
import platform
from typing import Dict, Any


def get_system_info() -> Dict[str, Any]:
    """
    Collect comprehensive system information.
    
    Returns:
        Dictionary containing CPU, memory, disk, and OS information.
    """
    try:
        # CPU information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory information
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_total_gb = memory.total / (1024 ** 3)
        memory_used_gb = memory.used / (1024 ** 3)
        memory_available_gb = memory.available / (1024 ** 3)
        
        # Disk information
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_total_gb = disk.total / (1024 ** 3)
        disk_used_gb = disk.used / (1024 ** 3)
        disk_free_gb = disk.free / (1024 ** 3)
        
        # OS information
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()
        os_platform = platform.platform()
        
        return {
            'cpu': {
                'usage_percent': cpu_percent,
                'core_count': cpu_count
            },
            'memory': {
                'usage_percent': memory_percent,
                'total_gb': round(memory_total_gb, 2),
                'used_gb': round(memory_used_gb, 2),
                'available_gb': round(memory_available_gb, 2)
            },
            'disk': {
                'usage_percent': disk_percent,
                'total_gb': round(disk_total_gb, 2),
                'used_gb': round(disk_used_gb, 2),
                'free_gb': round(disk_free_gb, 2)
            },
            'os': {
                'name': os_name,
                'version': os_version,
                'release': os_release,
                'platform': os_platform
            }
        }
    except Exception as e:
        raise RuntimeError(f"Failed to collect system information: {str(e)}")


def format_system_info_summary(info: Dict[str, Any]) -> str:
    """
    Format system information as a summary string.
    
    Args:
        info: System information dictionary from get_system_info()
        
    Returns:
        Formatted summary string.
    """
    return (
        f"OS: {info['os']['name']} {info['os']['release']}\n"
        f"CPU Usage: {info['cpu']['usage_percent']:.1f}%\n"
        f"Memory Usage: {info['memory']['usage_percent']:.1f}%\n"
        f"Disk Usage: {info['disk']['usage_percent']:.1f}%"
    )


def format_system_info_detailed(info: Dict[str, Any]) -> str:
    """
    Format system information as a detailed string.
    
    Args:
        info: System information dictionary from get_system_info()
        
    Returns:
        Formatted detailed string.
    """
    lines = [
        "=== System Information ===",
        f"Operating System: {info['os']['name']} {info['os']['release']}",
        f"OS Version: {info['os']['version']}",
        f"Platform: {info['os']['platform']}",
        "",
        "=== CPU Information ===",
        f"CPU Usage: {info['cpu']['usage_percent']:.1f}%",
        f"CPU Cores: {info['cpu']['core_count']}",
        "",
        "=== Memory Information ===",
        f"Memory Usage: {info['memory']['usage_percent']:.1f}%",
        f"Total Memory: {info['memory']['total_gb']} GB",
        f"Used Memory: {info['memory']['used_gb']} GB",
        f"Available Memory: {info['memory']['available_gb']} GB",
        "",
        "=== Disk Information ===",
        f"Disk Usage: {info['disk']['usage_percent']:.1f}%",
        f"Total Disk Space: {info['disk']['total_gb']} GB",
        f"Used Disk Space: {info['disk']['used_gb']} GB",
        f"Free Disk Space: {info['disk']['free_gb']} GB",
    ]
    return "\n".join(lines)

