import streamlit as st
import pandas as pd
from datetime import date

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Daily Bible Reading",
    page_icon="🌙",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Syne:wght@700;800&display=swap');

:root {
    --bg:        #07080F;
    --surface:   #0E1120;
    --surface2:  #151829;
    --moon:      #C8D6F0;
    --moon-glow: #8FABD4;
    --star:      #E8EEF8;
    --accent:    #4A6FA5;
    --accent-lt: #7BA3D4;
    --muted:     #5A6580;
    --border:    #1E2440;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Space Grotesk', sans-serif;
    color: var(--star);
}

[data-testid="stHeader"]          { background: transparent !important; display: none; }
[data-testid="stSidebar"]         { display: none; }
[data-testid="stToolbar"]         { display: none !important; }
[data-testid="stDecoration"]      { display: none !important; }
[data-testid="stMainMenuButton"]  { display: none !important; }
footer                            { display: none !important; }
.block-container { max-width: 660px !important; padding-top: 1.5rem !important; }

/* ── Starfield canvas ── */
#stars-canvas {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
}

/* ── All content above stars ── */
.block-container { position: relative; z-index: 1; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 2rem 2.5rem;
    background: linear-gradient(160deg, #0E1120 0%, #0A0D1A 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(74,111,165,0.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.moon-icon {
    font-size: 3.2rem;
    display: block;
    margin-bottom: 0.6rem;
    filter: drop-shadow(0 0 18px rgba(200,214,240,0.5));
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--moon);
    letter-spacing: -0.01em;
    margin: 0 0 0.5rem;
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0;
}

/* ── Date badge ── */
.date-badge {
    display: inline-block;
    background: var(--surface2);
    color: var(--moon-glow);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.5rem 1.5rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    margin-bottom: 1.8rem;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.72rem 2rem !important;
    transition: background 0.2s, box-shadow 0.2s !important;
    width: 100%;
    box-shadow: 0 0 0 0 rgba(74,111,165,0) !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--accent-lt) !important;
    box-shadow: 0 0 24px rgba(74,111,165,0.45) !important;
}

/* ── Reading card ── */
.reading-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    margin-top: 1.4rem;
}
.reading-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent-lt);
    margin-bottom: 0.5rem;
}
.reading-passage {
    font-family: 'Syne', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--moon);
    line-height: 1.25;
    margin-bottom: 0.2rem;
}
.reading-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.3rem 0;
}
.no-reading {
    text-align: center;
    font-weight: 600;
    color: var(--muted);
    font-size: 1rem;
    padding: 1rem;
}

/* ── Copy link button ── */
.copy-row {
    display: flex;
    justify-content: flex-end;
    margin-top: 1.4rem;
}
.copy-btn {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 999px;
    color: var(--moon-glow);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.42rem 1.1rem;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}
.copy-btn:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
</style>

<!-- Starfield -->
<canvas id="stars-canvas"></canvas>
<script>
(function(){
    const c = document.getElementById('stars-canvas');
    const ctx = c.getContext('2d');
    let stars = [];
    function resize(){
        c.width = window.innerWidth;
        c.height = window.innerHeight;
    }
    function init(){
        stars = [];
        for(let i=0;i<160;i++){
            stars.push({
                x: Math.random()*c.width,
                y: Math.random()*c.height,
                r: Math.random()*1.4+0.2,
                a: Math.random(),
                speed: Math.random()*0.004+0.001
            });
        }
    }
    function draw(){
        ctx.clearRect(0,0,c.width,c.height);
        stars.forEach(s=>{
            s.a += s.speed;
            const alpha = 0.3 + 0.7*Math.abs(Math.sin(s.a));
            ctx.beginPath();
            ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
            ctx.fillStyle = `rgba(200,214,240,${alpha})`;
            ctx.fill();
        });
        requestAnimationFrame(draw);
    }
    resize(); init(); draw();
    window.addEventListener('resize',()=>{ resize(); init(); });
})();
</script>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_bible_plan():
    bible = pd.read_csv("bible_reading_plan.csv")
    current_year = date.today().year
    bible["Date"] = pd.to_datetime(
        bible["Date"] + "-" + str(current_year),
        format="%d-%b-%Y"
    ).dt.date
    return bible

try:
    bible = load_bible_plan()
    today = date.today()
    today_reading = bible[bible["Date"] == today]
    data_loaded = True
except Exception:
    data_loaded = False
    today = date.today()
    today_reading = pd.DataFrame()

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="moon-icon">🌙</span>
    <h1 class="hero-title">Daily Bible Reading</h1>
    <p class="hero-subtitle">God's Word · Every Day</p>
</div>
""", unsafe_allow_html=True)

# ── Date badge ─────────────────────────────────────────────────────────────────
day_str = today.strftime("%A, %B %-d, %Y").upper()
st.markdown(f'<div style="text-align:center"><span class="date-badge">🌟 {day_str}</span></div>', unsafe_allow_html=True)

# ── Button ─────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    show = st.button("Open Today's Reading")

# ── Reading card ───────────────────────────────────────────────────────────────
if show:
    if not data_loaded:
        st.markdown('<div class="reading-card"><p class="no-reading">Could not load bible_reading_plan.csv — make sure it\'s in the same folder.</p></div>', unsafe_allow_html=True)
    elif not today_reading.empty:
        passage1 = today_reading.iloc[0]["Passage 1"]
        passage2 = today_reading.iloc[0]["Passage 2"]
        page_url = "?date=" + today.strftime("%Y-%m-%d")
        st.markdown(f"""
        <div class="reading-card">
            <div class="reading-label">First Reading</div>
            <div class="reading-passage">{passage1}</div>
            <hr class="reading-divider">
            <div class="reading-label">Second Reading</div>
            <div class="reading-passage">{passage2}</div>
            <div class="copy-row">
                <button class="copy-btn" onclick="navigator.clipboard.writeText(window.location.href).then(()=>{{this.innerText='✓ Copied!';setTimeout(()=>{{this.innerHTML='🔗 Copy Link'}},1800)}})">
                    🔗 Copy Link
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="reading-card"><p class="no-reading">No reading scheduled for today.</p></div>', unsafe_allow_html=True)