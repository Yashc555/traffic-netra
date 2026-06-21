import sys

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "System-Wide Performance Header (Fake high-throughput stats)" in line:
        skip = True
    
    if "        # 1. Metric Cards" in line:
        skip = False
        
    if not skip:
        new_lines.append(line)

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
