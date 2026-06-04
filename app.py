import streamlit as st
import pandas as pd
import urllib.parse
from datetime import date, datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Daily Bible Reading",
    page_icon="🌙",
    layout="centered",
)
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,700;0,900;1,700&family=Manrope:wght@400;500;600;700&display=swap');

:root {
    --bg:         #080B14;
    --surface:    rgba(18, 24, 43, 0.72);
    --surface2:   rgba(14, 19, 36, 0.6);
    --gold:       #F4C95D;
    --gold-dim:   rgba(244, 201, 93, 0.15);
    --cream:      #F5EBD0;
    --cream-dim:  rgba(245, 235, 208, 0.65);
    --soft-blue:  #8FB8E8;
    --blue-dim:   rgba(143, 184, 232, 0.12);
    --muted:      rgba(245, 235, 208, 0.38);
    --border:     rgba(160, 180, 220, 0.16);
    --border-gold:rgba(244, 201, 93, 0.28);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Manrope', sans-serif;
    color: var(--cream);
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at 50% 0%, #17213A 0%, #080B14 45%, #05060B 100%);
    z-index: 0;
    pointer-events: none;
}

/* grain overlay */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    background-size: 180px;
    opacity: 0.55;
    z-index: 0;
    pointer-events: none;
}

[data-testid="stHeader"]         { display: none !important; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stMainMenuButton"] { display: none !important; }
footer                           { display: none !important; }
.block-container {
    max-width: 600px !important;
    padding-top: 2rem !important;
    position: relative;
    z-index: 1;
}

/* starfield */
#stars-canvas {
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.6rem 2rem 2rem;
    background: rgba(12, 17, 35, 0.5);
    border: 1px solid var(--border);
    border-radius: 24px;
    margin-bottom: 1.4rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
}
.hero::before {
    content: "";
    position: absolute;
    top: -80px; left: 50%; transform: translateX(-50%);
    width: 260px; height: 160px;
    background: radial-gradient(ellipse, rgba(244,201,93,0.09) 0%, transparent 70%);
    pointer-events: none;
}
.moon-icon {
    font-size: 2.2rem;
    display: block;
    margin-bottom: 0.7rem;
    filter: drop-shadow(0 0 10px rgba(244,201,93,0.35));
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 2.3rem;
    font-weight: 900;
    color: var(--cream);
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem;
    line-height: 1.05;
}
.hero-subtitle {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.7;
    margin: 0;
}

/* ── Date pill ── */
.date-badge {
    display: inline-block;
    color: var(--gold);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.42rem 1.3rem;
    border-radius: 999px;
    border: 1px solid var(--border-gold);
    background: var(--gold-dim);
    margin-bottom: 1.3rem;
}

/* ── Main button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2A3D6E 0%, #1E2E54 100%) !important;
    color: var(--cream) !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    border: 1px solid rgba(143,184,232,0.25) !important;
    border-radius: 999px !important;
    padding: 0.68rem 2rem !important;
    transition: all 0.2s !important;
    width: 100%;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #344D86 0%, #27397A 100%) !important;
    border-color: rgba(244,201,93,0.35) !important;
    box-shadow: 0 4px 32px rgba(143,184,232,0.18) !important;
}

/* ── Reading card ── */
.reading-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-top: 1.2rem;
    backdrop-filter: blur(18px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
}
.card-intro {
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--muted);
    font-style: italic;
    margin-bottom: 1.4rem;
    letter-spacing: 0.01em;
}
.reading-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.4rem;
    opacity: 0.85;
}
.passage-link {
    display: inline-flex;
    align-items: baseline;
    gap: 0.3rem;
    color: var(--cream);
    text-decoration: none;
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.2;
    transition: color 0.18s;
}
.passage-link .ext {
    font-family: 'Manrope', sans-serif;
    font-size: 0.78rem;
    color: var(--soft-blue);
    opacity: 0.7;
    transition: opacity 0.18s;
    font-weight: 600;
}
.passage-link:hover { color: var(--gold); }
.passage-link:hover .ext { opacity: 1; }

.reading-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0;
}
.bottom-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1.3rem;
}
.esv-badge {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--muted);
    text-transform: uppercase;
}
.copy-btn {
    background: var(--blue-dim);
    border: 1px solid var(--border);
    border-radius: 999px;
    color: var(--soft-blue);
    font-family: 'Manrope', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 0.38rem 1rem;
    cursor: pointer;
    transition: all 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}
