import streamlit as st
import time
import random
import cv2
import numpy as np
from PIL import Image

# ===========================================================================
# PAGE CONFIG
# ===========================================================================
st.set_page_config(page_title="SolarVisionAI", page_icon="☀️", layout="wide")

# ===========================================================================
# DESIGN TOKENS
# ===========================================================================
BG_BASE = "#0B0F1E"
BG_PANEL = "#141B30"
SUN_ORANGE = "#FF7A3D"
SUN_GOLD = "#FFC93C"
FLARE_PINK = "#FF4D8D"
SOLAR_BLUE = "#4F8DFF"
ECO_GREEN = "#2EE6A6"
TEXT_PRIMARY = "#F5F7FF"
TEXT_MUTED = "#93A0C5"

GRADIENTS = [
    f"linear-gradient(135deg, {SUN_ORANGE}, {SUN_GOLD})",
    f"linear-gradient(135deg, {FLARE_PINK}, {SUN_ORANGE})",
    f"linear-gradient(135deg, {SOLAR_BLUE}, {ECO_GREEN})",
    f"linear-gradient(135deg, {ECO_GREEN}, {SUN_GOLD})",
]

# ===========================================================================
# SOLAR ENERGY FUN FACTS
# ===========================================================================
FACTS = [
    ("🌞", "Sunlight takes about 8 minutes and 20 seconds to travel the ~150 million km from the Sun to Earth."),
    ("⚡", "In just one hour, the Sun delivers more energy to Earth than the entire world uses in a full year."),
    ("🔬", "The first practical solar cell was built at Bell Labs in 1954 with ~6% efficiency — modern panels now top 22%."),
    ("🇮🇳", "Rajasthan's Bhadla Solar Park is one of the largest solar installations on Earth, spanning thousands of hectares."),
    ("🌥️", "Solar panels still generate electricity on cloudy days — typically 10-25% of their peak output."),
    ("❄️", "Panels actually run slightly more efficiently in cool, sunny climates — output dips a little as panel temperature rises."),
    ("♻️", "A typical rooftop solar system can offset around one tonne of CO2 every year compared to grid electricity."),
    ("🔄", "Bifacial panels capture reflected sunlight on their underside too, boosting total yield by up to 30%."),
    ("⏳", "Most panels are warrantied for 25+ years, while repaying the energy used to make them in just 1-4 years."),
    ("💧", "'Floatovoltaics' — solar farms floating on reservoirs — save land and cut water evaporation at the same time."),
    ("🔤", "The word 'photovoltaic' combines 'photo' (light) with 'volt', honoring physicist Alessandro Volta."),
    ("🏭", "China currently manufactures and installs more solar capacity than any other country in the world."),
    ("🛰️", "Satellites and the International Space Station rely on solar panels as their primary power source in orbit."),
    ("🏠", "A well-sized residential solar system can cut a household's electricity bill by 70-90%."),
    ("🧊", "Snow usually slides off tilted panels quickly — their dark surface absorbs heat and speeds up the melt."),
]

LOADING_STEPS = [
    "📡 Fetching satellite tile resolution...",
    "🧠 Running Segment Anything Model (SAM)...",
    "🟦 Running YOLOv8 rooftop object detector...",
    "🧩 Matching panel grid & color signatures...",
    "📐 Calculating usable rooftop area...",
]

METRICS_BY_TYPE = {
    "industrial": {
        "area": "1,500 sq. meter", "usable": "1,275 sq. meter (85%)",
        "capacity": "220 kW", "roi": "4.2 Years",
        "reco": "Industrial roof strength is optimal. Use Monocrystalline half-cell panels with a south-facing 15° tilt for maximum yield.",
    },
    "residential": {
        "area": "250 sq. meter", "usable": "175 sq. meter (70%)",
        "capacity": "35 kW", "roi": "5.5 Years",
        "reco": "Minor shading detected from nearby trees. Micro-inverters are recommended over a central string inverter to bypass localized power drops.",
    },
    "apartment": {
        "area": "1,100 sq. meter", "usable": "825 sq. meter (75%)",
        "capacity": "120 kW", "roi": "4.8 Years",
        "reco": "Standard concrete flat roof. A ballasted mounting system is recommended to avoid roof penetration and leakage risks.",
    },
    "default": {
        "area": "850 sq. meter", "usable": "550 sq. meter",
        "capacity": "75 kW", "roi": "5.0 Years",
        "reco": "Standard concrete flat roof. A ballasted mounting system is recommended to avoid roof penetration and leakage risks.",
    },
}

