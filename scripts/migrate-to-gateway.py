import re
import sys

file_path = sys.argv[1]
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remplace imports OpenAI
content = re.sub(r"from openai import.*", "import httpx", content)
content = re.sub(r"OpenAI\(api_key=.*?\)", "httpx.AsyncClient()", content)

# Remplace appels OpenAI par gateway
content = re.sub(
    r"client\.chat\.completions\.create\((.*?)\)",
    r"await httpx.post(\"http://localhost:3001/api/llm/chat/completions\", json={\1})",
    content, flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Migré: {file_path}")
