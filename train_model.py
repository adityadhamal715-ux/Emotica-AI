"""
train_model.py
===============
One-time training script for the Emotica AI emotion-recognition CNN.

Usage
-----
1. Download `fer2013.csv` (the classic Kaggle FER2013 release, 35,887
   rows with columns `emotion,pixels,Usage`) and place it at:
       project/data/fer2013.csv
2. Run:
       python train_model.py
3. On success, the trained model is written to:
       project/models/emotion_model.h5
   and the Streamlit app will pick it up automatically on next launch.

This script is deliberately standalone (no Streamlit imports) so it can
run from a plain terminal, optionally on a GPU box, independent of the
web app.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import config
from emotion_model import build_emotion_cnn


def load_fer2013(csv_path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    import cv2

    if not csv_path.exists():
        sys.exit(
            f"[Emotica AI] Could not find '{csv_path}'.\n"
            "Download the FER2013 dataset (fer2013.csv) and place it there, "
            "then re-run this script. See README.md for details."
        )

    print(f"Loading dataset from {csv_path} ...")
    df = pd.read_csv(csv_path)

    def to_equalized_image(pixel_str: str) -> np.ndarray:
        img = np.array(pixel_str.split(), dtype="uint8").reshape(
            config.FACE_IMG_SIZE, config.FACE_IMG_SIZE
        )
        # Must match camera.py's crop_face_for_model() preprocessing exactly,
        # so the live webcam images and training images are normalized the
        # same way — this is what most improves real-world (vs. test-set)
        # accuracy for FER2013-based models.
        return cv2.equalizeHist(img)

    print("Applying histogram equalization (matches live-camera preprocessing)...")
    images = df["pixels"].apply(to_equalized_image)
    X = np.stack(images.values).reshape(-1, config.FACE_IMG_SIZE, config.FACE_IMG_SIZE, 1)
    y = df["emotion"].values.astype("int64")

    is_train = df["Usage"] == "Training"
    is_test = df["Usage"].isin(["PublicTest", "PrivateTest"])

    X_train, y_train = X[is_train.values], y[is_train.values]
    X_test, y_test = X[is_test.values], y[is_test.values]
    return X_train, y_train, X_test, y_test


def build_augmenter():
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    return ImageDataGenerator(
        rotation_range=12,
        width_shift_range=0.10,
        height_shift_range=0.10,
        zoom_range=0.10,
        horizontal_flip=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the Emotica AI FER2013 CNN.")
    parser.add_argument("--csv", type=str, default=str(config.DATA_DIR / "fer2013.csv"))
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()

    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.utils import to_categorical

    X_train, y_train, X_test, y_test = load_fer2013(Path(args.csv))
    num_classes = len(config.EMOTION_LABELS)
    y_train_cat = to_categorical(y_train, num_classes)
    y_test_cat = to_categorical(y_test, num_classes)

    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    model = build_emotion_cnn(num_classes)
    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.summary()

    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6),
        ModelCheckpoint(
            str(config.MODEL_PATH), monitor="val_accuracy", save_best_only=True, verbose=1
        ),
    ]

    augmenter = build_augmenter()
    augmenter.fit(X_train)

    model.fit(
        augmenter.flow(X_train, y_train_cat, batch_size=args.batch_size),
        validation_data=(X_test, y_test_cat),
        epochs=args.epochs,
        callbacks=callbacks,
        verbose=1,
    )

    test_loss, test_acc = model.evaluate(X_test, y_test_cat, verbose=0)
    print(f"\nFinal test accuracy: {test_acc * 100:.2f}%  (loss: {test_loss:.4f})")
    print(f"Best model saved to: {config.MODEL_PATH}")


if __name__ == "__main__":
    main()