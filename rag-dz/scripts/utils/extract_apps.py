#!/usr/bin/env python3
import re

# Read the HTML file
with open('d:/IAFactory/rag-dz/apps/landing/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all app cards that have onclick (operational apps)
pattern = r'<article class="app-card"[^>]*>.*?<h5>(.*?)</h5>.*?<p>(.*?)</p>.*?onclick="window\.open'
matches = re.findall(pattern, content, re.DOTALL)

print(f"Total apps operationnelles: {len(matches)}\n")
print("="*80)

for i, (title, desc) in enumerate(matches, 1):
    # Clean up HTML entities and tags
    title = re.sub(r'<[^>]+>', '', title).strip()
    desc = re.sub(r'<[^>]+>', '', desc).strip()
    print(f"{i:2d}. {title:<40} | {desc}")
