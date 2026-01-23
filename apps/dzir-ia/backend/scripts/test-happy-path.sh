#!/bin/bash
# Happy Path Test Script for Dzir IA
# Prerequisites: Backend running on port 4000, Qdrant on 6333

API_URL="${API_URL:-http://localhost:4000}"
# JWT token - set via environment or use test token
# In dev with auth disabled/mocked, any token works
# In prod, get a real JWT from Gateway auth
TOKEN="${TEST_JWT:-test-token-for-dev}"

echo "=== Dzir IA Happy Path Test ==="
echo ""

# 1. Health Check
echo "1. Health Check..."
HEALTH=$(curl -s "$API_URL/health")
echo "   $HEALTH"
echo ""

# 2. Create Collection
echo "2. Creating collection 'Test'..."
COLLECTION=$(curl -s -X POST "$API_URL/api/collections" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test collection for happy path", "color": "#00A86B", "icon": "🧪"}')
echo "   $COLLECTION"

COLLECTION_ID=$(echo $COLLECTION | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "   Collection ID: $COLLECTION_ID"
echo ""

if [ -z "$COLLECTION_ID" ]; then
  echo "ERROR: Failed to create collection"
  exit 1
fi

# 3. Capture Text
echo "3. Capturing text content..."
CAPTURE=$(curl -s -X POST "$API_URL/api/capture" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"collectionId\": \"$COLLECTION_ID\",
    \"sourceType\": \"text\",
    \"title\": \"Dzir IA Introduction\",
    \"content\": \"Le projet Dzir IA est un second cerveau personnel pour la gestion de connaissances en Algérie. Il permet aux utilisateurs de capturer, organiser et retrouver leurs informations importantes. Dzir IA utilise des embeddings vectoriels et le RAG (Retrieval Augmented Generation) pour fournir des réponses précises basées sur les documents de l'utilisateur. Le système supporte plusieurs types de sources : texte, URL et PDF.\"
  }")
echo "   $CAPTURE"

DOCUMENT_ID=$(echo $CAPTURE | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "   Document ID: $DOCUMENT_ID"
echo ""

# 4. Search
echo "4. Searching for 'second cerveau'..."
SEARCH=$(curl -s -X POST "$API_URL/api/search" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "second cerveau", "limit": 5}')
echo "   $SEARCH"
echo ""

# 5. Ask
echo "5. Asking 'C'est quoi Dzir IA ?'..."
ASK=$(curl -s -X POST "$API_URL/api/ask" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "C'\''est quoi Dzir IA ?"}')
echo ""
echo "=== ASK RESPONSE (for validation) ==="
echo "$ASK" | python3 -m json.tool 2>/dev/null || echo "$ASK"
echo ""

# 6. Cleanup (optional)
echo "6. Cleanup - deleting test collection..."
DELETE=$(curl -s -X DELETE "$API_URL/api/collections/$COLLECTION_ID" \
  -H "Authorization: Bearer $TOKEN")
echo "   $DELETE"
echo ""

echo "=== Happy Path Test Complete ==="
