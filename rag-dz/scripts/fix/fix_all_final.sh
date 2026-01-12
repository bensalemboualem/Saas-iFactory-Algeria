#!/bin/bash

cd /opt/iafactory-rag-dz/apps

EXCLUDED="shared landing school-erp docs"
FIXED=0
SKIPPED=0

for app_dir in */; do
    app_name="${app_dir%/}"

    # Skip exclus
    if echo "$EXCLUDED" | grep -wq "$app_name"; then
        ((SKIPPED++))
        continue
    fi

    file="$app_dir/index.html"

    if [ ! -f "$file" ]; then
        ((SKIPPED++))
        continue
    fi

    # Backup
    cp "$file" "$file.backup-final-$(date +%s)"

    # 1. Supprimer toutes références ancien chatbot
    sed -i '/help-bubble/d' "$file"
    sed -i '/sendHelpMessage/d' "$file"
    sed -i '/handleHelpKeyPress/d' "$file"
    sed -i '/addHelpMessage/d' "$file"
    sed -i '/HELP CHATBOT/d' "$file"

    # 2. Compter les références iafactory-unified.js
    count=$(grep -c "iafactory-unified.js" "$file" 2>/dev/null || echo "0")

    if [ "$count" -gt 1 ]; then
        # Supprimer tous sauf le dernier
        # Garder seulement la dernière occurrence
        awk '
        /iafactory-unified\.js/ {
            line=$0;
            next
        }
        { print }
        END { if (line) print line }
        ' "$file" > "$file.tmp"
        mv "$file.tmp" "$file"
    fi

    # 3. Vérifier si système unifié est présent
    has_chatbot=$(grep -c "iaf-chatbot-btn" "$file" 2>/dev/null || echo "0")
    has_js=$(grep -c "iafactory-unified.js" "$file" 2>/dev/null || echo "0")

    if [ "$has_chatbot" -eq 0 ] || [ "$has_js" -eq 0 ]; then
        # Supprimer </body> et </html>
        sed -i 's|</body>||g' "$file"
        sed -i 's|</html>||g' "$file"

        # Ajouter système unifié
        cat >> "$file" << 'EOF'

    <!-- Footer Unifié -->
    <div data-iaf-footer></div>

    <!-- Chatbot Unifié -->
    <button class="iaf-chatbot-btn" onclick="IAFactory.toggleChatbot()"
            title="Aide" aria-label="Aide">
        💬
    </button>

    <!-- Scripts Unifiés -->
    <script src="/apps/shared/iafactory-unified.js"></script>

</body>
</html>
EOF
    fi

    echo "✅ $app_name"
    ((FIXED++))
done

echo ""
echo "=================================================="
echo "✅ Apps corrigées: $FIXED"
echo "⏭️  Apps ignorées: $SKIPPED"
echo "=================================================="
