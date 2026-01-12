#!/usr/bin/env python3
"""Insert Archon UI location block into nginx config"""

# Read the nginx config
with open('iafactory.conf', 'r') as f:
    lines = f.readlines()

# Read the archon block to insert
with open('archon-nginx-block.txt', 'r') as f:
    archon_block = f.read()

# Find the line with the closing brace of the server block
closing_braces = []
for i, line in enumerate(lines):
    if line.strip() == '}':
        closing_braces.append(i)

# The server block closing brace is the second to last }
if len(closing_braces) >= 2:
    insert_line = closing_braces[-2]  # Second to last }
    
    # Insert archon block before this closing brace
    lines.insert(insert_line, archon_block + '\n')
    
    # Write back
    with open('iafactory-fixed.conf', 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Archon block inserted at line {insert_line}")
else:
    print(f"❌ Could not find server block closing brace (found {len(closing_braces)} closing braces)")
