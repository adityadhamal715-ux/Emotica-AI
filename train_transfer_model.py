"""
train_transfer_model.py
========================
Trains the Emotica AI 4-emotion model using transfer learning from a
MobileNetV2 backbone pretrained on ImageNet, on your own collected
color dataset (data/custom/<Emotion>/*.png, produced by the updated
collect_faces.py). This generalizes far better than training a CNN
from scratch on a few hundred/thousand self-collected images, because
the backbone already knows general visual features and only has to
learn how our 4 classes map onto them.

Two-phase training:
  Phase 1 (head-only):  backbone frozen, only the new classification
                          head is trained — fast, stabilizes quickly.
  Phase 2 (fine-tune):   the last few backbone layers are unfrozen and
                          trained at a very low learning rate, letting
                          the model adapt its higher-level features
                          specifically to faces/expressions.

Usage
-----
    python collect_faces.py           # collect color images first
    python train_transfer_model.py    # then train

On success, models/emotion_model.h5 is overwritten — the Streamlit app
picks up whichever model is there automatically (it auto-detects
color-96 vs. grayscale-48 from the file itself).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict

import cv2
import numpy as np

import config
from emotion_model import build_emotion_cnn_transfer

MIN_RECOMMENDED_PER_CLASS = 100
BURST_PATTERN = re.compile(r"_burst(\d+)_")


def load_custom_dataset(val_split: float, seed: int = 42):
    """Same burst-aware, leakage-free split as train_custom_model.py — see
    that file's docstring for why this matters."""
    print(f"Loading custom dataset from {config.CUSTOM_DATA_DIR} ...\n")

    rng = np.random.default_rng(seed)
    X_train_parts, y_train_parts, X_val_parts, y_val_parts = [], [], [], []

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
            img_bgr = cv2.imread(str(f), cv2.IMREAD_COLOR)
            if img_bgr is None:
                continue
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            if img_rgb.shape[:2] != (config.TRANSFER_IMG_SIZE, config.TRANSFER_IMG_SIZE):
                img_rgb = cv2.resize(img_rgb, (config.TRANSFER_IMG_SIZE, config.TRANSFER_IMG_SIZE))
            by_burst[burst_key].append(img_rgb)

        burst_keys = list(by_burst.keys())
        rng.shuffle(burst_keys)
        if len(burst_keys) <= 1:
            n_val_bursts = 0
        else:
            n_val_bursts = max(1, round(len(burst_keys) * val_split))
        val_keys = set(burst_keys[:n_val_bursts])

        for key, imgs in by_burst.items():
            target_X = X_val_parts if key in val_keys else X_train_parts
            target_y = y_val_parts if key in val_keys else y_train_parts
            for img in imgs:
                target_X.append(img)
                target_y.append(idx)

    if not X_train_parts:
        sys.exit(
            "[Emotica AI] No images found under data/custom/. "
            "Run `python collect_faces.py` first to build your dataset."
        )

    size = config.TRANSFER_IMG_SIZE
    X_train = np.stack(X_train_parts).reshape(-1, size, size, 3).astype("float32")
    y_train = np.array(y_train_parts, dtype="int64")
    X_val = (
        np.stack(X_val_parts).reshape(-1, size, size, 3).astype("float32")
        if X_val_parts
        else np.empty((0, size, size, 3), dtype="float32")
    )
    y_val = np.array(y_val_parts, dtype="int64")

    print(f"Total images: {len(X_train) + len(X_val)}  |  Train: {len(X_train)}  |  Validation: {len(X_val)}\n")
    return X_train, y_train, X_val, y_val


def build_augmenter():
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    return ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.12,
        height_shift_range=0.12,
        zoom_range=0.15,
        brightness_range=(0.8, 1.2),
        horizontal_flip=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Emotica AI via MobileNetV2 transfer learning.")
    parser.add_argument("--head-epochs", type=int, default=25, help="Phase 1: head-only training epochs")
    parser.add_argument("--finetune-epochs", type=int, default=25, help="Phase 2: fine-tuning epochs")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--val-split", type=float, default=0.15)
    parser.add_argument("--finetune-layers", type=int, default=30, help="Backbone layers to unfreeze in phase 2")
    args = parser.parse_args()

    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.utils import to_categorical

    X_train, y_train, X_val, y_val = load_custom_dataset(args.val_split)
    num_classes = len(config.EMOTION_LABELS)
    y_train_cat = to_categorical(y_train, num_classes)
    y_val_cat = to_categorical(y_val, num_classes)

    # MobileNetV2 preprocessing (scales to [-1, 1]) — must match
    # emotion_model.py's EmotionModel.predict() exactly for live inference.
    X_val_prep = preprocess_input(X_val.copy())

    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    augmenter = build_augmenter()
    augmenter.fit(X_train)

    def augmented_preprocessed_flow():
        for batch_x, batch_y in augmenter.flow(X_train, y_train_cat, batch_size=args.batch_size):
            yield preprocess_input(batch_x), batch_y

    # ---------------- Phase 1: train the head only ---------------- #
    print("=" * 60)
    print("PHASE 1: training classification head (backbone frozen)")
    print("=" * 60)
    model, base = build_emotion_cnn_transfer(num_classes, fine_tune_last_n=0)
    model.compile(optimizer=Adam(learning_rate=1e-3), loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()

    callbacks_phase1 = [
        EarlyStopping(monitor="val_accuracy", patience=8, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=4, min_lr=1e-6),
    ]
    steps_per_epoch = max(1, len(X_train) // args.batch_size)
    model.fit(
        augmented_preprocessed_flow(),
        steps_per_epoch=steps_per_epoch,
        validation_data=(X_val_prep, y_val_cat),
        epochs=args.head_epochs,
        callbacks=callbacks_phase1,
        verbose=1,
    )

    # ---------------- Phase 2: fine-tune the backbone -------------- #
    print("\n" + "=" * 60)
    print(f"PHASE 2: fine-tuning last {args.finetune_layers} backbone layers")
    print("=" * 60)
    base.trainable = True
    for layer in base.layers[: -args.finetune_layers]:
        layer.trainable = False

    model.compile(optimizer=Adam(learning_rate=1e-5), loss="categorical_crossentropy", metrics=["accuracy"])
    callbacks_phase2 = [
        EarlyStopping(monitor="val_accuracy", patience=8, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=4, min_lr=1e-7),
        ModelCheckpoint(str(config.MODEL_PATH), monitor="val_accuracy", save_best_only=True, verbose=1),
    ]
    model.fit(
        augmented_preprocessed_flow(),
        steps_per_epoch=steps_per_epoch,
        validation_data=(X_val_prep, y_val_cat),
        epochs=args.finetune_epochs,
        callbacks=callbacks_phase2,
        verbose=1,
    )

    val_loss, val_acc = model.evaluate(X_val_prep, y_val_cat, verbose=0)
    print(f"\nFinal validation accuracy: {val_acc * 100:.2f}%  (loss: {val_loss:.4f})")
    print(f"Model saved to: {config.MODEL_PATH}")
    print(f"Classes (in order): {config.EMOTION_LABELS}")


if __name__ == "__main__":
    main()