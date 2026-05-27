#!/usr/bin/env python3
import os
import sys
import time
import signal
import subprocess
from scripts.utils.port_manager import find_free_port, release_ports
from scripts.utils.env_writer import generate_env_local

# Colors for multiplexing
C_BLUE = '\033[94m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_END = '\033[0m'

processes = []

allocated_ports = []

def cleanup(signum, frame):
    print(f"\n{C_YELLOW}Shutting down all services...{C_END}")
    for p in processes:
        p.terminate()
    # Ensure docker is down
    subprocess.run(["docker-compose", "down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Release locked ports
    if allocated_ports:
        release_ports(allocated_ports)
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def prefix_output(process, prefix, color):
    """Read lines from process and print with colored prefix"""
    for line in iter(process.stdout.readline, b''):
        print(f"{color}[{prefix}]{C_END} {line.decode('utf-8').rstrip()}")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"{C_GREEN}Scanning for available ports...{C_END}")
    ports = {
        'frontend': find_free_port(5173),
        'backend': find_free_port(8000),
        'postgres': find_free_port(5434),
        'redis': find_free_port(6380),
        'couchdb': find_free_port(5984)
    }
    
    global allocated_ports
    allocated_ports.extend(ports.values())
    
    # Generate .env.local and get the config
    config = generate_env_local(ports, root_dir)
    
    print(f"\n{C_GREEN}=== EduLafia Startup Configuration ==={C_END}")
    print(f"Frontend:  http://localhost:{ports['frontend']}")
    print(f"Backend:   http://localhost:{ports['backend']}")
    print(f"Postgres:  localhost:{ports['postgres']}")
    print("======================================\n")

    # 1. Start Docker (Pass dynamic ports via environment)
    env = os.environ.copy()
    env.update({str(k): str(v) for k, v in config.items()})
    
    # We must alter docker-compose dynamically or use env vars in the yml. 
    # For now, we assume docker-compose.yml uses ${POSTGRES_PORT:-5434} mapping.
    p_docker = subprocess.Popen(
        ["docker-compose", "--env-file", ".env.local", "up", "postgres", "redis", "couchdb"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env
    )
    processes.append(p_docker)
    
    # Wait for DB
    print(f"{C_BLUE}[SYSTEM]{C_END} Waiting 5s for databases to initialize...")
    time.sleep(5)
    
    # 2. Start Backend
    backend_dir = os.path.join(root_dir, 'apps/backend')
    
    # Start the backend via the virtual environment to ensure dependencies are found
    venv_python = os.path.join(backend_dir, '.venv', 'bin', 'python3')
    if not os.path.exists(venv_python):
        # Fallback to system python if venv doesn't exist
        venv_python = "python3"
        
    env['PYTHONPATH'] = os.path.join(backend_dir, 'src')
        
    p_backend = subprocess.Popen(
        [venv_python, "-m", "uvicorn", "edulafia.main:app", "--port", str(ports['backend']), "--reload"],
        cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env
    )
    processes.append(p_backend)

    # 3. Start Frontend
    frontend_dir = os.path.join(root_dir, 'apps/frontend')
    p_frontend = subprocess.Popen(
        ["pnpm", "dev", "--port", str(ports['frontend'])],
        cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env
    )
    processes.append(p_frontend)

    # Multiplex output threads
    import threading
    threading.Thread(target=prefix_output, args=(p_docker, "DOCKER", C_BLUE), daemon=True).start()
    threading.Thread(target=prefix_output, args=(p_backend, "BACKEND", C_GREEN), daemon=True).start()
    threading.Thread(target=prefix_output, args=(p_frontend, "FRONTEND", C_YELLOW), daemon=True).start()

    for p in processes:
        p.wait()
        
    # Ensure ports are released on natural exit
    if allocated_ports:
        release_ports(allocated_ports)

if __name__ == "__main__":
    main()