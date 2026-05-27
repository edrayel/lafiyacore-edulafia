#!/usr/bin/env python3
import argparse
import subprocess
import time
import os
import sys
import signal
from utils.port_manager import find_free_port, release_ports, is_port_in_use

def wait_for_port(port: int, timeout: int = 60) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.5)
    return False

def main():
    parser = argparse.ArgumentParser(description="Run a command with a background server.")
    parser.add_argument("--server-cmd", required=True, help="Command to start the server")
    parser.add_argument("--test-cmd", required=True, help="Command to run tests/client")
    parser.add_argument("--port", type=int, help="Port to check. If not provided, finds a free port.")
    parser.add_argument("--env-port-var", default="PORT", help="Environment variable to set for the port")
    args = parser.parse_args()

    port = args.port
    is_dynamic_port = False
    if not port:
        port = find_free_port(6100)
        is_dynamic_port = True
    
    print(f"Using port {port} for server...")
    
    env = os.environ.copy()
    env[args.env_port_var] = str(port)
    env["FRONTEND_PORT"] = str(port)
    env["BASE_URL"] = f"http://localhost:{port}"

    print(f"Starting server: {args.server_cmd}")
    # Use preexec_fn to run in a new process group so we can kill it easily
    server_proc = subprocess.Popen(args.server_cmd, shell=True, env=env, preexec_fn=os.setsid)

    try:
        if not wait_for_port(port, timeout=60):
            print(f"Error: Server did not bind to port {port} within timeout.")
            sys.exit(1)
        
        print(f"Server is up on port {port}. Running tests: {args.test_cmd}")
        test_proc = subprocess.run(args.test_cmd, shell=True, env=env)
        
        if test_proc.returncode != 0:
            print("Tests failed!")
            sys.exit(test_proc.returncode)
        else:
            print("Tests passed!")
            sys.exit(0)
            
    finally:
        print("Shutting down server...")
        try:
            os.killpg(os.getpgid(server_proc.pid), signal.SIGTERM)
            server_proc.wait(timeout=5)
        except Exception:
            pass
        if is_dynamic_port:
            release_ports([port])

if __name__ == "__main__":
    main()
