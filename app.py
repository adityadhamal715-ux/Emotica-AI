"""
app.py
======
Home / entry point for Emotica AI. Streamlit auto-discovers everything
under pages/ and builds the sidebar navigation (Live Detection,
Analytics, Song Manager, Settings, About) from those files — this
script only renders the Home dashboard and initializes shared session
state used by every page.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import streamlit as st

import config
from database import Database
from emotion_model import model_is_available
from music_player import MusicPlayer
from utils import inject_global_css, metric_card, render_header, status_badge

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------------------------------- #
# Shared session state — every page reads/writes these same keys so state
# (camera on/off, last detection, settings, etc.) is consistent app-wide.
# --------------------------------------------------------------------------- #
def init_session_state() -> None:
    defaults = {
        "camera_running": False,
        "current_emotion": None,
        "current_confidence": 0.0,
        "current_song": None,
        "current_fps": 0.0,
        "camera_resolution": "480p (640x480)",
        "camera_fps_target": config.DEFAULT_TARGET_FPS,
        "music_volume": 0.6,
        "auto_play": True,
        "confidence_threshold": config.DEFAULT_CONFIDENCE_THRESHOLD,
        "theme_mode": "Dark (default)",
    }
    for key, val in defaults.items():
        st.session_state.setdefault(key, val)

    if "db" not in st.session_state:
        st.session_state.db = Database()
    if "music_player" not in st.session_state:
        st.session_state.music_player = MusicPlayer()


init_session_state()
inject_global_css()

# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.markdown(f"## 🎧 {config.APP_NAME}")
    st.caption(config.APP_TAGLINE)
    st.divider()
    st.markdown("**Use the pages above to navigate:**")
    st.markdown(
        "- 🏠 Home\n"
        "- 📷 Live Detection\n"
        "- 📊 Analytics\n"
        "- 🎵 Song Manager\n"
        "- ⚙️ Settings\n"
        "- ℹ️ About Project"
    )
    st.divider()
    model_state = "online" if model_is_available() else "offline"
    st.markdown(status_badge("AI Model", model_state), unsafe_allow_html=True)
    cam_state = "online" if st.session_state.camera_running else "idle"
    st.markdown(status_badge("Camera", cam_state), unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Home dashboard
# --------------------------------------------------------------------------- #
render_header()

if not model_is_available():
    st.warning(
        "**Emotion model not found.** Train it first: place `fer2013.csv` in "
        "`data/` and run `python train_model.py` from the project folder. "
        "The Live Detection page will stay disabled until "
        f"`{config.MODEL_PATH.name}` exists in `models/`.",
        icon="⚠️",
    )

total_songs = sum(len(v) for v in st.session_state.music_player.all_songs().values())
if total_songs == 0:
    st.info(
        "**No songs loaded yet.** Drop mp3/wav/ogg files into the mood folders "
        "under `songs/` (see the Song Manager page) — files are picked up "
        "automatically, nothing to configure.",
        icon="🎵",
    )

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Detected Emotion", st.session_state.current_emotion or "—")
with col2:
    conf = st.session_state.current_confidence
    metric_card("Confidence", f"{conf * 100:.0f}%" if conf else "—")
with col3:
    metric_card("Current Song", st.session_state.current_song or "None")
with col4:
    metric_card("Live FPS", f"{st.session_state.current_fps:.1f}")

col5, col6, col7, col8 = st.columns(4)
with col5:
    metric_card("Camera Status", "Running" if st.session_state.camera_running else "Stopped")
with col6:
    metric_card("AI Status", "Ready" if model_is_available() else "Model Missing")
with col7:
    metric_card("Music Status", "Playing" if st.session_state.music_player.is_playing else "Idle")
with col8:
    metric_card("Current Time", dt.datetime.now().strftime("%H:%M:%S"))

st.divider()

db: Database = st.session_state.db
lcol, rcol = st.columns([2, 1])
with lcol:
    st.markdown("### Quick Overview")
    st.markdown(
        f"""
        <div class="glass-card">
        Total detections logged: <b>{db.total_count()}</b><br>
        Most frequent emotion: <b>{db.most_frequent_emotion() or '—'}</b><br>
        Average confidence: <b>{db.average_confidence() * 100:.1f}%</b><br>
        Songs available: <b>{total_songs}</b> across {len(config.MOOD_FOLDER_DESCRIPTIONS)} mood folders
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "Head to **📷 Live Detection** in the sidebar to start the webcam "
        "and begin real-time emotion-based music recommendation."
    )

with rcol:
    st.markdown("### Emotion → Music Map")
    for emotion, mood in config.EMOTION_MUSIC_MAP.items():
        action = f"→ plays `{mood}`" if mood else "→ no auto-play"
        st.markdown(f"**{emotion}** {action}")