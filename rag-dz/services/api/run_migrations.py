#!/usr/bin/env python3
"""
Database Migrations Runner for IAFactory RAG
Executes SQL migration files in order

Usage:
    python run_migrations.py          # Run all pending migrations
    python run_migrations.py 006      # Run specific migration
    python run_migrations.py --check  # Check migration status
"""

import os
import sys
import glob
import psycopg
from pathlib import Path
from datetime import datetime
from app.config import get_settings

settings = get_settings()


def get_connection():
    """Get database connection"""
    return psycopg.connect(settings.postgres_url, autocommit=True)


def create_migrations_table():
    """Create migrations tracking table if not exists"""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                executed_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        """)
        print("✓ Migrations tracking table ready")


def get_executed_migrations():
    """Get list of already executed migrations"""
    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT version FROM schema_migrations ORDER BY version")
            return {row[0] for row in cur.fetchall()}
    except Exception:
        # Table doesn't exist yet
        return set()


def execute_migration(filepath: Path):
    """Execute a single migration file"""
    version = filepath.name.split('_')[0]
    name = '_'.join(filepath.name.split('_')[1:]).replace('.sql', '')

    print(f"\n{'='*60}")
    print(f"Executing migration {version}: {name}")
    print(f"{'='*60}")

    with get_connection() as conn, conn.cursor() as cur:
        # Read migration file
        sql = filepath.read_text(encoding='utf-8')

        # Execute migration
        try:
            cur.execute(sql)

            # Record migration
            cur.execute("""
                INSERT INTO schema_migrations (version, name)
                VALUES (%s, %s)
                ON CONFLICT (version) DO NOTHING
            """, (version, name))

            print(f"✓ Migration {version} completed successfully")
            return True

        except Exception as e:
            print(f"❌ Migration {version} failed: {e}")
            raise


def run_migrations(specific_version=None):
    """Run all pending migrations or a specific one"""
    # Create tracking table
    create_migrations_table()

    # Get executed migrations
    executed = get_executed_migrations()

    # Get migration files
    migrations_dir = Path(__file__).parent / 'migrations'
    pattern = f"{specific_version}_*.sql" if specific_version else "[0-9][0-9][0-9]_*.sql"
    migration_files = sorted(migrations_dir.glob(pattern))

    if not migration_files:
        if specific_version:
            print(f"❌ No migration found for version {specific_version}")
            sys.exit(1)
        else:
            print("✓ No migration files found")
            return

    # Execute migrations
    executed_count = 0
    skipped_count = 0

    for filepath in migration_files:
        version = filepath.name.split('_')[0]

        if version in executed:
            print(f"⏭️  Skipping migration {version} (already executed)")
            skipped_count += 1
            continue

        execute_migration(filepath)
        executed_count += 1

    # Summary
    print(f"\n{'='*60}")
    print("Migration Summary")
    print(f"{'='*60}")
    print(f"✓ Executed: {executed_count}")
    print(f"⏭️  Skipped: {skipped_count}")
    print(f"{'='*60}\n")

    if executed_count > 0:
        show_tenant_stats()


def check_migration_status():
    """Show current migration status"""
    create_migrations_table()
    executed = get_executed_migrations()

    migrations_dir = Path(__file__).parent / 'migrations'
    all_migrations = sorted(migrations_dir.glob("[0-9][0-9][0-9]_*.sql"))

    print(f"\n{'='*60}")
    print("Migration Status")
    print(f"{'='*60}\n")

    for filepath in all_migrations:
        version = filepath.name.split('_')[0]
        name = '_'.join(filepath.name.split('_')[1:]).replace('.sql', '')
        status = "✓ EXECUTED" if version in executed else "⏳ PENDING"

        print(f"{version} {status:12s} {name}")

    print(f"\n{'='*60}")
    print(f"Total: {len(all_migrations)} migrations")
    print(f"Executed: {len(executed)}")
    print(f"Pending: {len(all_migrations) - len(executed)}")
    print(f"{'='*60}\n")


def show_tenant_stats():
    """Show tenant statistics after migrations"""
    try:
        with get_connection() as conn, conn.cursor() as cur:
            # Count tenants
            cur.execute("SELECT COUNT(*) FROM tenants")
            tenant_count = cur.fetchone()[0]

            print(f"\n{'='*60}")
            print("Tenant Statistics")
            print(f"{'='*60}\n")
            print(f"Total tenants: {tenant_count}")

            # Show recent tenants
            cur.execute("""
                SELECT id, name, region, plan, status, created_at
                FROM tenants
                ORDER BY created_at DESC
                LIMIT 5
            """)

            print("\nRecent tenants:")
            for row in cur.fetchall():
                tid, name, region, plan, status, created = row
                print(f"  - {name[:40]:40s} | {region} | {plan:10s} | {status}")

            print(f"\n{'='*60}\n")

    except Exception as e:
        print(f"Note: Could not fetch tenant stats (tenants table may not exist yet)")


def main():
    """Main entry point"""
    print(f"\n{'='*60}")
    print("IAFactory Database Migrations")
    print(f"{'='*60}")
    print(f"Database: {settings.postgres_url.split('@')[1] if '@' in settings.postgres_url else 'configured'}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Parse arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg in ['--check', '-c', 'status']:
            check_migration_status()
            return

        elif arg in ['--help', '-h']:
            print(__doc__)
            return

        else:
            # Specific migration version
            run_migrations(specific_version=arg)
            return

    # Run all pending migrations
    run_migrations()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
