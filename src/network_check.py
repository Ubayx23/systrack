"""
Network Diagnostics Module

Tests network connectivity by pinging a known host.
"""

import subprocess
import platform
from typing import Dict, Any, Optional


def ping_host(host: str = "google.com", timeout: int = 3) -> Dict[str, Any]:
    """
    Ping a host to check network connectivity and measure latency.
    
    Args:
        host: Hostname or IP address to ping (default: google.com)
        timeout: Timeout in seconds (default: 3)
        
    Returns:
        Dictionary containing connectivity status and latency information.
    """
    try:
        # Determine ping command based on OS
        os_name = platform.system().lower()
        
        if os_name == "windows":
            # Windows ping command
            cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
        else:
            # Unix-like systems (macOS, Linux)
            cmd = ["ping", "-c", "1", "-W", str(timeout), host]
        
        # Execute ping command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 1
        )
        
        # Parse ping output for latency
        latency_ms = None
        if result.returncode == 0:
            output = result.stdout.lower()
            
            # Try to extract latency from ping output
            # Format varies by OS, try common patterns
            if "time=" in output or "time<" in output:
                # Unix-like format: time=43.123 ms or time<1 ms
                for line in output.split('\n'):
                    if "time=" in line or "time<" in line:
                        try:
                            # Extract number after time= or time<
                            import re
                            match = re.search(r'time[<=](\d+\.?\d*)', line)
                            if match:
                                latency_ms = float(match.group(1))
                                break
                        except (ValueError, AttributeError):
                            pass
            
            return {
                'online': True,
                'host': host,
                'latency_ms': latency_ms,
                'message': f'Online (Ping {host}: {latency_ms:.0f}ms)' if latency_ms else f'Online (Ping {host}: Success)'
            }
        else:
            return {
                'online': False,
                'host': host,
                'latency_ms': None,
                'message': f'Offline (Unable to reach {host})'
            }
            
    except subprocess.TimeoutExpired:
        return {
            'online': False,
            'host': host,
            'latency_ms': None,
            'message': f'Offline (Timeout connecting to {host})'
        }
    except FileNotFoundError:
        raise RuntimeError("ping command not found. Network diagnostics unavailable.")
    except Exception as e:
        return {
            'online': False,
            'host': host,
            'latency_ms': None,
            'message': f'Offline (Error: {str(e)})'
        }


def format_network_info_summary(network_info: Dict[str, Any]) -> str:
    """
    Format network information as a summary string.
    
    Args:
        network_info: Network information dictionary from ping_host()
        
    Returns:
        Formatted summary string.
    """
    return f"Network: {network_info['message']}"


def format_network_info_detailed(network_info: Dict[str, Any]) -> str:
    """
    Format network information as a detailed string.
    
    Args:
        network_info: Network information dictionary from ping_host()
        
    Returns:
        Formatted detailed string.
    """
    lines = [
        "=== Network Diagnostics ===",
        f"Host Tested: {network_info['host']}",
        f"Status: {'Online' if network_info['online'] else 'Offline'}",
    ]
    
    if network_info['latency_ms'] is not None:
        lines.append(f"Latency: {network_info['latency_ms']:.2f} ms")
    
    lines.append(f"Message: {network_info['message']}")
    
    return "\n".join(lines)

