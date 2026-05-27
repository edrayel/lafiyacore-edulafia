import socket
import logging
import fcntl
import os

logger = logging.getLogger(__name__)

LOCKFILE_PATH = "/tmp/edulafia_ports.lock"

def is_port_in_use(port: int) -> bool:
    """Check if a port is currently bound on localhost (IPv4 or IPv6)."""
    # Check IPv4
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(('127.0.0.1', port))
        except OSError:
            return True

    # Check IPv6 if available on the host OS
    if socket.has_ipv6:
        try:
            with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('::1', port))
        except OSError:
            return True
                
    return False

def find_free_port(start_port: int, max_attempts: int = 100) -> int:
    """Find the next available port starting from start_port, and lock it."""
    if not os.path.exists(LOCKFILE_PATH):
        with open(LOCKFILE_PATH, 'w') as f:
            f.write("")
            
    with open(LOCKFILE_PATH, 'r+') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            locked_ports = set()
            content = f.read().strip()
            if content:
                locked_ports = set(int(p) for p in content.split(',') if p)
                
            # Filter out locked ports that are no longer in use by the OS
            # to handle crashed previous runs
            active_locked_ports = set()
            for p in locked_ports:
                if is_port_in_use(p):
                    active_locked_ports.add(p)
                    
            for port in range(start_port, start_port + max_attempts):
                if port not in active_locked_ports and not is_port_in_use(port):
                    active_locked_ports.add(port)
                    f.seek(0)
                    f.truncate()
                    f.write(','.join(str(p) for p in active_locked_ports))
                    return port
                    
            raise RuntimeError(f"Could not find a free port between {start_port} and {start_port + max_attempts}")
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

def release_ports(ports: list):
    """Remove ports from the lockfile."""
    if not os.path.exists(LOCKFILE_PATH):
        return
        
    with open(LOCKFILE_PATH, 'r+') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            content = f.read().strip()
            if content:
                locked_ports = set(int(p) for p in content.split(',') if p)
                for port in ports:
                    if port in locked_ports:
                        locked_ports.remove(port)
                f.seek(0)
                f.truncate()
                f.write(','.join(str(p) for p in locked_ports))
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
