#!/bin/bash
FILE=/opt/iafactory-rag-dz/apps/landing/index.html

# Remplacer tous les /apps par les vrais chemins basés sur le port
# Business
sed -i "s|window.open('/apps', '_blank')\">Ouvrir :8182|window.open('apps/dashboard/index.html', '_blank')\">Ouvrir :8182|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8210|window.open('apps/pme-copilot/index.html', '_blank')}>Ouvrir :8210|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8211|window.open('apps/pme-copilot-ui/index.html', '_blank')}>Ouvrir :8211|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8212|window.open('apps/crm-ia/index.html', '_blank')}>Ouvrir :8212|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8213|window.open('apps/crm-ia-ui/index.html', '_blank')}>Ouvrir :8213|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8214|window.open('apps/startup-dz/index.html', '_blank')}>Ouvrir :8214|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8215|window.open('apps/startupdz-onboarding/index.html', '_blank')}>Ouvrir :8215|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8195|window.open('apps/business-dz/index.html', '_blank')}>Ouvrir :8195|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8193|window.open('apps/dashboard/index.html', '_blank')}>Ouvrir :8193|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8196|window.open('apps/data-dz/index.html', '_blank')}>Ouvrir :8196|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8205|window.open('apps/data-dz-dashboard/index.html', '_blank')}>Ouvrir :8205|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8206|window.open('apps/data-dz-dashboard/index.html', '_blank')}>Ouvrir :8206|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8192|window.open('apps/landing/index.html', '_blank')}>Ouvrir :8192|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8216|window.open('apps/landing-pro/index.html', '_blank')}>Ouvrir :8216|g" $FILE

# Finance
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8207|window.open('apps/billing-panel/index.html', '_blank')}>Ouvrir :8207|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8208|window.open('apps/billing-panel/index.html', '_blank')}>Ouvrir :8208|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8199|window.open('apps/fiscal-assistant/index.html', '_blank')}>Ouvrir :8199|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8200|window.open('apps/fiscal-assistant/index.html', '_blank')}>Ouvrir :8200|g" $FILE

# Legal
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8197|window.open('apps/legal-assistant/index.html', '_blank')}>Ouvrir :8197|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8198|window.open('apps/legal-assistant/index.html', '_blank')}>Ouvrir :8198|g" $FILE

# IA & Agents
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8188|window.open('apps/bmad/index.html', '_blank')}>Ouvrir :8188|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8185|window.open('apps/shared/council/index.html', '_blank')}>Ouvrir :8185|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8189|window.open('apps/creative-studio/index.html', '_blank')}>Ouvrir :8189|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8186|window.open('apps/ithy/index.html', '_blank')}>Ouvrir :8186|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8187|window.open('apps/ithy/index.html', '_blank')}>Ouvrir :8187|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8201|window.open('apps/voice-assistant/index.html', '_blank')}>Ouvrir :8201|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8202|window.open('apps/voice-assistant/index.html', '_blank')}>Ouvrir :8202|g" $FILE
sed -i "s|window.open('/apps', '_blank')}>Ouvrir :8191|window.open('apps/landing/index.html', '_blank')}>Ouvrir :8191|g" $FILE

echo "Apps links fixed!"
