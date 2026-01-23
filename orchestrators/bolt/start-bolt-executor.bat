@echo off
cd /d D:\IAFactory\rag-dz\orchestrators\bolt
set BOLT_URL=http://localhost:5174
python -m uvicorn src.main:app --host 0.0.0.0 --port 8053
