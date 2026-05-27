# Intelligent Port Allocation System Design

## Overview
A custom Python script (`start-dev.py`) built specifically for the EduLafia ecosystem that prevents port conflicts by dynamically scanning and assigning available ports for the Frontend, Backend, and Docker services before booting them.

## Core Responsibilities
1. **Dependency Verification:** Check if Docker, Node/pnpm, and Python are installed and running.
2. **Port Scanning Engine:** Scan the local machine for default ports (5173, 8000, 5434, 6380, 5984).
3. **Auto-Increment Allocation:** If a port is occupied by another project, silently increment (e.g., `8000` -> `8001`) until a free port is found.
4. **Environment Injection:** Dynamically write these new ports to a `.env.local` and `.env` override file.
5. **Unified Process Multiplexing:** Boot Docker Compose, the FastAPI backend, and the Vite frontend simultaneously, multiplexing their standard output into a single, color-coded terminal stream.

## Components

### 1. The Port Scanner (`utils/port_manager.py`)
A lightweight Python `socket` utility that attempts to bind to a port on `127.0.0.1`. If it throws an `OSError`, the port is in use.

### 2. Environment Generator (`utils/env_writer.py`)
Reads the base `.env` and `docker-compose.yml`, replaces the required ports with the newly discovered free ports, and writes them to `.env.local` to ensure all services can communicate with each other (e.g., FastAPI knows the new Postgres port).

### 3. Process Multiplexer (`start-dev.py`)
Uses Python's `subprocess.Popen` to launch the 3 main services asynchronously.
- Prefix `[DOCKER]` (Blue) for `docker-compose up`
- Prefix `[BACKEND]` (Green) for `uvicorn`
- Prefix `[FRONTEND]` (Yellow) for `pnpm dev`
It captures `SIGINT` (Ctrl+C) to gracefully shut down all child processes when the user exits.

## Execution Flow
1. User runs `python start-dev.py`
2. Script scans default ports.
3. Script finds `5434` (Postgres) is blocked. Scans `5435`. It is free.
4. Script writes `DATABASE_URL=postgresql+asyncpg://...:5435/...` to `.env.local`
5. Script rewrites `docker-compose.yml` port bindings dynamically (or uses environment variable overrides).
6. Script boots Docker. Waits for Postgres to be healthy.
7. Script boots Backend on port `8000`.
8. Script boots Frontend on port `5173`.
9. Script prints a summary table of the final URLs.
10. Unified log stream begins.

## Error Handling
- If Docker daemon is not running, abort with a clear error.
- If a port cannot be found within 100 increments, abort.
- If a child process crashes (e.g., Backend fails to start), kill the other processes and exit cleanly.

## Scope
This script is strictly a development tool. It will not be used in staging or production environments (which will rely on Docker Swarm/Kubernetes routing).