.copy-btn:hover {
    background: rgba(244,201,93,0.12);
    border-color: var(--border-gold);
    color: var(--gold);
}
.no-reading {
    text-align: center;
    font-weight: 500;
    color: var(--muted);
    font-size: 0.95rem;
    padding: 1rem;
    font-style: italic;
}
</style>

<canvas id="stars-canvas"></canvas>
<script>
(function(){
    const c = document.getElementById('stars-canvas');
    const ctx = c.getContext('2d');
    let stars = [];
    function resize(){ c.width = window.innerWidth; c.height = window.innerHeight; }
    function init(){
        stars = [];
        for(let i=0;i<130;i++){
            const warm = Math.random() < 0.12;
            stars.push({
                x: Math.random()*c.width, y: Math.random()*c.height,
                r: Math.random()*1.2+0.15,
                a: Math.random(), sp: Math.random()*0.003+0.0008,
                warm
            });
        }
    }
    function draw(){
        ctx.clearRect(0,0,c.width,c.height);
        stars.forEach(s=>{
            s.a += s.sp;
            const alpha = 0.2 + 0.65*Math.abs(Math.sin(s.a));
            ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
            ctx.fillStyle = s.warm
                ? `rgba(244,201,93,${alpha * 0.8})`
                : `rgba(200,218,245,${alpha})`;
            ctx.fill();
        });
        requestAnimationFrame(draw);
    }
    resize(); init(); draw();
    window.addEventListener('resize',()=>{ resize(); init(); });
})();
</script>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def bible_gateway_url(passage: str) -> str:
    query = urllib.parse.quote(passage.strip())
    return f"https://www.biblegateway.com/passage/?search={query}&version=ESV"

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_bible_plan():
    bible = pd.read_csv("bible_reading_plan.csv")
    current_year = date.today().year
    bible["Date"] = pd.to_datetime(
        bible["Date"] + "-" + str(current_year), format="%d-%b-%Y"
    ).dt.date
    return bible

try:
    bible = load_bible_plan()
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    today_reading = bible[bible["Date"] == today]
    
    data_loaded = True
except Exception:
    data_loaded = False
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    today_reading = pd.DataFrame()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="moon-icon">🌙</span>
    <h1 class="hero-title">Daily Bible Reading</h1>
    <p class="hero-subtitle">God's Word · Every Day</p>
</div>
""", unsafe_allow_html=True)

# ── Date pill ─────────────────────────────────────────────────────────────────
day_str = today.strftime("%A, %B %-d, %Y").upper()
st.markdown(f'<div style="text-align:center"><span class="date-badge">{day_str}</span></div>', unsafe_allow_html=True)

# ── Button ────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    show = st.button("Open Today's Reading")

# ── Reading card ──────────────────────────────────────────────────────────────
if show:
    if not data_loaded:
        st.markdown('<div class="reading-card"><p class="no-reading">Could not load bible_reading_plan.csv — make sure it\'s in the same folder.</p></div>', unsafe_allow_html=True)
    elif not today_reading.empty:
        passage1 = today_reading.iloc[0]["Passage 1"]
        passage2 = today_reading.iloc[0]["Passage 2"]
        url1 = bible_gateway_url(passage1)
        url2 = bible_gateway_url(passage2)
        st.markdown(f"""
        <div class="reading-card">
            <p class="card-intro">A quiet reading for today.</p>
            <div class="reading-label">First Reading</div>
            <a class="passage-link" href="{url1}" target="_blank" rel="noopener">
                {passage1} <span class="ext">↗</span>
            </a>
            <hr class="reading-divider">
            <div class="reading-label">Second Reading</div>
            <a class="passage-link" href="{url2}" target="_blank" rel="noopener">
                {passage2} <span class="ext">↗</span>
            </a>
            <div class="bottom-row">
                <span class="esv-badge">ESV · Bible Gateway</span>
                <button class="copy-btn" onclick="navigator.clipboard.writeText(window.location.href).then(()=>{{this.innerText='✓ Copied!';setTimeout(()=>{{this.innerHTML='🔗 Copy Link'}},1800)}})">
                    🔗 Copy Link
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="reading-card"><p class="no-reading">No reading scheduled for today.</p></div>', unsafe_allow_html=True)
