import sys

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.startswith("# ─── SVG Icons Dictionary ─────────────────────────────────────────────────────"):
        skip = True
        new_lines.append("from ui_assets import SVG_ICONS, CUSTOM_CSS\n")
        new_lines.append("st.markdown(CUSTOM_CSS, unsafe_allow_html=True)\n")
    if line.startswith("# ─── Session State Init ────────────────────────────────────────────────────────"):
        skip = False
    
    if not skip:
        new_lines.append(line)

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
