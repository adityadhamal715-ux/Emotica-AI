"""
config.py
=========
Central configuration for Emotica AI. All tunable constants, file paths,
and static mappings live here so the rest of the codebase never hard-codes
values that might change between environments.
"""

from __future__ import annotations

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# Base paths
# --------------------------------------------------------------------------- #
BASE_DIR: Path = Path(__file__).resolve().parent
ASSETS_DIR: Path = BASE_DIR / "assets"
SONGS_DIR: Path = BASE_DIR / "songs"
MODELS_DIR: Path = BASE_DIR / "models"
DATA_DIR: Path = BASE_DIR / "data"
DB_PATH: Path = BASE_DIR / "emotica.db"

MODEL_PATH: Path = MODELS_DIR / "emotion_model.h5"
LOGO_PATH: Path = ASSETS_DIR / "logo.png"
CUSTOM_DATA_DIR: Path = DATA_DIR / "custom"

for _dir in (ASSETS_DIR, SONGS_DIR, MODELS_DIR, DATA_DIR, CUSTOM_DATA_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
# Model / detection constants
# --------------------------------------------------------------------------- #
FACE_IMG_SIZE: int = 48
TRANSFER_IMG_SIZE: int = 96  # input size for the MobileNetV2 transfer-learning model
# Reduced to 4 classes for the custom, self-collected dataset (was the full
# 7-class FER2013 set). Order matters — it defines the CNN's output index,
# and collect_faces.py / train_custom_model.py must use these exact,
# identically-spelled folder names under data/custom/.
EMOTION_LABELS: list[str] = ["Angry", "Happy", "Neutral", "Sad"]

# Frame is only run through the CNN every N captured frames. Face
# *detection* still runs every frame so the bounding box stays smooth;
# only the (heavier) emotion *classification* is throttled.
INFERENCE_EVERY_N_FRAMES: int = 3

MIN_FACE_DETECTION_CONFIDENCE: float = 0.6
DEFAULT_CONFIDENCE_THRESHOLD: float = 0.55  # below this, "Uncertain"

# --------------------------------------------------------------------------- #
# Camera defaults (overridable from the Settings page, stored in session)
# --------------------------------------------------------------------------- #
DEFAULT_CAMERA_INDEX: int = 0
DEFAULT_CAMERA_WIDTH: int = 640
DEFAULT_CAMERA_HEIGHT: int = 480
DEFAULT_TARGET_FPS: int = 30

CAMERA_RESOLUTIONS: dict[str, tuple[int, int]] = {
    "480p (640x480)": (640, 480),
    "720p (1280x720)": (1280, 720),
    "1080p (1920x1080)": (1920, 1080),
}

# --------------------------------------------------------------------------- #
# Emotion -> music-mood mapping (4-emotion custom model)
# --------------------------------------------------------------------------- #
# Each emotion maps to a *mood folder* under SONGS_DIR. `None` means
# "do not auto-play anything" (used for Neutral, per project spec).
EMOTION_MUSIC_MAP: dict[str, str | None] = {
    "Happy": "happy",
    "Sad": "motivation",
    "Angry": "calm",
    "Neutral": None,
}

MOOD_FOLDER_DESCRIPTIONS: dict[str, str] = {
    "happy": "Upbeat / feel-good tracks played when Happy is detected.",
    "motivation": "Uplifting tracks played when Sad is detected.",
    "calm": "Calm / relaxing tracks played when Angry is detected.",
}

SUPPORTED_AUDIO_EXT: tuple[str, ...] = (".mp3", ".wav", ".ogg")

# --------------------------------------------------------------------------- #
# UI / theme constants
# --------------------------------------------------------------------------- #
APP_NAME: str = "Emotica AI"
APP_TAGLINE: str = "Real-Time Emotion Detection & Smart Music Recommendation"
APP_VERSION: str = "1.0.0"

COLOR_BG: str = "#0a0e1a"
COLOR_BG_SECONDARY: str = "#0f1526"
COLOR_ACCENT: str = "#00e5ff"
COLOR_ACCENT_SECONDARY: str = "#7c4dff"
COLOR_GLASS: str = "rgba(255, 255, 255, 0.05)"
COLOR_GLASS_BORDER: str = "rgba(255, 255, 255, 0.10)"
COLOR_TEXT: str = "#e8ecf5"
COLOR_TEXT_MUTED: str = "#8a94a8"
COLOR_SUCCESS: str = "#00e676"
COLOR_WARNING: str = "#ffb300"
COLOR_DANGER: str = "#ff5252"

EMOTION_COLORS: dict[str, str] = {
    "Happy": "#ffd54f",
    "Sad": "#4fc3f7",
    "Angry": "#ff5252",
    "Neutral": "#b0bec5",
}