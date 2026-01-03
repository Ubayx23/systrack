"""
Network Diagnostics Module

Tests network connectivity by pinging a known host and running Ookla speedtest.
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
    if network_info.get('online') and network_info.get('latency_ms') is not None:
        return f"Network: {network_info['message']}\nPing Time: {network_info['latency_ms']:.0f} ms"
    else:
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
        lines.append(f"Ping Time: {network_info['latency_ms']:.2f} ms")
    
    lines.append(f"Message: {network_info['message']}")
    lines.append("")  # Add trailing newline for consistency
    
    return "\n".join(lines)


def run_ookla_speedtest() -> Dict[str, Any]:
    """
    Run Ookla Speedtest to get detailed network statistics.
    Tries to connect to the closest server in your location.
    
    Returns:
        Dictionary containing download speed, upload speed, ping, and server info.
    """
    try:
        import speedtest
        
        # Create speedtest client with secure=True to use HTTPS (prevents 403 errors)
        st = speedtest.Speedtest(secure=True)
        
        # Get list of all servers
        st.get_servers()
        servers = st.servers
        
        # Try to find closest server by distance
        # This usually gives you a server in your actual location
        st.get_best_server()
        server = st.results.server
        
        # Get more detailed server info
        server_id = server.get('id')
        server_info = None
        if server_id and servers:
            # Find the full server details
            for country_code, server_list in servers.items():
                for srv in server_list:
                    if srv.get('id') == server_id:
                        server_info = srv
                        break
                if server_info:
                    break
        
        # Use server_info if available, otherwise use basic server data
        final_server = server_info if server_info else server
        
        # Run download test
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # Run upload test
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # Get ping from results
        ping_ms = st.results.ping
        
        # Get location details
        location = final_server.get('name', 'Unknown')
        city = final_server.get('name', '').split(',')[0] if ',' in final_server.get('name', '') else location
        country = final_server.get('country', server.get('country', 'Unknown'))
        sponsor = final_server.get('sponsor', server.get('sponsor', 'Unknown'))
        
        return {
            'success': True,
            'download_mbps': round(download_speed, 2),
            'upload_mbps': round(upload_speed, 2),
            'ping_ms': round(ping_ms, 2),
            'server': {
                'name': location,
                'city': city,
                'sponsor': sponsor,
                'country': country,
                'distance': round(server.get('d', 0), 2),
                'id': server_id
            }
        }
    except ImportError:
        return {
            'success': False,
            'error': 'speedtest-cli not installed. Run: pip install speedtest-cli'
        }
    except Exception as e:
        error_msg = str(e)
        # Check for common HTTP errors
        if '403' in error_msg or 'Forbidden' in error_msg:
            return {
                'success': False,
                'error': 'HTTP 403 Forbidden - Ookla servers blocked the request. This may be temporary, please try again later.'
            }
        elif 'HTTPSConnectionPool' in error_msg or 'Connection' in error_msg:
            return {
                'success': False,
                'error': 'Connection error - Unable to reach Ookla servers. Check your internet connection.'
            }
        else:
            return {
                'success': False,
                'error': f'Speedtest failed: {error_msg}'
            }
        


def format_speedtest_results(speedtest_info: Dict[str, Any]) -> str:
    """
    Format Ookla speedtest results as a detailed string.
    
    Args:
        speedtest_info: Speedtest information dictionary from run_ookla_speedtest()
        
    Returns:
        Formatted detailed string.
    """
    if not speedtest_info.get('success'):
        return f"Speedtest Error: {speedtest_info.get('error', 'Unknown error')}"
    
    server = speedtest_info['server']
    lines = [
        "",
        "=== Ookla Speedtest Results ===",
        "",
        "⚠️  DISCLAIMER: Results are estimates based on the test server selected.",
        "   Server location/provider may not reflect your actual location/ISP.",
        "",
        f"Test Server: {server['name']}",
        f"Server Provider: {server['sponsor']}",
        f"Server Location: {server.get('city', server['name'])}, {server['country']}",
        f"Distance to Server: {server['distance']} km",
        "",
        "Network Performance:",
        f"  Ping: {speedtest_info['ping_ms']} ms",
        f"  Download Speed: {speedtest_info['download_mbps']} Mbps",
        f"  Upload Speed: {speedtest_info['upload_mbps']} Mbps",
    ]
    
    return "\n".join(lines)