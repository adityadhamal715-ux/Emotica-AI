"""
utils.py
========
Small, dependency-light helpers shared across pages: FPS measurement,
CSS injection for the glassmorphism theme, and misc formatting helpers.
"""

from __future__ import annotations

import time
from collections import deque

import streamlit as st

import config


class FPSCounter:
    """Rolling-window FPS estimator (smoother than instantaneous 1/dt)."""

    def __init__(self, window: int = 30) -> None:
        self._timestamps: deque[float] = deque(maxlen=window)

    def tick(self) -> float:
        now = time.perf_counter()
        self._timestamps.append(now)
        if len(self._timestamps) < 2:
            return 0.0
        span = self._timestamps[-1] - self._timestamps[0]
        if span <= 0:
            return 0.0
        return (len(self._timestamps) - 1) / span


def inject_global_css() -> None:
    """Injects the dark, glassmorphism theme used across every page."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: radial-gradient(circle at 20% 0%, #101a33 0%, {config.COLOR_BG} 55%);
            color: {config.COLOR_TEXT};
        }}

        section[data-testid="stSidebar"] {{
            background: {config.COLOR_BG_SECONDARY};
            border-right: 1px solid {config.COLOR_GLASS_BORDER};
        }}

        h1, h2, h3, h4 {{
            font-family: 'Segoe UI', 'Inter', sans-serif;
            letter-spacing: 0.3px;
        }}

        .glass-card {{
            background: {config.COLOR_GLASS};
            border: 1px solid {config.COLOR_GLASS_BORDER};
            border-radius: 16px;
            padding: 1.1rem 1.4rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 24px rgba(0,0,0,0.25);
            margin-bottom: 0.9rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(0, 229, 255, 0.10);
        }}

        .metric-label {{
            color: {config.COLOR_TEXT_MUTED};
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.25rem;
        }}
        .metric-value {{
            font-size: 1.65rem;
            font-weight: 700;
            color: {config.COLOR_TEXT};
        }}

        .status-dot {{
            display: inline-block;
            width: 9px; height: 9px;
            border-radius: 50%;
            margin-right: 6px;
        }}
        .dot-online {{ background: {config.COLOR_SUCCESS}; box-shadow: 0 0 8px {config.COLOR_SUCCESS}; }}
        .dot-offline {{ background: {config.COLOR_DANGER}; box-shadow: 0 0 8px {config.COLOR_DANGER}; }}
        .dot-idle {{ background: {config.COLOR_WARNING}; box-shadow: 0 0 8px {config.COLOR_WARNING}; }}

        .stButton > button {{
            border-radius: 10px;
            border: 1px solid {config.COLOR_GLASS_BORDER};
            background: linear-gradient(135deg, {config.COLOR_ACCENT_SECONDARY}, {config.COLOR_ACCENT});
            color: #06101f;
            font-weight: 600;
            padding: 0.5rem 1.1rem;
            transition: filter 0.15s ease;
        }}
        .stButton > button:hover {{ filter: brightness(1.12); }}

        .app-header {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.4rem;
        }}
        .app-title {{
            font-size: 1.9rem;
            font-weight: 800;
            background: linear-gradient(90deg, {config.COLOR_ACCENT}, {config.COLOR_ACCENT_SECONDARY});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .app-tagline {{
            color: {config.COLOR_TEXT_MUTED};
            font-size: 0.95rem;
            margin-top: -0.6rem;
        }}

        div[data-testid="stMetric"] {{
            background: {config.COLOR_GLASS};
            border: 1px solid {config.COLOR_GLASS_BORDER};
            border-radius: 14px;
            padding: 0.8rem 1rem;
        }}

        /* ---- Redesigned Live Detection page ---- */
        .st-key-start_btn_wrap .stButton > button {{
            background: linear-gradient(135deg, #00c853, #00e676);
            color: #06170c;
        }}
        .st-key-stop_btn_wrap .stButton > button {{
            background: linear-gradient(135deg, #d32f2f, #ff5252);
            color: #200606;
        }}
        .st-key-pause_btn_wrap .stButton > button {{
            background: linear-gradient(135deg, {config.COLOR_ACCENT_SECONDARY}, {config.COLOR_ACCENT});
            border-radius: 50%;
            width: 46px; height: 46px;
            padding: 0;
        }}

        .clock-badge {{
            background: {config.COLOR_GLASS};
            border: 1px solid {config.COLOR_GLASS_BORDER};
            border-radius: 12px;
            padding: 0.5rem 1rem;
            text-align: center;
            font-weight: 700;
            color: {config.COLOR_ACCENT};
        }}
        .clock-badge .clock-date {{
            color: {config.COLOR_TEXT_MUTED};
            font-size: 0.72rem;
            font-weight: 500;
        }}

        .emotion-hero {{
            background: {config.COLOR_GLASS};
            border: 1px solid {config.COLOR_GLASS_BORDER};
            border-radius: 18px;
            padding: 1.1rem;
            text-align: center;
        }}
        .emotion-hero-title {{
            font-size: 0.85rem;
            color: {config.COLOR_TEXT_MUTED};
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.6rem;
        }}
        .emotion-hero-emoji {{
            font-size: 2.6rem;
            display: block;
            filter: drop-shadow(0 0 12px currentColor);
        }}
        .emotion-hero-label {{
            font-size: 1.5rem;
            font-weight: 800;
            margin-top: 0.2rem;
        }}
        .emotion-hero-sub {{
            color: {config.COLOR_TEXT_MUTED};
            font-size: 0.85rem;
        }}

        .waveform {{
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 3px;
            height: 26px;
            margin-top: 0.6rem;
        }}
        .waveform span {{
            display: inline-block;
            width: 3px;
            background: {config.COLOR_SUCCESS};
            border-radius: 2px;
            animation: waveform-bounce 1.1s ease-in-out infinite;
        }}
        @keyframes waveform-bounce {{
            0%, 100% {{ height: 20%; }}
            50% {{ height: 100%; }}
        }}

        .now-playing-card {{
            background: {config.COLOR_GLASS};
            border: 1px solid {config.COLOR_GLASS_BORDER};
            border-radius: 18px;
            padding: 1rem 1.1rem;
        }}
        .now-playing-title {{
            font-size: 0.85rem;
            color: {config.COLOR_TEXT_MUTED};
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        .now-playing-song {{
            font-weight: 700;
            font-size: 1.05rem;
        }}
        .now-playing-mood {{
            color: {config.COLOR_TEXT_MUTED};
            font-size: 0.85rem;
        }}
        .now-playing-time {{
            display: flex;
            justify-content: space-between;
            color: {config.COLOR_TEXT_MUTED};
            font-size: 0.75rem;
            margin-top: 0.3rem;
        }}
        .progress-track {{
            background: rgba(255,255,255,0.08);
            border-radius: 6px;
            height: 5px;
            width: 100%;
            overflow: hidden;
            margin-top: 0.3rem;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, {config.COLOR_ACCENT_SECONDARY}, {config.COLOR_ACCENT});
            height: 100%;
        }}

        .quick-stats-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.35rem 0;
            border-bottom: 1px solid {config.COLOR_GLASS_BORDER};
            font-size: 0.88rem;
        }}
        .quick-stats-row:last-child {{ border-bottom: none; }}
        .quick-stats-label {{ color: {config.COLOR_TEXT_MUTED}; }}
        .quick-stats-value {{ font-weight: 700; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        f"""
        <div class="app-header">
            <span style="font-size:2rem;">🎧</span>
            <span class="app-title">{config.APP_NAME}</span>
        </div>
        <div class="app-tagline">{config.APP_TAGLINE}</div>
        <hr style="border-color:{config.COLOR_GLASS_BORDER}; margin-top:0.6rem;">
        """,
        unsafe_allow_html=True,
    )


def status_badge(label: str, state: str) -> str:
    """state: 'online' | 'offline' | 'idle'"""
    dot_class = {"online": "dot-online", "offline": "dot-offline", "idle": "dot-idle"}.get(
        state, "dot-idle"
    )
    return f'<span class="status-dot {dot_class}"></span>{label}'


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


EMOTION_EMOJI: dict[str, str] = {
    "Happy": "😄",
    "Sad": "😢",
    "Angry": "😠",
    "Fear": "😨",
    "Surprise": "😲",
    "Disgust": "🤢",
    "Neutral": "😐",
    "Uncertain": "🤔",
}

EMOTION_SUBTITLE: dict[str, str] = {
    "Happy": "You look great!",
    "Sad": "Here's something uplifting.",
    "Angry": "Let's calm things down.",
    "Fear": "Take a breath — relaxing.",
    "Surprise": "Ooh, exciting!",
    "Disgust": "Shifting the mood.",
    "Neutral": "Just observing.",
    "Uncertain": "Still figuring it out...",
}


def format_mmss(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def waveform_html(bar_count: int = 18) -> str:
    import random as _random

    bars = []
    for i in range(bar_count):
        height = _random.randint(30, 100)
        delay = round(_random.uniform(0, 1.0), 2)
        bars.append(f'<span style="height:{height}%; animation-delay:{delay}s;"></span>')
    return f'<div class="waveform">{"".join(bars)}</div>'


def clock_badge_html(time_str: str, date_str: str) -> str:
    return (
        f'<div class="clock-badge">🕐 {time_str}'
        f'<div class="clock-date">{date_str}</div></div>'
    )


def emotion_hero_html(emotion: str | None) -> str:
    label = emotion or "—"
    emoji = EMOTION_EMOJI.get(label, "🙂")
    subtitle = EMOTION_SUBTITLE.get(label, "Waiting for a face...")
    color = config.EMOTION_COLORS.get(label, config.COLOR_TEXT)
    return f"""
    <div class="emotion-hero" style="color:{color};">
        <div class="emotion-hero-title" style="color:{config.COLOR_TEXT_MUTED};">Current Emotion</div>
        <span class="emotion-hero-emoji">{emoji}</span>
        <div class="emotion-hero-label" style="color:{color};">{label}</div>
        <div class="emotion-hero-sub">{subtitle}</div>
        {waveform_html() if emotion else ""}
    </div>
    """


def now_playing_html(
    song_name: str | None,
    mood: str | None,
    is_playing: bool,
    elapsed: float,
    duration: float | None,
) -> str:
    if song_name is None:
        return """
        <div class="now-playing-card">
            <div class="now-playing-title">🎵 Now Playing</div>
            <div class="now-playing-mood">Nothing playing right now.</div>
        </div>
        """

    status = "Now Playing" if is_playing else "Paused"
    total = duration if duration else max(elapsed, 1.0)
    pct = min(100.0, (elapsed / total) * 100.0) if total else 0.0
    total_label = format_mmss(duration) if duration else "--:--"
    mood_label = f"{mood.capitalize()} Playlist" if mood else ""

    return f"""
    <div class="now-playing-card">
        <div class="now-playing-title">🎵 Now Playing</div>
        <div class="now-playing-song">{song_name}</div>
        <div class="now-playing-mood">{mood_label} · ♪ {status}</div>
        <div class="progress-track"><div class="progress-fill" style="width:{pct:.1f}%;"></div></div>
        <div class="now-playing-time"><span>{format_mmss(elapsed)}</span><span>{total_label}</span></div>
    </div>
    """