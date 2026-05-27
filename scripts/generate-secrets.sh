#!/bin/bash
# EduLafia Secret Key Generator
# Generates secure random keys for JWT, APP, and database passwords
#
# Usage:
#   ./scripts/generate-secrets.sh          # Print to stdout
#   ./scripts/generate-secrets.sh --apply  # Update .env file

set -e

# Generate secrets
JWT_SECRET_KEY=$(openssl rand -hex 64)
APP_SECRET_KEY=$(openssl rand -hex 64)
POSTGRES_PASSWORD=$(openssl rand -base64 24 | tr -d '=/+' | head -c 32)
COUCHDB_PASSWORD=$(openssl rand -base64 24 | tr -d '=/+' | head -c 32)

if [ "$1" = "--apply" ]; then
    # Update .env file
    ENV_FILE=".env"

    if [ ! -f "$ENV_FILE" ]; then
        echo "Error: $ENV_FILE not found. Copy .env.example to .env first."
        exit 1
    fi

    # Replace secrets in .env
    sed -i.bak \
        -e "s|^JWT_SECRET_KEY=.*|JWT_SECRET_KEY=$JWT_SECRET_KEY|" \
        -e "s|^APP_SECRET_KEY=.*|APP_SECRET_KEY=$APP_SECRET_KEY|" \
        -e "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$POSTGRES_PASSWORD|" \
        -e "s|^COUCHDB_PASSWORD=.*|COUCHDB_PASSWORD=$COUCHDB_PASSWORD|" \
        -e "s|^DATABASE_URL=.*|DATABASE_URL=postgresql+asyncpg://edulafia:$POSTGRES_PASSWORD@localhost:5433/edulafia|" \
        "$ENV_FILE"

    # Remove backup file
    rm -f "${ENV_FILE}.bak"

    echo "Secrets updated in $ENV_FILE"
    echo ""
    echo "IMPORTANT: Restart your services for changes to take effect:"
    echo "  docker-compose down && docker-compose up -d"
else
    # Print to stdout
    echo "# Generated EduLafia Secrets"
    echo "# Copy these to your .env file"
    echo ""
    echo "JWT_SECRET_KEY=$JWT_SECRET_KEY"
    echo "APP_SECRET_KEY=$APP_SECRET_KEY"
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD"
    echo "COUCHDB_PASSWORD=$COUCHDB_PASSWORD"
    echo ""
    echo "# Or run: ./scripts/generate-secrets.sh --apply"
fi
