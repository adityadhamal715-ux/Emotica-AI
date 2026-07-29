"""
emotion_model.py
================
Defines the FER2013 CNN architecture and exposes a cached loader plus a
`predict_emotion()` helper used by the live-detection loop.

IMPORTANT — read this before running the app:
The model file (models/emotion_model.h5) is a *trained artifact*, not
source code, and therefore cannot be shipped as part of this codebase —
exactly like the mp3 files under songs/, it has to be produced/added by
you. Run `train_model.py` once (see README.md) against the FER2013
dataset to generate it. This module will detect a missing model and
surface a clear, non-crashing warning in the UI instead of failing.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import streamlit as st

import config

logger = logging.getLogger(__name__)


def build_emotion_cnn(num_classes: int = len(config.EMOTION_LABELS)):
    """
    Builds the CNN architecture used for FER2013 emotion classification.
    Input: 48x48 grayscale face crops. ~1.2M parameters — light enough
    for real-time CPU inference. Intended for large datasets (FER2013's
    ~28k training images) — for small self-collected datasets, use
    build_emotion_cnn_light() instead, which is far less prone to
    memorizing a few hundred images instead of learning real features.
    """
    from tensorflow.keras import layers, models, regularizers

    reg = regularizers.l2(1e-4)
    model = models.Sequential(
        [
            layers.Input(shape=(config.FACE_IMG_SIZE, config.FACE_IMG_SIZE, 1)),

            layers.Conv2D(32, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.Conv2D(32, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            layers.Dropout(0.25),

            layers.Conv2D(64, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.Conv2D(64, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            layers.Dropout(0.25),

            layers.Conv2D(128, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.Conv2D(128, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            layers.Dropout(0.3),

            layers.Flatten(),
            layers.Dense(256, activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(num_classes, activation="softmax"),
        ],
        name="emotica_fer_cnn",
    )
    return model


def build_emotion_cnn_light(num_classes: int = len(config.EMOTION_LABELS)):
    """
    A much smaller, more heavily-regularized CNN (~140k params, vs ~1.47M
    for build_emotion_cnn) intended for small, self-collected datasets
    (hundreds, not tens-of-thousands, of images). The full-size model
    has enough capacity to memorize a few hundred near-duplicate webcam
    frames outright rather than learning generalizable expression
    features — this smaller model, combined with strong dropout/L2 and
    heavy augmentation, is far less prone to that failure mode.
    """
    from tensorflow.keras import layers, models, regularizers

    reg = regularizers.l2(5e-4)
    model = models.Sequential(
        [
            layers.Input(shape=(config.FACE_IMG_SIZE, config.FACE_IMG_SIZE, 1)),

            layers.Conv2D(16, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            layers.Dropout(0.35),

            layers.Conv2D(32, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            layers.Dropout(0.35),

            layers.Conv2D(64, 3, padding="same", activation="relu", kernel_regularizer=reg),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            layers.Dropout(0.4),

            layers.GlobalAveragePooling2D(),
            layers.Dense(64, activation="relu", kernel_regularizer=reg),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ],
        name="emotica_custom_cnn_light",
    )
    return model


def build_emotion_cnn_transfer(num_classes: int = len(config.EMOTION_LABELS), fine_tune_last_n: int = 0):
    """
    Transfer-learning architecture: a MobileNetV2 backbone pretrained on
    ImageNet (millions of natural images), with a small classification
    head trained on our own face data. For small, self-collected
    datasets (hundreds to low-thousands of images) this generalizes far
    better than training a CNN from scratch, because the backbone
    already knows general-purpose visual features (edges, textures,
    shapes) — it only has to learn how *our* classes map onto those
    features, rather than learning to see from zero.

    fine_tune_last_n: if > 0, unfreezes the last N layers of the
    backbone for a low-learning-rate fine-tuning phase (see
    train_transfer_model.py) after the head has already converged.
    """
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import MobileNetV2

    base = MobileNetV2(
        input_shape=(config.TRANSFER_IMG_SIZE, config.TRANSFER_IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
        alpha=0.35,  # smallest/fastest MobileNetV2 variant — still CPU-real-time
    )
    base.trainable = fine_tune_last_n > 0
    if fine_tune_last_n > 0:
        for layer in base.layers[:-fine_tune_last_n]:
            layer.trainable = False

    model = models.Sequential(
        [
            base,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.3),
            layers.Dense(64, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation="softmax"),
        ],
        name="emotica_transfer_mobilenetv2",
    )
    return model, base


class EmotionModel:
    """
    Wraps the loaded Keras model and exposes a simple predict() API.
    Auto-detects, from the loaded model's own input shape, whether it's
    the legacy grayscale-48 model or the newer color-96 transfer model
    — so camera.py / the Live Detection page can adapt preprocessing
    without needing to be told which model type is on disk.
    """

    def __init__(self, model) -> None:
        self._model = model
        shape = model.input_shape  # e.g. (None, 48, 48, 1) or (None, 96, 96, 3)
        self.input_size: int = shape[1]
        self.is_color: bool = shape[3] == 3

    def predict(self, face_image: np.ndarray) -> tuple[str, float, np.ndarray]:
        """
        face_image: for grayscale models, a (size, size) uint8/float
        array; for color models, a (size, size, 3) RGB uint8/float
        array. Use self.is_color / self.input_size to prepare the
        right crop (see camera.py's crop_face_for_model / crop_face_color).
        """
        if self.is_color:
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

            x = face_image.astype("float32")
            x = preprocess_input(x)
            x = x.reshape(1, self.input_size, self.input_size, 3)
        else:
            x = face_image.astype("float32") / 255.0
            x = x.reshape(1, self.input_size, self.input_size, 1)

        probs = self._model.predict(x, verbose=0)[0]
        idx = int(np.argmax(probs))
        return config.EMOTION_LABELS[idx], float(probs[idx]), probs


@st.cache_resource(show_spinner="Loading emotion recognition model...")
def load_emotion_model(model_path: str = str(config.MODEL_PATH)) -> EmotionModel | None:
    """
    Loads the trained .h5 model once per Streamlit server process
    (cached via st.cache_resource so every rerun reuses the same
    in-memory model instead of reloading from disk).

    Returns None if the model file doesn't exist yet — callers must
    handle that gracefully rather than crashing the app.
    """
    path = Path(model_path)
    if not path.exists():
        logger.warning("Emotion model not found at %s", path)
        return None

    try:
        from tensorflow.keras.models import load_model

        keras_model = load_model(str(path), compile=False)
        return EmotionModel(keras_model)
    except Exception:
        logger.exception("Failed to load emotion model from %s", path)
        return None


def model_is_available(model_path: str = str(config.MODEL_PATH)) -> bool:
    return Path(model_path).exists()