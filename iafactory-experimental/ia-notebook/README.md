# Notebook LM IAFactory 📓

**Interrogez vos documents avec l'Intelligence Artificielle**

Alternative professionnelle à NotebookLM de Google, optimisée pour le marché algérien.

## 🌟 Fonctionnalités

- ✅ **Upload multi-formats** - PDF, DOCX, TXT, MD, CSV, XLSX
- ✅ **RAG avancé** - Retrieval Augmented Generation
- ✅ **Chat intelligent** - Questions/réponses sur vos documents
- ✅ **Sources citées** - Traçabilité des réponses
- ✅ **Multi-documents** - Interrogez plusieurs fichiers simultanément
- ✅ **Embeddings sémantiques** - Recherche par sens, pas par mots-clés
- ✅ **IA puissante** - Claude (Anthropic) ou GPT-4 (OpenAI)

## 🚀 Installation

### Backend
```bash
cd apps/notebook-lm/backend
pip install PyPDF2 python-docx pandas langchain faiss-cpu anthropic openai
```

### API
```python
from app.routers import notebook_lm
app.include_router(notebook_lm.router)
```

## 📖 Utilisation

### Upload document
```bash
curl -X POST "https://api.iafactory.com/api/notebook-lm/upload" \
  -F "file=@document.pdf"
```

### Poser une question
```bash
curl -X POST "https://api.iafactory.com/api/notebook-lm/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Résume les points clés",
    "file_ids": ["file-id-123"]
  }'
```

## 🏗️ Architecture

- **Frontend**: Interface chat avec drag & drop upload
- **Backend**: Python RAG service avec FAISS
- **API**: FastAPI endpoints (upload, query, delete)
- **Embeddings**: OpenAI ou HuggingFace local
- **LLM**: Claude 3.5 Sonnet ou GPT-4

## 📊 Formats Supportés

| Format | Extension | Extraction |
|--------|-----------|------------|
| PDF | .pdf | PyPDF2 |
| Word | .docx | python-docx |
| Texte | .txt, .md | Direct |
| CSV | .csv | pandas |
| Excel | .xlsx | pandas |

**Limite**: 50 MB par fichier

---

✅ **NOTEBOOK LM COMPLÉTÉ**
