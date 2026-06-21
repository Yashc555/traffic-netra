# ui_assets.py

SVG_ICONS = {
    "camera": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></span>""",
    "chart": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></span>""",
    "upload": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg></span>""",
    "alert": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span>""",
    "check": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></span>""",
    "card": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg></span>""",
    "info": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg></span>""",
    "settings": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>""",
    "download": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></span>""",
    "clock": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span>""",
    "pin": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span>""",
    "video": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 7a2 2 0 0 0-2.45-1.45L16 7V5a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2l4.55 1.45A2 2 0 0 0 23 17V7z"/></svg></span>""",
    "doc": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></span>""",
    "users": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>""",
    "truck": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg></span>""",
    "shield": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span>""",
    "crosshair": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg></span>""",
    "trending": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></span>""",
    "trophy": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34"/><path d="M12 2a7.7 7.7 0 0 1 7.54 8H4.46A7.7 7.7 0 0 1 12 2z"/></svg></span>""",
    "target": """<span class="tn-svg-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></span>""",
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@300;400;500;600;700;800&display=swap');

/* --- Hide Streamlit Header Bar --- */
header[data-testid="stHeader"] {
    display: none !important;
}
[data-testid="stAppViewContainer"] {
    padding-top: 0px !important;
}

/* --- Root & Body Overrides --- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1C1512;
}

.stApp {
    background-color: #FAF9F5 !important;
}

/* Force Light Theme Colors on all default Streamlit texts (overriding dark mode hosts) */
.stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp td, .stApp th {
    color: #1C1512 !important;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #1C1512 !important;
}
[data-testid="stSidebar"] *, [data-testid="stSidebar"] label span, [data-testid="stSidebar"] label p {
    color: #1C1512 !important;
}

/* --- Typography --- */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Sora', sans-serif !important;
    color: #1C1512 !important;
    font-weight: 700 !important;
}

