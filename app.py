import streamlit as st
import pandas as pd
from datetime import date

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Daily Bible Reading",
    page_icon="✝",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&family=EB+Garamond:ital@0;1&display=swap');

/* ── Root tokens ── */
:root {
    --cream:   #F7F3EC;
    --parchment: #EDE5D5;
    --gold:    #B8924A;
    --gold-lt: #D4AC6E;
    --ink:     #2C2416;
    --ink-muted: #6B5B3E;
    --border:  #C9B48A;
    --shadow:  rgba(44,36,22,0.12);
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--cream) !important;
    font-family: 'EB Garamond', Georgia, serif;
    color: var(--ink);
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
.block-container { max-width: 680px !important; padding-top: 2rem !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 2rem 2rem;
    background: var(--parchment);
    border: 1px solid var(--border);
    border-radius: 4px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    inset: 8px;
    border: 1px solid var(--border);
    border-radius: 2px;
    pointer-events: none;
    opacity: 0.5;
}
.hero-cross {
    font-size: 2rem;
    color: var(--gold);
    letter-spacing: 0.3em;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: 'Cinzel', serif;
    font-size: 2rem;
    font-weight: 600;
    color: var(--ink);
    letter-spacing: 0.08em;
    line-height: 1.2;
    margin: 0 0 0.4rem;
}
.hero-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.15rem;
    color: var(--ink-muted);
    margin: 0;
}
.gold-rule {
    border: none;
    border-top: 1px solid var(--gold);
    width: 60px;
    margin: 1rem auto;
    opacity: 0.6;
}

/* ── Date badge ── */
.date-badge {
    display: inline-block;
    background: var(--ink);
    color: var(--cream);
    font-family: 'Cinzel', serif;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    padding: 0.45rem 1.4rem;
    border-radius: 2px;
    margin-bottom: 1.8rem;
}

/* ── Button override ── */
div[data-testid="stButton"] > button {
    background: var(--ink) !important;
    color: var(--cream) !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.18em !important;
    border: 1px solid var(--ink) !important;
    border-radius: 2px !important;
    padding: 0.65rem 2.5rem !important;
    transition: background 0.2s, color 0.2s !important;
    width: 100%;
}
div[data-testid="stButton"] > button:hover {
    background: var(--gold) !important;
    border-color: var(--gold) !important;
}

/* ── Reading card ── */
.reading-card {
    background: var(--parchment);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2rem 2.2rem;
    margin-top: 1.6rem;
    position: relative;
}
.reading-card::before {
    content: "";
    position: absolute;
    inset: 7px;
    border: 1px solid var(--border);
    border-radius: 2px;
    pointer-events: none;
    opacity: 0.4;
}
.reading-label {
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.reading-passage {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 300;
    color: var(--ink);
    line-height: 1.3;
    margin-bottom: 0.3rem;
}
.reading-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0;
}
.verse-of-day {
    font-family: 'EB Garamond', serif;
    font-style: italic;
    font-size: 1rem;
    color: var(--ink-muted);
    text-align: center;
    padding: 1.4rem 1rem 0;
    line-height: 1.7;
}
.no-reading {
    text-align: center;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    color: var(--ink-muted);
    font-size: 1.15rem;
    padding: 1.5rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 0.9rem;
    color: var(--ink-muted);
    margin-top: 3rem;
    padding-bottom: 2rem;
    opacity: 0.7;
}
</style>
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
    <div class="hero-cross">✦ ✝ ✦</div>
    <h1 class="hero-title">Daily Bible Reading</h1>
    <hr class="gold-rule">
    <p class="hero-subtitle">A plan for encountering God's Word each day</p>
</div>
""", unsafe_allow_html=True)

# ── Date badge ─────────────────────────────────────────────────────────────────
day_str = today.strftime("%A, %B %-d, %Y").upper()
st.markdown(f'<div style="text-align:center"><span class="date-badge">{day_str}</span></div>', unsafe_allow_html=True)

# ── Button ─────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    show = st.button("Open Today's Reading")

# ── Reading card ───────────────────────────────────────────────────────────────
if show:
    if not data_loaded:
        st.markdown('<div class="reading-card"><p class="no-reading">Could not load <em>bible_reading_plan.csv</em>. Please ensure the file is in the same directory.</p></div>', unsafe_allow_html=True)
    elif not today_reading.empty:
        passage1 = today_reading.iloc[0]["Passage 1"]
        passage2 = today_reading.iloc[0]["Passage 2"]
        st.markdown(f"""
        <div class="reading-card">
            <div class="reading-label">First Reading</div>
            <div class="reading-passage">{passage1}</div>
            <hr class="reading-divider">
            <div class="reading-label">Second Reading</div>
            <div class="reading-passage">{passage2}</div>
            <div class="verse-of-day">
                "Your word is a lamp to my feet and a light to my path."<br>
                <span style="font-size:0.85rem; letter-spacing:0.08em;">— Psalm 119:105</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="reading-card"><p class="no-reading">No reading is scheduled for today.<br>Rest, reflect, and give thanks.</p></div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Sola Scriptura &nbsp;·&nbsp; Scripture alone</div>', unsafe_allow_html=True)