#!/bin/bash
# Script to run database migrations for IAFactory RAG
# Usage: ./run_migrations.sh [migration_number]
# Example: ./run_migrations.sh 007  (runs only migration 007)
#          ./run_migrations.sh       (runs all pending migrations)

set -e  # Exit on error

# Load environment variables
if [ -f ../.env ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Database connection from environment or default
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-iafactory}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"

# Construct connection string
DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

echo "=========================================="
echo "IAFactory Database Migrations"
echo "=========================================="
echo "Database: ${DB_NAME}"
echo "Host: ${DB_HOST}:${DB_PORT}"
echo ""

# Check if specific migration number provided
SPECIFIC_MIGRATION=$1

if [ -n "$SPECIFIC_MIGRATION" ]; then
    # Run specific migration
    MIGRATION_FILE="${SPECIFIC_MIGRATION}_*.sql"
    echo "Running specific migration: $MIGRATION_FILE"

    for file in $MIGRATION_FILE; do
        if [ -f "$file" ]; then
            echo "Executing: $file"
            psql "$DATABASE_URL" -f "$file"
            echo "✓ Migration $file completed"
        else
            echo "❌ Migration file not found: $MIGRATION_FILE"
            exit 1
        fi
    done
else
    # Run all migrations in order
    echo "Running all migrations..."
    echo ""

    for file in $(ls -1 [0-9][0-9][0-9]_*.sql | sort); do
        echo "Executing: $file"
        psql "$DATABASE_URL" -f "$file" || {
            echo "❌ Migration failed: $file"
            exit 1
        }
        echo "✓ Migration $file completed"
        echo ""
    done
fi

echo ""
echo "=========================================="
echo "✓ All migrations completed successfully!"
echo "=========================================="

# Show tenant count
echo ""
echo "Current tenants in database:"
psql "$DATABASE_URL" -c "SELECT id, name, region, plan, status, created_at FROM tenants ORDER BY created_at DESC LIMIT 10;"
