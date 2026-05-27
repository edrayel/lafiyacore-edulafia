#!/bin/bash
# EduLafia Development Server Startup Script
# Checks for port conflicts and prompts user before starting servers

set -e

FRONTEND_PORT=5173
BACKEND_PORT=8000
POSTGRES_PORT=5433
REDIS_PORT=6380
COUCHDB_PORT=5984

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║       EduLafia Development Server        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""

# Function to check if a port is in use
check_port() {
    local port=$1
    local name=$2
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ -n "$pid" ]; then
        echo -e "${YELLOW}⚠ Port $port ($name) is in use by PID: $pid${NC}"
        return 1
    fi
    return 0
}

# Check all ports
CONFLICTS=0
check_port $FRONTEND_PORT "Frontend (Vite)" || CONFLICTS=$((CONFLICTS + 1))
check_port $BACKEND_PORT "Backend (FastAPI)" || CONFLICTS=$((CONFLICTS + 1))
check_port $POSTGRES_PORT "PostgreSQL" || CONFLICTS=$((CONFLICTS + 1))
check_port $REDIS_PORT "Redis" || CONFLICTS=$((CONFLICTS + 1))
check_port $COUCHDB_PORT "CouchDB" || CONFLICTS=$((CONFLICTS + 1))

if [ $CONFLICTS -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Found $CONFLICTS port conflict(s).${NC}"
    echo ""
    echo "Options:"
    echo "  1) Kill processes using conflicting ports"
    echo "  2) Use different ports (edit .env and vite.config.ts)"
    echo "  3) Cancel startup"
    echo ""
    read -p "Choose an option (1/2/3): " choice

    case $choice in
        1)
            echo -e "${YELLOW}Killing conflicting processes...${NC}"
            lsof -ti:$FRONTEND_PORT | xargs kill -9 2>/dev/null || true
            lsof -ti:$BACKEND_PORT | xargs kill -9 2>/dev/null || true
            echo -e "${GREEN}✓ Conflicting processes killed.${NC}"
            ;;
        2)
            echo ""
            read -p "Enter new frontend port (default: $FRONTEND_PORT): " new_frontend_port
            read -p "Enter new backend port (default: $BACKEND_PORT): " new_backend_port
            FRONTEND_PORT=${new_frontend_port:-$FRONTEND_PORT}
            BACKEND_PORT=${new_backend_port:-$BACKEND_PORT}
            echo -e "${GREEN}✓ Using frontend port: $FRONTEND_PORT, backend port: $BACKEND_PORT${NC}"
            ;;
        3|*)
            echo -e "${RED}✗ Startup cancelled.${NC}"
            exit 1
            ;;
    esac
fi

echo ""
echo -e "${GREEN}Starting EduLafia development servers...${NC}"
echo ""

# Start backend
echo -e "${GREEN}→ Starting backend on port $BACKEND_PORT...${NC}"
cd "$(dirname "$0")/../apps/backend"
PYTHONPATH=src python3 -m uvicorn edulafia.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &
BACKEND_PID=$!
cd - > /dev/null

# Wait for backend to start
echo -e "${GREEN}→ Waiting for backend to be ready...${NC}"
for i in $(seq 1 30); do
    if curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready!${NC}"
        break
    fi
    sleep 1
done

# Start frontend
echo -e "${GREEN}→ Starting frontend on port $FRONTEND_PORT...${NC}"
cd "$(dirname "$0")/../apps/frontend"
npx vite --port $FRONTEND_PORT &
FRONTEND_PID=$!
cd - > /dev/null

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║       EduLafia is running! 🚀            ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Frontend:  ${GREEN}http://localhost:$FRONTEND_PORT${NC}"
echo -e "  Backend:   ${GREEN}http://localhost:$BACKEND_PORT${NC}"
echo -e "  API Docs:  ${GREEN}http://localhost:$BACKEND_PORT/docs${NC}"
echo ""
echo -e "  Login:     ${GREEN}See the credentials displayed during initial setup${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"

# Trap Ctrl+C to kill all child processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo -e '\n${RED}Servers stopped.${NC}'; exit" INT TERM

# Wait for any process to exit
wait
