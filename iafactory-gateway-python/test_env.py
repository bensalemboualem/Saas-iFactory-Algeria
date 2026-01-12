import os
from dotenv import load_dotenv

load_dotenv()

print(f"DEEPSEEK_API_KEY : {os.getenv('DEEPSEEK_API_KEY', 'VIDE')[:20]}...")
print(f"GEMINI_API_KEY : {os.getenv('GEMINI_API_KEY', 'VIDE')[:20]}...")
