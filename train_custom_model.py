"""
train_custom_model.py
======================
Trains the Emotica AI CNN from scratch on your own collected dataset
(data/custom/<Emotion>/*.png, produced by collect_faces.py) instead of
FER2013. Only the 4 emotions in config.EMOTION_LABELS are used
(Angry, Happy, Neutral, Sad).

Usage
-----
    python collect_faces.py          # collect images first
    python train_custom_model.py     # then train

On success, the trained model is written to models/emotion_model.h5,
same as train_model.py — the Streamlit app doesn't care which script
produced it.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict

import cv2
import numpy as np

import config
from emotion_model import build_emotion_cnn_light

MIN_RECOMMENDED_PER_CLASS = 100
BURST_PATTERN = re.compile(r"_burst(\d+)_")


def load_custom_dataset(val_split: float, seed: int = 42):
    """
    Loads images grouped by capture "burst" (see collect_faces.py) and
    splits train/validation by whole bursts rather than individual
    frames. Frames within one 3-second burst are near-duplicates of
    each other (same lighting, same instant) — splitting at the frame
    level lets near-identical images leak into both train and
    validation, which is what produced the earlier fake "100% accuracy"
    that didn't hold up on live video. Splitting by burst instead means
    validation only ever sees genuinely unseen moments.
    """
    print(f"Loading custom dataset from {config.CUSTOM_DATA_DIR} ...\n")

    rng = np.random.default_rng(seed)
    X_train_parts, y_train_parts, X_val_parts, y_val_parts = [], [], [], []
    any_ungrouped = False

    for idx, emotion in enumerate(config.EMOTION_LABELS):
        folder = config.CUSTOM_DATA_DIR / emotion
        files = sorted(folder.glob("*.png")) if folder.exists() else []
        print(f"  {emotion:10s}: {len(files)} images")

        if len(files) < MIN_RECOMMENDED_PER_CLASS:
            print(
                f"    ⚠ Fewer than {MIN_RECOMMENDED_PER_CLASS} images for '{emotion}' — "
                "the model will likely be weak for this class. Run collect_faces.py more."
            )

        by_burst: dict[str, list] = defaultdict(list)
        for f in files:
            match = BURST_PATTERN.search(f.name)
            burst_key = match.group(1) if match else f"_ungrouped_{f.name}"
            if not match:
                any_ungrouped = True
            img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            if img.shape != (config.FACE_IMG_SIZE, config.FACE_IMG_SIZE):
                img = cv2.resize(img, (config.FACE_IMG_SIZE, config.FACE_IMG_SIZE))
            by_burst[burst_key].append(img)

        burst_keys = list(by_burst.keys())
        rng.shuffle(burst_keys)
        if len(burst_keys) <= 1:
            n_val_bursts = 0  # too few bursts to hold any out — all goes to train
        else:
            n_val_bursts = max(1, round(len(burst_keys) * val_split))
        val_keys = set(burst_keys[:n_val_bursts])

        for key, imgs in by_burst.items():
            target_X = X_val_parts if key in val_keys else X_train_parts
            target_y = y_val_parts if key in val_keys else y_train_parts
            for img in imgs:
                target_X.append(img)
                target_y.append(idx)

    if any_ungrouped:
        print(
            "\n⚠ Some images have old filenames without a burst id (from before this "
            "update) — they were treated as their own single-image group. For best "
            "results, delete data/custom/ and re-run collect_faces.py to regenerate "
            "burst-tagged filenames.\n"
        )

    if not X_train_parts:
        sys.exit(
            "[Emotica AI] No images found under data/custom/. "
            "Run `python collect_faces.py` first to build your dataset."
        )

    X_train = np.stack(X_train_parts).reshape(-1, config.FACE_IMG_SIZE, config.FACE_IMG_SIZE, 1).astype("float32")
    y_train = np.array(y_train_parts, dtype="int64")
    X_val = (
        np.stack(X_val_parts).reshape(-1, config.FACE_IMG_SIZE, config.FACE_IMG_SIZE, 1).astype("float32")
        if X_val_parts
        else np.empty((0, config.FACE_IMG_SIZE, config.FACE_IMG_SIZE, 1), dtype="float32")
    )
    y_val = np.array(y_val_parts, dtype="int64")

    print(f"Total images: {len(X_train) + len(X_val)}  |  Train: {len(X_train)}  |  Validation: {len(X_val)}\n")
    return X_train, y_train, X_val, y_val


def build_augmenter():
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    # Slightly stronger augmentation than train_model.py since a
    # self-collected dataset is typically much smaller than FER2013.
    return ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.12,
        height_shift_range=0.12,
        zoom_range=0.15,
        brightness_range=(0.8, 1.2),
        horizontal_flip=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Emotica AI on a custom 4-emotion dataset.")
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--val-split", type=float, default=0.15)
    args = parser.parse_args()

    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.utils import to_categorical

    X_train, y_train, X_val, y_val = load_custom_dataset(args.val_split)
    num_classes = len(config.EMOTION_LABELS)
    y_train_cat = to_categorical(y_train, num_classes)
    y_val_cat = to_categorical(y_val, num_classes)

    model = build_emotion_cnn_light(num_classes)
    model.compile(optimizer=Adam(learning_rate=1e-3), loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()

    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=15, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=6, min_lr=1e-6),
        ModelCheckpoint(str(config.MODEL_PATH), monitor="val_accuracy", save_best_only=True, verbose=1),
    ]

    augmenter = build_augmenter()
    augmenter.fit(X_train)

    model.fit(
        augmenter.flow(X_train, y_train_cat, batch_size=args.batch_size),
        validation_data=(X_val, y_val_cat),
        epochs=args.epochs,
        callbacks=callbacks,
        verbose=1,
    )

    val_loss, val_acc = model.evaluate(X_val, y_val_cat, verbose=0)
    print(f"\nFinal validation accuracy: {val_acc * 100:.2f}%  (loss: {val_loss:.4f})")
    print(f"Model saved to: {config.MODEL_PATH}")
    print(f"Classes (in order): {config.EMOTION_LABELS}")


if __name__ == "__main__":
    main()