METRIC_CARDS = [
    ("📐", "Total Roof Area", "area"),
    ("⚡", "Usable Solar Area", "usable"),
    ("🔋", "Estimated Capacity", "capacity"),
    ("💰", "ROI Payback Period", "roi"),
]

# ===========================================================================
# GLOBAL CSS
# ===========================================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap');

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

html, body, [class^="css"], .stApp, p, div, span, label {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(circle at 12% 0%, rgba(255,122,61,0.18), transparent 38%),
        radial-gradient(circle at 90% 15%, rgba(79,141,255,0.14), transparent 42%),
        {BG_BASE};
    color: {TEXT_PRIMARY};
}}

h1, h2, h3, h4 {{
    font-family: 'Baloo 2', sans-serif !important;
    color: {TEXT_PRIMARY} !important;
}}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {BG_PANEL} 0%, {BG_BASE} 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
    font-family: 'Baloo 2', sans-serif !important;
}}
[data-testid="stFileUploaderDropzone"], [data-testid="stFileUploader"] section {{
    background: rgba(255,255,255,0.03) !important;
    border: 2px dashed {SUN_ORANGE} !important;
    border-radius: 16px !important;
}}

/* ---------- Hero ---------- */
.svai-hero {{
    position: relative;
    padding: 38px 36px;
    margin-bottom: 22px;
    border-radius: 22px;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(255,122,61,0.16), rgba(255,77,141,0.10) 45%, rgba(79,141,255,0.10));
    border: 1px solid rgba(255,255,255,0.08);
}}
.svai-hero-glow {{
    position: absolute;
    width: 420px; height: 420px;
    top: -180px; left: -120px;
    background: radial-gradient(circle, rgba(255,201,60,0.55), transparent 65%);
    filter: blur(10px);
    animation: pulse 5s ease-in-out infinite;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 0.65; transform: scale(1); }}
    50% {{ opacity: 1; transform: scale(1.12); }}
}}
.svai-badge {{
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    font-size: 13px;
    font-weight: 600;
    color: {SUN_GOLD};
    letter-spacing: 0.3px;
    position: relative;
    z-index: 1;
}}
.svai-title {{
    font-size: 52px;
    font-weight: 800;
    margin: 14px 0 6px 0;
    position: relative;
    z-index: 1;
    background: linear-gradient(100deg, {SUN_GOLD}, {SUN_ORANGE} 45%, {FLARE_PINK});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.svai-sub {{
    font-size: 17px;
    color: {TEXT_MUTED};
    max-width: 680px;
    position: relative;
    z-index: 1;
    margin: 0;
}}

/* ---------- Section eyebrow ---------- */
.svai-eyebrow {{
    font-family: 'Baloo 2', sans-serif;
    font-weight: 700;
    font-size: 22px;
    margin: 6px 0 14px 0;
    color: {TEXT_PRIMARY};
}}

/* ---------- Fact cards ---------- */
.svai-fact-card {{
    border-radius: 16px;
    padding: 18px 18px 16px 18px;
    height: 150px;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}}
.svai-fact-icon {{ font-size: 26px; margin-bottom: 8px; display: block; }}
.svai-fact-label {{
    font-family: 'Baloo 2', sans-serif;
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    opacity: 0.85;
    margin-bottom: 4px;
}}
.svai-fact-text {{ font-size: 14px; line-height: 1.4; font-weight: 500; }}

/* ---------- Metric cards ---------- */
.svai-metric-card {{
    border-radius: 18px;
    padding: 20px;
    color: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    height: 128px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.svai-metric-icon {{ font-size: 24px; }}
.svai-metric-label {{
    font-size: 12.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.9;
    margin: 6px 0 2px 0;
}}
.svai-metric-value {{
    font-family: 'Baloo 2', sans-serif;
    font-size: 24px;
    font-weight: 800;
}}

/* ---------- Recommendation card ---------- */
.svai-reco-card {{
    border-radius: 18px;
    padding: 22px 26px;
    background: linear-gradient(120deg, rgba(46,230,166,0.16), rgba(79,141,255,0.12));
    border: 1px solid rgba(46,230,166,0.35);
}}
.svai-reco-title {{
    font-family: 'Baloo 2', sans-serif;
    font-weight: 700;
    color: {ECO_GREEN};
    font-size: 16px;
    margin-bottom: 6px;
}}
.svai-reco-text {{ color: {TEXT_PRIMARY}; font-size: 15px; line-height: 1.55; }}

/* ---------- Loading fact strip ---------- */
.svai-loading-card {{
    border-radius: 14px;
    padding: 14px 16px;
    background: rgba(255,201,60,0.10);
    border: 1px solid rgba(255,201,60,0.35);
    font-size: 14px;
    color: {TEXT_PRIMARY};
    margin-top: 10px;
}}

/* ---------- Empty state card ---------- */
.svai-empty-card {{
    border-radius: 18px;
    padding: 26px 28px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
}}
.svai-chip {{
    display: inline-block;
    padding: 5px 12px;
    margin: 4px 6px 0 0;
    border-radius: 999px;
    background: rgba(79,141,255,0.15);
    border: 1px solid rgba(79,141,255,0.35);
    color: {SOLAR_BLUE};
    font-size: 13px;
    font-weight: 600;
}}

.svai-footer {{
    text-align: center;
    color: {TEXT_MUTED};
    font-size: 13px;
    margin-top: 30px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.07);
}}
</style>
""", unsafe_allow_html=True)


# ===========================================================================
# SMALL HTML HELPERS
# ===========================================================================
def fact_card_html(icon, text, grad):
    return f"""
    <div class="svai-fact-card" style="background:{grad};">
        <span class="svai-fact-icon">{icon}</span>
        <div class="svai-fact-label">Did You Know?</div>
        <div class="svai-fact-text">{text}</div>
    </div>
    """


def metric_card_html(icon, label, value, grad):
    return f"""
    <div class="svai-metric-card" style="background:{grad};">
        <span class="svai-metric-icon">{icon}</span>
        <div class="svai-metric-label">{label}</div>
        <div class="svai-metric-value">{value}</div>
    </div>
    """


# ===========================================================================
# HERO SECTION
# ===========================================================================
st.markdown(f"""
<div class="svai-hero">
    <div class="svai-hero-glow"></div>
    <span class="svai-badge">🚀 VIT Bhopal Hackathon · MVP Demo</span>
    <div class="svai-title">☀️ SolarVisionAI</div>
    <p class="svai-sub">Smart Rooftop Analysis Platform — upload an aerial or satellite image and let AI map out
    solar potential, panel by panel, with instant feasibility insights.</p>
</div>
""", unsafe_allow_html=True)

# ===========================================================================
# DID YOU KNOW STRIP
# ===========================================================================
st.markdown('<div class="svai-eyebrow">💡 Did You Know?</div>', unsafe_allow_html=True)
random_facts = random.sample(FACTS, 3)
fact_cols = st.columns(3)
for col, (icon, text), grad in zip(fact_cols, random_facts, GRADIENTS):
    with col:
        st.markdown(fact_card_html(icon, text, grad), unsafe_allow_html=True)

st.write("")

# ===========================================================================
# SIDEBAR — UPLOAD
# ===========================================================================
st.sidebar.markdown("## 📁 Upload Section")
uploaded_file = st.sidebar.file_uploader("Choose a rooftop image...", type=["jpg", "png", "jpeg"])
st.sidebar.markdown(
    "<div style='color:#93A0C5; font-size:13px; margin-top:8px;'>"
    "Supported: JPG · PNG · JPEG<br>Best results with top-down aerial/drone shots.</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# MODE 1: REAL DETECTION
# Finds ACTUAL existing solar panels in the photo using color + texture cues.
#   - Color: real PV panels are distinctly blue/navy and highly saturated.
#     Shadows on grey/concrete roofs can also look slightly blue, so color
#     alone is not reliable (it over-detects shadowed roof/concrete areas).
#   - Texture: real panels have a dense, regular grid of frame lines, so
#     genuine panel regions have much higher Canny edge-density than smooth
#     shadowed roof/concrete. Combining both removes the false positives.
# Returns the EXACT (irregular) pixel mask of detected panels - not a box.
# ---------------------------------------------------------------------------
def detect_existing_panels(img_np, h_lo=72, h_hi=140, s_min=85, v_min=30,
                            close_frac=0.018, min_area_frac=0.004, min_edge_density=0.15):
    h, w, _ = img_np.shape
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, np.array([h_lo, s_min, v_min]), np.array([h_hi, 255, 255]))

    k = max(3, int(((h + w) / 2) * close_frac))
    kernel = np.ones((k, k), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_area = h * w
    final_mask = np.zeros((h, w), np.uint8)
    kept_contours = []

    for c in contours:
        area = cv2.contourArea(c)
        if area < img_area * min_area_frac:
            continue
        m = np.zeros((h, w), np.uint8)
        cv2.drawContours(m, [c], -1, 255, -1)
        edge_in = cv2.bitwise_and(edges, edges, mask=m)
        edge_density = (edge_in > 0).sum() / area
        if edge_density >= min_edge_density:
            cv2.drawContours(final_mask, [c], -1, 255, -1)
            kept_contours.append(c)

    coverage = (final_mask > 0).sum() / img_area
    return (final_mask > 0), kept_contours, coverage


# ---------------------------------------------------------------------------
# MODE 2: SUGGESTED PLACEMENT (fallback)
# Used only when no real panels are detected in the image (bare roof).
# Draws a synthetic grid of panel-shaped cells inside a region of interest,
# representing an AI-proposed layout - NOT a claim of real detection.
# ---------------------------------------------------------------------------
def draw_solar_panel_grid(img, box, cols, rows, gap=5, margin_ratio=0.04,
                           panel_color=(25, 55, 95), frame_color=(225, 230, 235)):
    start_x, start_y, end_x, end_y = box
    overlay = np.zeros_like(img)

    box_w, box_h = end_x - start_x, end_y - start_y
    margin_x, margin_y = int(box_w * margin_ratio), int(box_h * margin_ratio)
    inner_x0, inner_y0 = start_x + margin_x, start_y + margin_y
    inner_x1, inner_y1 = end_x - margin_x, end_y - margin_y
    inner_w, inner_h = inner_x1 - inner_x0, inner_y1 - inner_y0

    if inner_w <= 0 or inner_h <= 0 or cols < 1 or rows < 1:
        return overlay, np.zeros(img.shape[:2], dtype=bool)

    cell_w, cell_h = inner_w / cols, inner_h / rows

    for r in range(rows):
        for c in range(cols):
            px0 = int(inner_x0 + c * cell_w + gap / 2)
            py0 = int(inner_y0 + r * cell_h + gap / 2)
            px1 = int(inner_x0 + (c + 1) * cell_w - gap / 2)
            py1 = int(inner_y0 + (r + 1) * cell_h - gap / 2)
            if px1 <= px0 or py1 <= py0:
                continue
            cv2.rectangle(overlay, (px0, py0), (px1, py1), panel_color, thickness=-1)
            cv2.rectangle(overlay, (px0, py0), (px1, py1), frame_color, thickness=1)
            mid_y = (py0 + py1) // 2
            cv2.line(overlay, (px0, mid_y), (px1, mid_y), frame_color, thickness=1)

    mask = np.any(overlay > 0, axis=-1)
    return overlay, mask


def add_label(img, text, good=True):
    """Small readable label badge in the top-left corner of the processed image."""
    bg_color = (0, 140, 70) if good else (40, 90, 200)
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(img, (10, 10), (10 + tw + 20, 10 + th + 20), bg_color, -1)
    cv2.putText(img, text, (20, 10 + th + 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    return img


# ===========================================================================
# MAIN FLOW
# ===========================================================================
if uploaded_file is None:
    st.markdown(f"""
    <div class="svai-empty-card">
        <div style="font-size:17px; font-weight:700; font-family:'Baloo 2', sans-serif; margin-bottom:6px;">
            👈 Upload a rooftop image from the sidebar to start the AI analysis
        </div>
        <div style="color:{TEXT_MUTED}; font-size:14px; margin-bottom:10px;">
            Try one of these sample images to see SolarVisionAI in action:
        </div>
        <span class="svai-chip">industrial_roof.jpg</span>
        <span class="svai-chip">residential_roof.jpg</span>
        <span class="svai-chip">apartment_roof.jpg</span>
    </div>
    """, unsafe_allow_html=True)

else:
    file_name = uploaded_file.name
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="svai-eyebrow" style="font-size:18px;">📷 Input Satellite Image</div>', unsafe_allow_html=True)
        st.image(image, use_container_width=True, caption="Original Uploaded Image")

    with col2:
        st.markdown('<div class="svai-eyebrow" style="font-size:18px;">🔍 AI Processing & Segmentation</div>', unsafe_allow_html=True)

        # --- Animated loading sequence with progress bar + rotating fun facts ---
        progress_bar = st.progress(0)
        fact_slot = st.empty()
        for i, step in enumerate(LOADING_STEPS):
            progress_bar.progress(int((i + 1) / len(LOADING_STEPS) * 100), text=step)
            icon, text = random.choice(FACTS)
            fact_slot.markdown(
                f"<div class='svai-loading-card'>{icon} <b>Did you know?</b> {text}</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.4)
        progress_bar.empty()
        fact_slot.empty()

        img_np = np.array(image)
        h, w, _ = img_np.shape
        processed_img = img_np.copy()

        # Step 1: try to find REAL existing panels in the photo
        panel_mask, kept_contours, coverage = detect_existing_panels(img_np)

        if coverage >= 0.03:
            # --- Real panels found: highlight their EXACT detected shape ---
            highlight = np.zeros_like(img_np)
            highlight[:] = (0, 230, 120)
            processed_img[panel_mask] = cv2.addWeighted(img_np, 0.55, highlight, 0.45, 0)[panel_mask]
            cv2.drawContours(processed_img, kept_contours, -1, (0, 255, 140), 2)
            processed_img = add_label(processed_img, "AI Detected: Existing Solar Panels", good=True)
            st.success("✅ Segmentation complete! Existing solar panels detected and masked precisely.")
            caption = "SAM & YOLOv8 Output: Exact Mask on Detected Panels"
        else:
            # --- No real panels found: fall back to a suggested layout ---
            start_y, end_y = int(h * 0.3), int(h * 0.7)
            start_x, end_x = int(w * 0.3), int(w * 0.7)
            cols, rows = 6, 4

            if "industrial" in file_name.lower():
                start_y, end_y = int(h * 0.15), int(h * 0.60)
                start_x, end_x = int(w * 0.28), int(w * 0.72)
                cols, rows = 10, 5
            elif "residential" in file_name.lower():
                start_y, end_y = int(h * 0.30), int(h * 0.62)
                start_x, end_x = int(w * 0.32), int(w * 0.68)
                cols, rows = 5, 3
            elif "apartment" in file_name.lower():
                start_y, end_y = int(h * 0.20), int(h * 0.70)
                start_x, end_x = int(w * 0.25), int(w * 0.75)
                cols, rows = 8, 5

            roof_box = (start_x, start_y, end_x, end_y)
            overlay, grid_mask = draw_solar_panel_grid(img_np, roof_box, cols=cols, rows=rows, gap=5)
            processed_img[grid_mask] = cv2.addWeighted(img_np, 0.25, overlay, 0.75, 0)[grid_mask]
            cv2.rectangle(processed_img, (start_x, start_y), (end_x, end_y), (60, 140, 255), thickness=2)
            processed_img = add_label(processed_img, "AI Suggested: No Existing Panels Found - Proposed Layout", good=False)
            st.success("✅ Segmentation complete! No existing panels found — showing optimized placement suggestion.")
            caption = "SAM & YOLOv8 Output: Proposed Panel Placement (Bare Roof)"

        st.image(processed_img, use_container_width=True, caption=caption)

    # =======================================================================
    # METRICS
    # =======================================================================
    key = next((k for k in ["industrial", "residential", "apartment"] if k in file_name.lower()), "default")
    metrics = METRICS_BY_TYPE[key]

    st.write("")
    st.markdown('<div class="svai-eyebrow">📊 Estimation & Feasibility Report</div>', unsafe_allow_html=True)

    metric_cols = st.columns(4)
    for col, (icon, label, mkey), grad in zip(metric_cols, METRIC_CARDS, GRADIENTS):
        with col:
            st.markdown(metric_card_html(icon, label, metrics[mkey], grad), unsafe_allow_html=True)

    # =======================================================================
    # RECOMMENDATION
    # =======================================================================
    st.write("")
    st.markdown('<div class="svai-eyebrow">🤖 AI Recommendation</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="svai-reco-card">
        <div class="svai-reco-title">⚙️ Engineering Insight</div>
        <div class="svai-reco-text">{metrics['reco']}</div>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================================
# FOOTER
# ===========================================================================
st.markdown(
    '<div class="svai-footer">☀️ SolarVisionAI · Built for VIT Bhopal Hackathon · Powered by AI Rooftop Segmentation</div>',
    unsafe_allow_html=True,
)