#!/bin/bash
FILE=/opt/iafactory-rag-dz/apps/landing/index.html

# Dev apps remaining
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8203|window.open('"'"'apps/api-portal/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8203|g' $FILE
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8194|window.open('"'"'apps/dev-portal/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8194|g' $FILE
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8204|window.open('"'"'apps/developer/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8204|g' $FILE
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8190|window.open('"'"'apps/shared/n8n/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8190|g' $FILE
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8184|window.open('"'"'apps/dzirvideo-ai/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8184|g' $FILE
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8183|window.open('"'"'apps/shared/docs/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8183|g' $FILE
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8888|window.open('"'"'apps/shared/jupyter/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8888|g' $FILE
sed -i 's|window.open('"'"'/apps'"'"', '"'"'_blank'"'"')">Ouvrir :8180|window.open('"'"'apps/landing/index.html'"'"', '"'"'_blank'"'"')">Ouvrir :8180|g' $FILE

echo "Dev apps links fixed! Remaining /apps links:"
grep -c "window.open('/apps'" $FILE || echo "0"