/* --- Sidebar styling --- */
[data-testid="stSidebar"] {
    background-color: #F4EFE6 !important;
    border-right: 1px solid #DDD7CD !important;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}
[data-testid="stSidebar"] hr {
    border-color: #DDD7CD !important;
}

/* --- Main Block Container --- */
.main .block-container {
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1350px;
}

/* --- Section Labels (Muted, tracked print headers) --- */
.tn-section-label {
    font-family: 'Sora', sans-serif;
    font-size: 10px;
    font-weight: 700;
    color: #7D7066 !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.tn-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #E6DFD5 !important;
}

/* --- Wordmark / Branding --- */
.tn-wordmark {
    display: flex;
    flex-direction: column;
    padding-bottom: 20px;
    border-bottom: 1px solid #DDD7CD;
    margin-bottom: 24px;
}
.tn-wordmark-title {
    font-family: 'Sora', sans-serif;
    font-size: 20px;
    font-weight: 300;
    color: #1C1512 !important;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin: 0;
}
.tn-wordmark-title b {
    font-weight: 800;
}
.tn-wordmark-sub {
    font-size: 9px;
    color: #7D7066 !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-top: 4px;
    font-weight: 600;
}

/* --- Page Header --- */
.tn-page-header {
    margin-bottom: 28px;
    border-bottom: 1px solid #DDD7CD;
    padding-bottom: 16px;
}
.tn-page-header h1 {
    font-size: 32px;
    font-weight: 800 !important;
    letter-spacing: -1px;
    margin: 0 0 6px 0;
    text-transform: lowercase;
}
.tn-main-header h1 {
    font-size: 56px !important;
}
.tn-page-header p {
    color: #6E6259 !important;
    font-size: 10px;
    margin: 0;
    letter-spacing: 1.5px;
    line-height: 1.5;
    font-weight: 600;
}

/* --- Cards (Sharp geometry, print journal cards) --- */
.tn-card {
    background: #F4EFE6;
    border: 1px solid #DDD7CD;
    border-radius: 0px !important; /* Flat geometry */
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: none !important; /* No shadows */
}

/* --- Status Banner --- */
.tn-status-banner {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    margin-bottom: 20px;
    border: 1px solid #DDD7CD;
    background: #F4EFE6;
    border-radius: 0px;
}
.tn-status-banner.violation {
    border-left: 4px solid #B55A4B !important;
    background: #F7ECE9;
}
.tn-status-banner.violation, .tn-status-banner.violation * {
    color: #B55A4B !important;
}
.tn-status-banner.clear {
    border-left: 4px solid #5B806B !important;
    background: #EDF3F0;
}
.tn-status-banner.clear, .tn-status-banner.clear * {
    color: #5B806B !important;
}

/* --- Badges --- */
.tn-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 8px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    border-radius: 0px;
}
.badge-critical { background: #F7ECE9 !important; color: #B55A4B !important; border: 1px solid #ECC2BC !important; }
.badge-warning  { background: #FAF4E8 !important; color: #B8934E !important; border: 1px solid #EADCB8 !important; }
.badge-info     { background: #E9F1F5 !important; color: #4A7A96 !important; border: 1px solid #C9DFEB !important; }
.badge-clear    { background: #EDF3F0 !important; color: #5B806B !important; border: 1px solid #C6DFD4 !important; }

/* --- Metrics Grid & Cards --- */
.tn-metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}
.tn-metric {
    background: #F4EFE6;
    border: 1px solid #DDD7CD;
    border-radius: 0px !important;
    padding: 16px;
    position: relative;
    box-shadow: none !important;
}
.tn-metric::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: var(--accent, #DDD7CD);
}
.tn-metric.detected::before { background: #B55A4B; }
.tn-metric.clear::before    { background: #5B806B; }
.tn-metric-label {
    font-family: 'Sora', sans-serif;
    font-size: 9px;
    font-weight: 700;
    color: #7D7066 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.tn-metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #1C1512 !important;
    line-height: 1.1;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}
.tn-metric-sub {
    font-size: 11px;
    color: #6E6259 !important;
    margin-top: 4px;
}

/* --- Canvas Frame --- */
.tn-image-canvas {
    background: #F4EFE6;
    border: 1px solid #DDD7CD;
    padding: 8px;
    display: inline-block;
}

.tn-image-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FAF9F5;
    border-bottom: 1px solid #DDD7CD;
    padding: 12px 16px;
    font-family: 'Sora', sans-serif;
    font-size: 10px;
    font-weight: 700;
    color: #1C1512 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.tn-image-label svg {
    color: #7D7066;
    width: 14px;
    height: 14px;
}

/* --- Plate Display --- */
.tn-plate-box {
    background: #1C1512;
    border: 1px solid #33221A;
    border-radius: 0px !important;
    padding: 10px 20px;
    display: inline-block;
    margin: 8px 0;
}
.tn-plate-text {
    font-family: 'Courier New', monospace;
    font-size: 24px;
    font-weight: 700;
    color: #FAF9F5 !important;
    letter-spacing: 5px;
}

/* --- Minimal Metadata Pill / UUID --- */
.tn-uuid {
    font-family: 'Courier New', monospace;
    font-size: 10px;
    color: #6E6259 !important;
    background: #EADFCF !important;
    padding: 3px 6px;
    border-radius: 0px;
}

/* --- File Uploader Styling (Fully transparent and light theme forced) --- */
[data-testid="stFileUploader"] {
    background-color: #F4EFE6 !important;
    border: 1px dashed #C8BFAF !important;
    border-radius: 0px !important;
    padding: 8px !important;
}
[data-testid="stFileUploader"] > section {
    background-color: #F4EFE6 !important;
    border: none !important;
    padding: 8px 12px !important;
}
[data-testid="stFileUploader"] > section * {
    background-color: transparent !important;
    color: #1C1512 !important;
}
[data-testid="stFileUploader"] button {
    border-radius: 0px !important;
    border: 1px solid #DDD7CD !important;
    background: #FAF9F5 !important;
    color: #1C1512 !important;
    font-size: 11px !important;
}
[data-testid="stFileUploader"] button:hover {
    background-color: #EADFCF !important;
    border-color: #C8BFAF !important;
}
[data-testid="stFileUploaderDropzone"] {
    background-color: #F4EFE6 !important;
}

/* --- Streamlit Buttons (Flat Terracotta for primary stButton) --- */
.stButton > button {
    background: #B55A4B !important;
    color: #FAF9F5 !important;
    border: 1px solid #B55A4B !important;
    border-radius: 0px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    padding: 12px 24px !important;
    transition: all 0.15s ease-in-out !important;
    box-shadow: none !important;
}
.stButton > button * {
    color: #FAF9F5 !important;
}
.stButton > button:hover {
    background: #9E4A3B !important;
    border-color: #9E4A3B !important;
    color: #FAF9F5 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* --- Sidebar Buttons (Flat Warm Sand / Compact Editorial style) --- */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] button[data-testid^="stBaseButton"] {
    background: #FAF9F5 !important;
    color: #1C1512 !important;
    border: 1px solid #C8BFAF !important;
    border-radius: 0px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    padding: 8px 16px !important;
    transition: all 0.15s ease-in-out !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button *,
[data-testid="stSidebar"] button[data-testid^="stBaseButton"] * {
    color: #1C1512 !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:hover {
    background: #EADFCF !important;
    border-color: #A69B8F !important;
    color: #1C1512 !important;
    box-shadow: none !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover *,
[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:hover * {
    color: #1C1512 !important;
}

/* --- Secondary Download Buttons (Flat Warm Sand / Editorial style) --- */
.pdf-btn > button, div[data-testid="stDownloadButton"] > button {
    background: #FAF9F5 !important;
    color: #1C1512 !important;
    border: 1px solid #C8BFAF !important;
    border-radius: 0px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    padding: 12px 24px !important;
    transition: all 0.15s ease-in-out !important;
    box-shadow: none !important;
}
.pdf-btn > button *, div[data-testid="stDownloadButton"] > button * {
    color: #1C1512 !important;
}
.pdf-btn > button:hover, div[data-testid="stDownloadButton"] > button:hover {
    background: #EADFCF !important;
    border-color: #A69B8F !important;
    color: #1C1512 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* --- Native Form Widgets --- */
[data-testid="stCheckbox"] label span, [data-testid="stRadio"] label span {
    font-size: 12px !important;
    color: #1C1512 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stCheckbox"] [role="checkbox"] {
    border-radius: 0px !important;
    border-color: #C8BFAF !important;
}
[data-testid="stCheckbox"] [role="checkbox"][aria-checked="true"] {
    background-color: #1C1512 !important;
    border-color: #1C1512 !important;
}

/* Text Input & Select Box styling */
[data-testid="stTextInput"] input, [data-testid="stSelectbox"] > div > div {
    background: #FAF9F5 !important;
    border: 1px solid #DDD7CD !important;
    border-radius: 0px !important;
    color: #1C1512 !important;
    font-size: 13px !important;
}
[data-testid="stInputHelperInstructions"] {
    left: 0 !important;
    right: 0 !important;
    text-align: center !important;
}
[data-testid="stTextInput"] label, [data-testid="stSelectbox"] label {
    font-family: 'Sora', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #7D7066 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* --- Tabs --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 32px !important;
    border-bottom: 1px solid #DDD7CD !important;
    background-color: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: #7D7066 !important;
    background-color: transparent !important;
    padding: 12px 4px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #1C1512 !important;
    border-bottom: 2px solid #1C1512 !important;
}

/* --- Table & Custom History --- */
.tn-table-container {
    width: 100%;
    overflow-x: auto;
}
table.tn-history-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: left;
    background: #F4EFE6;
}
table.tn-history-table th {
    background: #EADFCF;
    border-bottom: 1px solid #DDD7CD;
    color: #1C1512 !important;
    padding: 10px 14px;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 10px;
}
table.tn-history-table td {
    padding: 12px 14px;
    border-bottom: 1px solid #DDD7CD;
    color: #6E6259 !important;
}
table.tn-history-table tr:last-child td {
    border-bottom: none;
}

/* --- Inline SVG Alignment helper --- */
.tn-svg-icon {
    display: inline-flex;
    align-self: center;
    margin-right: 6px;
    vertical-align: middle;
}
.tn-svg-icon svg {
    width: 14px;
    height: 14px;
    stroke: currentColor;
}

/* --- Alert Messages --- */
.stAlert {
    border-radius: 0px !important;
    box-shadow: none !important;
    border: 1px solid #DDD7CD !important;
    background-color: #F4EFE6 !important;
}

/* --- Loading Spinner --- */
.tn-loading {
    text-align: center;
    padding: 40px;
}
.tn-loading-spinner {
    width: 32px;
    height: 32px;
    border: 2px solid #EADFCF;
    border-top-color: #1C1512;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* --- Hide Streamlit Branding --- */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }

/* --- Lock Sidebar (Always show, hide all collapse/expand controls) --- */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}
[data-testid="stSidebar"] {
    min-width: 21rem !important;
    transform: none !important;
    visibility: visible !important;
}

/* --- Vega Lite Chart Overrides (Remove Dark Background & Clean Labels) --- */
[data-testid="stVegaLiteChart"], .stVegaLiteChart, .stVegaLiteChart > div, .stVegaLiteChart svg {
    background-color: transparent !important;
    background: transparent !important;
}
.stVegaLiteChart text, .stVegaLiteChart svg text {
    fill: #1C1512 !important;
    color: #1C1512 !important;
}
</style>
"""
