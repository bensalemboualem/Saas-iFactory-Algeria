#!/bin/bash
export PGPASSWORD='supabase-secret-password'
docker exec -e PGPASSWORD="$PGPASSWORD" supabase-db psql -U supabase_admin -d postgres -c "ALTER USER supabase_auth_admin WITH PASSWORD 'supabase-secret-password';"
docker exec -e PGPASSWORD="$PGPASSWORD" supabase-db psql -U supabase_admin -d postgres -c "ALTER USER authenticator WITH PASSWORD 'supabase-secret-password';"
docker exec -e PGPASSWORD="$PGPASSWORD" supabase-db psql -U supabase_admin -d postgres -c "SELECT usename, passwd IS NOT NULL as has_pass FROM pg_shadow WHERE usename IN ('supabase_auth_admin', 'authenticator');"
docker restart supabase-auth supabase-rest
sleep 30
docker ps --filter name=supabase --format "table {{.Names}}\t{{.Status}}"
