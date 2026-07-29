"""
music_player.py
================
Wraps `pygame.mixer` to play mood-appropriate songs. Handles:
  * auto-discovering mp3/wav/ogg files under songs/<mood>/ (no hard-coded filenames)
  * random selection without repeating the same track twice in a row
  * switching songs only when the *effective mood* changes (so a jittery
    emotion prediction doesn't restart the song every frame)
  * volume control and auto-play on/off
"""

from __future__ import annotations

import logging
import random
import time
from pathlib import Path

import pygame

import config

logger = logging.getLogger(__name__)


class MusicPlayer:
    def __init__(self) -> None:
        self._initialized = False
        self._current_mood: str | None = None
        self._current_song: Path | None = None
        self._last_song_by_mood: dict[str, Path] = {}
        self._volume: float = 0.6
        self._play_started_at: float | None = None
        self._paused_at: float | None = None
        self._paused_elapsed: float = 0.0
        self._init_mixer()

    def _init_mixer(self) -> None:
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self._volume)
            self._initialized = True
        except Exception:
            logger.exception("Failed to initialize pygame mixer (no audio device?)")
            self._initialized = False

    @property
    def is_available(self) -> bool:
        return self._initialized

    # ------------------------------------------------------------------ #
    def songs_for_mood(self, mood: str) -> list[Path]:
        folder = config.SONGS_DIR / mood
        if not folder.exists():
            return []
        return sorted(
            p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in config.SUPPORTED_AUDIO_EXT
        )

    def all_songs(self) -> dict[str, list[Path]]:
        return {mood: self.songs_for_mood(mood) for mood in config.MOOD_FOLDER_DESCRIPTIONS}

    def _pick_song(self, mood: str) -> Path | None:
        candidates = self.songs_for_mood(mood)
        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]

        last = self._last_song_by_mood.get(mood)
        pool = [c for c in candidates if c != last] or candidates
        return random.choice(pool)

    # ------------------------------------------------------------------ #
    def play_for_emotion(self, emotion: str, force: bool = False) -> str | None:
        """
        Plays a song for the mood mapped to `emotion`. Returns the song
        filename played (or None). Does nothing if the mood hasn't
        changed since the last call (unless force=True), and does
        nothing for emotions mapped to None (e.g. Neutral).
        """
        mood = config.EMOTION_MUSIC_MAP.get(emotion)

        if mood is None:
            self.stop()
            self._current_mood = None
            return None

        if mood == self._current_mood and not force:
            return self._current_song.name if self._current_song else None

        if not self._initialized:
            return None

        song = self._pick_song(mood)
        if song is None:
            logger.info("No songs found for mood '%s'", mood)
            return None

        try:
            pygame.mixer.music.load(str(song))
            pygame.mixer.music.set_volume(self._volume)
            pygame.mixer.music.play()
            self._current_mood = mood
            self._current_song = song
            self._last_song_by_mood[mood] = song
            self._play_started_at = time.time()
            self._paused_at = None
            self._paused_elapsed = 0.0
            return song.name
        except Exception:
            logger.exception("Failed to play song %s", song)
            return None

    def stop(self) -> None:
        if self._initialized:
            pygame.mixer.music.stop()
        self._current_song = None
        self._play_started_at = None
        self._paused_at = None
        self._paused_elapsed = 0.0

    def toggle_pause(self) -> bool:
        """Pauses if playing, resumes if paused. Returns the new paused state."""
        if not self._initialized or self._current_song is None:
            return False
        if self._paused_at is None:
            pygame.mixer.music.pause()
            self._paused_at = time.time()
            return True
        else:
            pygame.mixer.music.unpause()
            self._paused_elapsed += time.time() - self._paused_at
            self._paused_at = None
            return False

    @property
    def is_paused(self) -> bool:
        return self._paused_at is not None

    def elapsed_seconds(self) -> float:
        """Best-effort playback position, based on wall-clock time since play()."""
        if self._play_started_at is None:
            return 0.0
        now = self._paused_at or time.time()
        return max(0.0, now - self._play_started_at - self._paused_elapsed)

    def duration_seconds(self) -> float | None:
        """Best-effort total song length via mutagen, if installed. None if unknown."""
        if self._current_song is None:
            return None
        try:
            from mutagen import File as MutagenFile

            audio = MutagenFile(str(self._current_song))
            if audio is not None and audio.info is not None:
                return float(audio.info.length)
        except Exception:
            pass
        return None

    def set_volume(self, volume_0_1: float) -> None:
        self._volume = max(0.0, min(1.0, volume_0_1))
        if self._initialized:
            pygame.mixer.music.set_volume(self._volume)

    @property
    def current_song_name(self) -> str | None:
        return self._current_song.name if self._current_song else None

    @property
    def is_playing(self) -> bool:
        return self._initialized and pygame.mixer.music.get_busy()