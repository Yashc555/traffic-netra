import sys

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add get_base64_crop helper
helper_code = """
import base64
def get_base64_crop(img_np, bbox):
    try:
        x1, y1, x2, y2 = [int(v) for v in bbox]
        h, w = img_np.shape[:2]
        x1 = max(0, x1 - 20)
        y1 = max(0, y1 - 20)
        x2 = min(w, x2 + 20)
        y2 = min(h, y2 + 20)
        crop = img_np[y1:y2, x1:x2]
        crop_pil = Image.fromarray(crop)
        buf = io.BytesIO()
        crop_pil.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        return ""

"""
if "def get_base64_crop" not in content:
    content = content.replace("def st_html(html_str):", helper_code + "def st_html(html_str):")

# Add base64 image generation
gen_code = """                    # Explainable AI reasoning steps
                    crop_b64 = ""
                    if "bbox" in v:
                        crop_b64 = get_base64_crop(st.session_state.original_img, v["bbox"])
                    
                    xai_steps_html = ""
"""
content = content.replace("                    # Explainable AI reasoning steps\n                    xai_steps_html = \"\"", gen_code)

# Add to HTML
html_code = """                        if crop_b64:
                            xai_steps_html += f'<div style="margin-top:8px; text-align:center; border:1px solid #DDD7CD; background:#1C1512; padding:4px;"><img src="data:image/jpeg;base64,{crop_b64}" style="max-width:100%; max-height:120px;" /></div>'
                        xai_steps_html += '</div>'"""
content = content.replace("                        xai_steps_html += '</div>'", html_code)


with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
