# 🎧 Emotica AI

**Real-Time Emotion Detection & Smart Music Recommendation**

Emotica AI watches your webcam, detects your facial emotion in real time with a CNN, and automatically plays mood-matched music — all inside a dark, glassmorphism-themed Streamlit dashboard. Every detection is logged to SQLite and visualized on a live Plotly analytics page.

<img src="data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMTIwMCA2MjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8cmFkaWFsR3JhZGllbnQgaWQ9ImJnIiBjeD0iMjAlIiBjeT0iMCUiIHI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjMTAxYTMzIi8+CiAgICAgIDxzdG9wIG9mZnNldD0iNTUlIiBzdG9wLWNvbG9yPSIjMGEwZTFhIi8+CiAgICA8L3JhZGlhbEdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJhY2NlbnQiIHgxPSIwIiB5MT0iMCIgeDI9IjEiIHkyPSIwIj4KICAgICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iIzdjNGRmZiIvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiMwMGU1ZmYiLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgICA8ZmlsdGVyIGlkPSJnbG93IiB4PSItNTAlIiB5PSItNTAlIiB3aWR0aD0iMjAwJSIgaGVpZ2h0PSIyMDAlIj4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iNiIgcmVzdWx0PSJiIi8+CiAgICAgIDxmZU1lcmdlPjxmZU1lcmdlTm9kZSBpbj0iYiIvPjxmZU1lcmdlTm9kZSBpbj0iU291cmNlR3JhcGhpYyIvPjwvZmVNZXJnZT4KICAgIDwvZmlsdGVyPgogICAgPHN0eWxlPgogICAgICAuY2FyZCB7IGZpbGw6IHJnYmEoMjU1LDI1NSwyNTUsMC4wNSk7IHN0cm9rZTogcmdiYSgyNTUsMjU1LDI1NSwwLjEyKTsgc3Ryb2tlLXdpZHRoOiAxLjU7IHJ4OiAxNDsgfQogICAgICAudGl0bGUgeyBmaWxsOiAjZThlY2Y1OyBmb250LWZhbWlseTogJ1NlZ29lIFVJJywgc2Fucy1zZXJpZjsgZm9udC13ZWlnaHQ6IDcwMDsgZm9udC1zaXplOiAxNnB4OyB9CiAgICAgIC5zdWIgeyBmaWxsOiAjOGE5NGE4OyBmb250LWZhbWlseTogJ1NlZ29lIFVJJywgc2Fucy1zZXJpZjsgZm9udC1zaXplOiAxMnB4OyB9CiAgICAgIC5sYWJlbCB7IGZpbGw6ICMwMGU1ZmY7IGZvbnQtZmFtaWx5OiAnU2Vnb2UgVUknLCBzYW5zLXNlcmlmOyBmb250LXdlaWdodDogNzAwOyBmb250LXNpemU6IDEycHg7IGxldHRlci1zcGFjaW5nOiAxcHg7IH0KICAgICAgLmFycm93IHsgc3Ryb2tlOiB1cmwoI2FjY2VudCk7IHN0cm9rZS13aWR0aDogMi41OyBmaWxsOiBub25lOyBtYXJrZXItZW5kOiB1cmwoI2Fycm93aGVhZCk7IH0KICAgIDwvc3R5bGU+CiAgICA8bWFya2VyIGlkPSJhcnJvd2hlYWQiIG1hcmtlcldpZHRoPSI5IiBtYXJrZXJIZWlnaHQ9IjkiIHJlZlg9IjciIHJlZlk9IjMiIG9yaWVudD0iYXV0byI+CiAgICAgIDxwYXRoIGQ9Ik0wLDAgTDcsMyBMMCw2IFoiIGZpbGw9IiMwMGU1ZmYiLz4KICAgIDwvbWFya2VyPgogIDwvZGVmcz4KCiAgPHJlY3Qgd2lkdGg9IjEyMDAiIGhlaWdodD0iNjIwIiBmaWxsPSJ1cmwoI2JnKSIvPgogIDx0ZXh0IHg9IjQwIiB5PSI0NSIgY2xhc3M9InRpdGxlIiBmb250LXNpemU9IjI0Ij5FbW90aWNhIEFJIOKAlCBTeXN0ZW0gQXJjaGl0ZWN0dXJlPC90ZXh0PgogIDx0ZXh0IHg9IjQwIiB5PSI2OCIgY2xhc3M9InN1YiI+V2ViY2FtIOKGkiBGYWNlIERldGVjdGlvbiDihpIgRW1vdGlvbiBDTk4g4oaSIE1vb2QtTWF0Y2hlZCBNdXNpYywgd2l0aCBTUUxpdGUgbG9nZ2luZyAmYW1wOyBsaXZlIGFuYWx5dGljczwvdGV4dD4KCiAgPCEtLSBSb3cgMTogSW5wdXQgcGlwZWxpbmUgLS0+CiAgPHJlY3QgeD0iNDAiIHk9IjExMCIgd2lkdGg9IjIyMCIgaGVpZ2h0PSIxMTAiIGNsYXNzPSJjYXJkIi8+CiAgPHRleHQgeD0iNjAiIHk9IjE0MCIgY2xhc3M9ImxhYmVsIj5DQVBUVVJFPC90ZXh0PgogIDx0ZXh0IHg9IjYwIiB5PSIxNjUiIGNsYXNzPSJ0aXRsZSIgZm9udC1zaXplPSIxNSI+Q2FtZXJhU3RyZWFtPC90ZXh0PgogIDx0ZXh0IHg9IjYwIiB5PSIxODUiIGNsYXNzPSJzdWIiPmNhbWVyYS5weSDigJQgdGhyZWFkZWQ8L3RleHQ+CiAgPHRleHQgeD0iNjAiIHk9IjIwMiIgY2xhc3M9InN1YiI+Y3YyLlZpZGVvQ2FwdHVyZSByZWFkZXI8L3RleHQ+CgogIDxyZWN0IHg9IjMxMCIgeT0iMTEwIiB3aWR0aD0iMjIwIiBoZWlnaHQ9IjExMCIgY2xhc3M9ImNhcmQiLz4KICA8dGV4dCB4PSIzMzAiIHk9IjE0MCIgY2xhc3M9ImxhYmVsIj5ERVRFQ1Q8L3RleHQ+CiAgPHRleHQgeD0iMzMwIiB5PSIxNjUiIGNsYXNzPSJ0aXRsZSIgZm9udC1zaXplPSIxNSI+RmFjZURldGVjdG9yPC90ZXh0PgogIDx0ZXh0IHg9IjMzMCIgeT0iMTg1IiBjbGFzcz0ic3ViIj5NZWRpYVBpcGUgZmFjZV9kZXRlY3Rpb248L3RleHQ+CiAgPHRleHQgeD0iMzMwIiB5PSIyMDIiIGNsYXNzPSJzdWIiPmV2ZXJ5IGZyYW1lIOKGkiBGYWNlQm94PC90ZXh0PgoKICA8cmVjdCB4PSI1ODAiIHk9IjExMCIgd2lkdGg9IjIyMCIgaGVpZ2h0PSIxMTAiIGNsYXNzPSJjYXJkIi8+CiAgPHRleHQgeD0iNjAwIiB5PSIxNDAiIGNsYXNzPSJsYWJlbCI+Q0xBU1NJRlk8L3RleHQ+CiAgPHRleHQgeD0iNjAwIiB5PSIxNjUiIGNsYXNzPSJ0aXRsZSIgZm9udC1zaXplPSIxNSI+RW1vdGlvbk1vZGVsPC90ZXh0PgogIDx0ZXh0IHg9IjYwMCIgeT0iMTg1IiBjbGFzcz0ic3ViIj5lbW90aW9uX21vZGVsLnB5IChLZXJhcyk8L3RleHQ+CiAgPHRleHQgeD0iNjAwIiB5PSIyMDIiIGNsYXNzPSJzdWIiPmV2ZXJ5IE4gZnJhbWVzIOKGkiBsYWJlbCArICU8L3RleHQ+CgogIDxyZWN0IHg9Ijg1MCIgeT0iMTEwIiB3aWR0aD0iMzEwIiBoZWlnaHQ9IjExMCIgY2xhc3M9ImNhcmQiLz4KICA8dGV4dCB4PSI4NzAiIHk9IjE0MCIgY2xhc3M9ImxhYmVsIj5SRVNQT05EPC90ZXh0PgogIDx0ZXh0IHg9Ijg3MCIgeT0iMTY1IiBjbGFzcz0idGl0bGUiIGZvbnQtc2l6ZT0iMTUiPk11c2ljUGxheWVyPC90ZXh0PgogIDx0ZXh0IHg9Ijg3MCIgeT0iMTg1IiBjbGFzcz0ic3ViIj5tdXNpY19wbGF5ZXIucHkgKHB5Z2FtZS5taXhlcik8L3RleHQ+CiAgPHRleHQgeD0iODcwIiB5PSIyMDIiIGNsYXNzPSJzdWIiPkVNT1RJT05fTVVTSUNfTUFQIOKGkiBtb29kIGZvbGRlcjwvdGV4dD4KCiAgPHBhdGggY2xhc3M9ImFycm93IiBkPSJNMjYwLDE2NSBIMzEwIi8+CiAgPHBhdGggY2xhc3M9ImFycm93IiBkPSJNNTMwLDE2NSBINTgwIi8+CiAgPHBhdGggY2xhc3M9ImFycm93IiBkPSJNODAwLDE2NSBIODUwIi8+CgogIDwhLS0gUm93IDI6IFBlcnNpc3RlbmNlICsgVUkgLS0+CiAgPHJlY3QgeD0iNDAiIHk9IjI4MCIgd2lkdGg9IjMzMCIgaGVpZ2h0PSIxMjAiIGNsYXNzPSJjYXJkIi8+CiAgPHRleHQgeD0iNjAiIHk9IjMxMCIgY2xhc3M9ImxhYmVsIj5QRVJTSVNURU5DRTwvdGV4dD4KICA8dGV4dCB4PSI2MCIgeT0iMzM1IiBjbGFzcz0idGl0bGUiIGZvbnQtc2l6ZT0iMTUiPkRhdGFiYXNlIChTUUxpdGUpPC90ZXh0PgogIDx0ZXh0IHg9IjYwIiB5PSIzNTYiIGNsYXNzPSJzdWIiPmRhdGFiYXNlLnB5IOKAlCBkZXRlY3Rpb25zIHRhYmxlPC90ZXh0PgogIDx0ZXh0IHg9IjYwIiB5PSIzNzQiIGNsYXNzPSJzdWIiPnRpbWVzdGFtcCDCtyBlbW90aW9uIMK3IGNvbmZpZGVuY2Ugwrcgc29uZzwvdGV4dD4KCiAgPHJlY3QgeD0iNDEwIiB5PSIyODAiIHdpZHRoPSIzMzAiIGhlaWdodD0iMTIwIiBjbGFzcz0iY2FyZCIvPgogIDx0ZXh0IHg9IjQzMCIgeT0iMzEwIiBjbGFzcz0ibGFiZWwiPkFOQUxZVElDUzwvdGV4dD4KICA8dGV4dCB4PSI0MzAiIHk9IjMzNSIgY2xhc3M9InRpdGxlIiBmb250LXNpemU9IjE1Ij5QbG90bHkgQ2hhcnRzPC90ZXh0PgogIDx0ZXh0IHg9IjQzMCIgeT0iMzU2IiBjbGFzcz0ic3ViIj5hbmFseXRpY3MucHkg4oCUIHBpZSAvIGJhciAvIHRpbWVsaW5lPC90ZXh0PgogIDx0ZXh0IHg9IjQzMCIgeT0iMzc0IiBjbGFzcz0ic3ViIj5saXZlIHRyZW5kICsgdG9wLWVtb3Rpb24gZG9udXQ8L3RleHQ+CgogIDxyZWN0IHg9Ijc4MCIgeT0iMjgwIiB3aWR0aD0iMzgwIiBoZWlnaHQ9IjEyMCIgY2xhc3M9ImNhcmQiLz4KICA8dGV4dCB4PSI4MDAiIHk9IjMxMCIgY2xhc3M9ImxhYmVsIj5QUkVTRU5UQVRJT048L3RleHQ+CiAgPHRleHQgeD0iODAwIiB5PSIzMzUiIGNsYXNzPSJ0aXRsZSIgZm9udC1zaXplPSIxNSI+U3RyZWFtbGl0IE11bHRpcGFnZSBBcHA8L3RleHQ+CiAgPHRleHQgeD0iODAwIiB5PSIzNTYiIGNsYXNzPSJzdWIiPmFwcC5weSArIHBhZ2VzLyAoTGl2ZSDCtyBBbmFseXRpY3Mgwrc8L3RleHQ+CiAgPHRleHQgeD0iODAwIiB5PSIzNzQiIGNsYXNzPSJzdWIiPlNvbmcgTWFuYWdlciDCtyBTZXR0aW5ncyDCtyBBYm91dCk8L3RleHQ+CgogIDxwYXRoIGNsYXNzPSJhcnJvdyIgZD0iTTk2MCwyMjAgVjI4MCIvPgogIDxwYXRoIGNsYXNzPSJhcnJvdyIgZD0iTTY5MCwyMjAgUTY5MCwyNTAgNTcwLDI4MCIvPgogIDxwYXRoIGNsYXNzPSJhcnJvdyIgZD0iTTIwNSwyMjAgUTIwNSwyNTAgMjA1LDI4MCIvPgogIDxwYXRoIGNsYXNzPSJhcnJvdyIgZD0iTTM3MCwzNDAgSDQxMCIvPgogIDxwYXRoIGNsYXNzPSJhcnJvdyIgZD0iTTc0MCwzNDAgSDc4MCIvPgoKICA8IS0tIFJvdyAzOiBUcmFpbmluZy9vZmZsaW5lIHRvb2xzIC0tPgogIDxyZWN0IHg9IjQwIiB5PSI0NTAiIHdpZHRoPSIxMTIwIiBoZWlnaHQ9IjEzMCIgY2xhc3M9ImNhcmQiIGZpbGw9InJnYmEoMTI0LDc3LDI1NSwwLjA2KSIvPgogIDx0ZXh0IHg9IjYwIiB5PSI0ODAiIGNsYXNzPSJsYWJlbCI+T0ZGTElORSAvIFRSQUlOSU5HIFRPT0xTIChydW4gb3V0c2lkZSBTdHJlYW1saXQpPC90ZXh0PgoKICA8ZyBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiPgogICAgPHJlY3QgeD0iNjAiIHk9IjUwMCIgd2lkdGg9IjI1MCIgaGVpZ2h0PSI2MCIgcng9IjEwIiBmaWxsPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDQpIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIvPgogICAgPHRleHQgeD0iNzUiIHk9IjUyMiIgZmlsbD0iI2ZmZDU0ZiIgZm9udC1zaXplPSIxMyIgZm9udC13ZWlnaHQ9IjcwMCI+Y29sbGVjdF9mYWNlcy5weTwvdGV4dD4KICAgIDx0ZXh0IHg9Ijc1IiB5PSI1NDIiIGZpbGw9IiM4YTk0YTgiIGZvbnQtc2l6ZT0iMTEiPldlYmNhbSBkYXRhc2V0IGNvbGxlY3RvciAoNCBjbGFzc2VzKTwvdGV4dD4KCiAgICA8cmVjdCB4PSIzMzAiIHk9IjUwMCIgd2lkdGg9IjI1MCIgaGVpZ2h0PSI2MCIgcng9IjEwIiBmaWxsPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDQpIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIvPgogICAgPHRleHQgeD0iMzQ1IiB5PSI1MjIiIGZpbGw9IiM0ZmMzZjciIGZvbnQtc2l6ZT0iMTMiIGZvbnQtd2VpZ2h0PSI3MDAiPnRyYWluX21vZGVsLnB5PC90ZXh0PgogICAgPHRleHQgeD0iMzQ1IiB5PSI1NDIiIGZpbGw9IiM4YTk0YTgiIGZvbnQtc2l6ZT0iMTEiPkZFUjIwMTMgQ05OIGZyb20gc2NyYXRjaDwvdGV4dD4KCiAgICA8cmVjdCB4PSI2MDAiIHk9IjUwMCIgd2lkdGg9IjI1MCIgaGVpZ2h0PSI2MCIgcng9IjEwIiBmaWxsPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDQpIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIvPgogICAgPHRleHQgeD0iNjE1IiB5PSI1MjIiIGZpbGw9IiMwMGU2NzYiIGZvbnQtc2l6ZT0iMTMiIGZvbnQtd2VpZ2h0PSI3MDAiPnRyYWluX2N1c3RvbV9tb2RlbC5weTwvdGV4dD4KICAgIDx0ZXh0IHg9IjYxNSIgeT0iNTQyIiBmaWxsPSIjOGE5NGE4IiBmb250LXNpemU9IjExIj5MaWdodCBDTk4gb24geW91ciBvd24gZGF0YXNldDwvdGV4dD4KCiAgICA8cmVjdCB4PSI4NzAiIHk9IjUwMCIgd2lkdGg9IjI1MCIgaGVpZ2h0PSI2MCIgcng9IjEwIiBmaWxsPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDQpIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIvPgogICAgPHRleHQgeD0iODg1IiB5PSI1MjIiIGZpbGw9IiNmZjUyNTIiIGZvbnQtc2l6ZT0iMTMiIGZvbnQtd2VpZ2h0PSI3MDAiPnRyYWluX3RyYW5zZmVyX21vZGVsLnB5PC90ZXh0PgogICAgPHRleHQgeD0iODg1IiB5PSI1NDIiIGZpbGw9IiM4YTk0YTgiIGZvbnQtc2l6ZT0iMTEiPk1vYmlsZU5ldFYyIHRyYW5zZmVyIGxlYXJuaW5nPC90ZXh0PgogIDwvZz4KCiAgPHBhdGggY2xhc3M9ImFycm93IiBkPSJNMTEwMCw0NTAgVjIzMCBRMTEwMCwxNTAgMTE2MCwxNTAiIG9wYWNpdHk9IjAiLz4KICA8cGF0aCBkPSJNNjAwLDUwMCBWNDUwIiBzdHJva2U9InVybCgjYWNjZW50KSIgc3Ryb2tlLXdpZHRoPSIyIiBmaWxsPSJub25lIiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93aGVhZCkiIG9wYWNpdHk9IjAuNSIvPgogIDx0ZXh0IHg9IjEwMTAiIHk9IjYwNSIgY2xhc3M9InN1YiIgdGV4dC1hbmNob3I9ImVuZCI+QWxsIHRocmVlIHByb2R1Y2Ug4oaSIG1vZGVscy9lbW90aW9uX21vZGVsLmg1IChhdXRvLWRldGVjdGVkIGJ5IHNoYXBlKTwvdGV4dD4KPC9zdmc+Cg==" alt="Architecture Diagram" width="100%">

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Emotion → Music Mapping](#emotion--music-mapping)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Getting a Model — 3 Ways to Train](#getting-a-model--3-ways-to-train)
- [Adding Music](#adding-music)
- [Running the App](#running-the-app)
- [Data & Analytics](#data--analytics)
- [Configuration Reference](#configuration-reference)
- [Performance Notes](#performance-notes)
- [Troubleshooting](#troubleshooting)
- [Technology Stack](#technology-stack)
- [Roadmap Ideas](#roadmap-ideas)
- [License](#license)

---

## Overview

Emotica AI is a Streamlit application built around a simple loop:

> **Webcam → Face Detection (MediaPipe) → Emotion Classification (CNN) → Mood-Matched Music (pygame) → Logged Detection (SQLite) → Live Analytics (Plotly)**

The current model classifies **4 emotions** — `Angry`, `Happy`, `Neutral`, `Sad` — and the project ships with **three different, swappable ways to produce the model file** (`models/emotion_model.h5`), so you can choose the training path that fits your data:

| Script | Approach | Best for |
|---|---|---|
| `train_model.py` | CNN from scratch on the public **FER2013** dataset | Large, generic labeled data (~36k images), no custom data collection needed |
| `train_custom_model.py` | A smaller, heavily-regularized CNN trained on **your own webcam photos** | Small self-collected datasets (hundreds of images), better real-world accuracy for *your* face |
| `train_transfer_model.py` | **MobileNetV2 transfer learning** fine-tuned on your own webcam photos | Best generalization from a small custom dataset — recommended default |

`emotion_model.py` auto-detects which kind of model is loaded (grayscale 48×48 vs. color 96×96) purely from the saved file's input shape, so the rest of the app (camera preprocessing, live inference) adapts automatically — no manual switching required.

---

## Features

- 🎥 **Smooth live webcam feed** — capture runs on its own background thread (`camera.py`) so the UI never blocks on `cv2.VideoCapture.read()`
- 🙂 **MediaPipe face detection** every frame, with a live bounding box overlay
- 🧠 **CNN emotion classification**, throttled to every *N* frames (configurable) since it's the heavier step
- 📈 **Per-detection confidence score** (e.g. `Happy (98%)`), with an "Uncertain" fallback below a configurable threshold
- 🎵 **Automatic, no-repeat music playback**, switching only when the *effective* mood changes (so jittery predictions don't restart a song every frame)
- 🗄️ **SQLite-backed detection history** (`emotica.db`) — thread-safe, one connection per thread
- 📊 **Plotly analytics dashboard** — emotion pie chart, bar chart, timeline, live trend line, and a "top emotion" donut
- 🛠️ **Custom dataset collector** (`collect_faces.py`) — a standalone OpenCV tool to capture your own labeled face bursts for the 4 emotions
- 🎚️ **Fully configurable** camera resolution/FPS, playback volume, auto-play toggle, and confidence threshold, all from the Settings page
- 🌓 **Polished dark glassmorphism UI** shared across every page via a single CSS injection (`utils.py`)
- 🩹 **Graceful degradation** — the app never crashes if the model or songs are missing; it shows clear on-screen guidance instead

---

## Emotion → Music Mapping

<img src="data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMTAwMCAzODAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8cmFkaWFsR3JhZGllbnQgaWQ9ImJnMiIgY3g9IjIwJSIgY3k9IjAlIiByPSIxMDAlIj4KICAgICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iIzEwMWEzMyIvPgogICAgICA8c3RvcCBvZmZzZXQ9IjU1JSIgc3RvcC1jb2xvcj0iIzBhMGUxYSIvPgogICAgPC9yYWRpYWxHcmFkaWVudD4KICAgIDxtYXJrZXIgaWQ9ImFycm93MiIgbWFya2VyV2lkdGg9IjkiIG1hcmtlckhlaWdodD0iOSIgcmVmWD0iNyIgcmVmWT0iMyIgb3JpZW50PSJhdXRvIj4KICAgICAgPHBhdGggZD0iTTAsMCBMNywzIEwwLDYgWiIgZmlsbD0iIzhhOTRhOCIvPgogICAgPC9tYXJrZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIxMDAwIiBoZWlnaHQ9IjM4MCIgZmlsbD0idXJsKCNiZzIpIi8+CiAgPHRleHQgeD0iNDAiIHk9IjQ1IiBmaWxsPSIjZThlY2Y1IiBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiIGZvbnQtd2VpZ2h0PSI3MDAiIGZvbnQtc2l6ZT0iMjIiPkVtb3Rpb24g4oaSIE11c2ljIE1vb2QgTWFwPC90ZXh0PgogIDx0ZXh0IHg9IjQwIiB5PSI2OCIgZmlsbD0iIzhhOTRhOCIgZm9udC1mYW1pbHk9IlNlZ29lIFVJLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEzIj5jb25maWcuRU1PVElPTl9NVVNJQ19NQVAg4oCUIGRlZmluZWQgb25jZSwgdXNlZCBieSBNdXNpY1BsYXllciBhbmQgdGhlIEhvbWUgZGFzaGJvYXJkPC90ZXh0PgoKICA8IS0tIEhhcHB5IC0tPgogIDxjaXJjbGUgY3g9IjE0MCIgY3k9IjE2MCIgcj0iNDYiIGZpbGw9InJnYmEoMjU1LDIxMyw3OSwwLjEyKSIgc3Ryb2tlPSIjZmZkNTRmIiBzdHJva2Utd2lkdGg9IjIiLz4KICA8dGV4dCB4PSIxNDAiIHk9IjE1MyIgZmlsbD0iI2ZmZDU0ZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIyNiI+8J+YhDwvdGV4dD4KICA8dGV4dCB4PSIxNDAiIHk9IjE3OCIgZmlsbD0iI2U4ZWNmNSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlNlZ29lIFVJLCBzYW5zLXNlcmlmIiBmb250LXdlaWdodD0iNzAwIiBmb250LXNpemU9IjE0Ij5IYXBweTwvdGV4dD4KICA8cGF0aCBkPSJNMTg2LDE2MCBIMzAwIiBzdHJva2U9IiM4YTk0YTgiIHN0cm9rZS13aWR0aD0iMiIgbWFya2VyLWVuZD0idXJsKCNhcnJvdzIpIi8+CiAgPHJlY3QgeD0iMzAwIiB5PSIxMzUiIHdpZHRoPSIxNTAiIGhlaWdodD0iNTAiIHJ4PSIxMCIgZmlsbD0icmdiYSgyNTUsMjEzLDc5LDAuMDgpIiBzdHJva2U9InJnYmEoMjU1LDIxMyw3OSwwLjMpIi8+CiAgPHRleHQgeD0iMzc1IiB5PSIxNjUiIGZpbGw9IiNmZmQ1NGYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJTZWdvZSBVSSwgc2Fucy1zZXJpZiIgZm9udC13ZWlnaHQ9IjcwMCIgZm9udC1zaXplPSIxNCI+c29uZ3MvaGFwcHkvPC90ZXh0PgoKICA8IS0tIFNhZCAtLT4KICA8Y2lyY2xlIGN4PSIxNDAiIGN5PSIyNTAiIHI9IjQ2IiBmaWxsPSJyZ2JhKDc5LDE5NSwyNDcsMC4xMikiIHN0cm9rZT0iIzRmYzNmNyIgc3Ryb2tlLXdpZHRoPSIyIi8+CiAgPHRleHQgeD0iMTQwIiB5PSIyNDMiIGZpbGw9IiM0ZmMzZjciIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMjYiPvCfmKI8L3RleHQ+CiAgPHRleHQgeD0iMTQwIiB5PSIyNjgiIGZpbGw9IiNlOGVjZjUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJTZWdvZSBVSSwgc2Fucy1zZXJpZiIgZm9udC13ZWlnaHQ9IjcwMCIgZm9udC1zaXplPSIxNCI+U2FkPC90ZXh0PgogIDxwYXRoIGQ9Ik0xODYsMjUwIEgzMDAiIHN0cm9rZT0iIzhhOTRhOCIgc3Ryb2tlLXdpZHRoPSIyIiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93MikiLz4KICA8cmVjdCB4PSIzMDAiIHk9IjIyNSIgd2lkdGg9IjE1MCIgaGVpZ2h0PSI1MCIgcng9IjEwIiBmaWxsPSJyZ2JhKDc5LDE5NSwyNDcsMC4wOCkiIHN0cm9rZT0icmdiYSg3OSwxOTUsMjQ3LDAuMykiLz4KICA8dGV4dCB4PSIzNzUiIHk9IjI1NSIgZmlsbD0iIzRmYzNmNyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlNlZ29lIFVJLCBzYW5zLXNlcmlmIiBmb250LXdlaWdodD0iNzAwIiBmb250LXNpemU9IjE0Ij5zb25ncy9tb3RpdmF0aW9uLzwvdGV4dD4KCiAgPCEtLSBBbmdyeSAtLT4KICA8Y2lyY2xlIGN4PSIxNDAiIGN5PSI3MCIgcj0iNDYiIGZpbGw9InJnYmEoMjU1LDgyLDgyLDAuMTIpIiBzdHJva2U9IiNmZjUyNTIiIHN0cm9rZS13aWR0aD0iMiIvPgogIDx0ZXh0IHg9IjE0MCIgeT0iNjMiIGZpbGw9IiNmZjUyNTIiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMjYiPvCfmKA8L3RleHQ+CiAgPHRleHQgeD0iMTQwIiB5PSI4OCIgZmlsbD0iI2U4ZWNmNSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlNlZ29lIFVJLCBzYW5zLXNlcmlmIiBmb250LXdlaWdodD0iNzAwIiBmb250LXNpemU9IjE0Ij5BbmdyeTwvdGV4dD4KICA8cGF0aCBkPSJNMTg2LDcwIEgzMDAiIHN0cm9rZT0iIzhhOTRhOCIgc3Ryb2tlLXdpZHRoPSIyIiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93MikiLz4KICA8cmVjdCB4PSIzMDAiIHk9IjQ1IiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjUwIiByeD0iMTAiIGZpbGw9InJnYmEoMjU1LDgyLDgyLDAuMDgpIiBzdHJva2U9InJnYmEoMjU1LDgyLDgyLDAuMykiLz4KICA8dGV4dCB4PSIzNzUiIHk9Ijc1IiBmaWxsPSIjZmY1MjUyIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiIGZvbnQtd2VpZ2h0PSI3MDAiIGZvbnQtc2l6ZT0iMTQiPnNvbmdzL2NhbG0vPC90ZXh0PgoKICA8IS0tIE5ldXRyYWwgLS0+CiAgPGNpcmNsZSBjeD0iMTQwIiBjeT0iMzMwIiByPSI0MCIgZmlsbD0icmdiYSgxNzYsMTkwLDE5NywwLjEyKSIgc3Ryb2tlPSIjYjBiZWM1IiBzdHJva2Utd2lkdGg9IjIiLz4KICA8dGV4dCB4PSIxNDAiIHk9IjMyMyIgZmlsbD0iI2IwYmVjNSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIyMiI+8J+YkDwvdGV4dD4KICA8dGV4dCB4PSIxNDAiIHk9IjM0NSIgZmlsbD0iI2U4ZWNmNSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlNlZ29lIFVJLCBzYW5zLXNlcmlmIiBmb250LXdlaWdodD0iNzAwIiBmb250LXNpemU9IjEzIj5OZXV0cmFsPC90ZXh0PgogIDxwYXRoIGQ9Ik0xODAsMzMwIEgzMDAiIHN0cm9rZT0iIzhhOTRhOCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtZGFzaGFycmF5PSI0LDQiIG1hcmtlci1lbmQ9InVybCgjYXJyb3cyKSIvPgogIDx0ZXh0IHg9IjMyMCIgeT0iMzM1IiBmaWxsPSIjOGE5NGE4IiBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTMiPm5vIGF1dG8tcGxheSAoYnkgZGVzaWduKTwvdGV4dD4KCiAgPCEtLSBSaWdodCBzaWRlOiBwbGF5YmFjayBlbmdpbmUgLS0+CiAgPHJlY3QgeD0iNTQwIiB5PSI5MCIgd2lkdGg9IjQyMCIgaGVpZ2h0PSIyMjAiIHJ4PSIxNiIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjA0KSIgc3Ryb2tlPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMTIpIi8+CiAgPHRleHQgeD0iNTY1IiB5PSIxMjUiIGZpbGw9IiMwMGU1ZmYiIGZvbnQtZmFtaWx5PSJTZWdvZSBVSSwgc2Fucy1zZXJpZiIgZm9udC13ZWlnaHQ9IjcwMCIgZm9udC1zaXplPSIxMyIgbGV0dGVyLXNwYWNpbmc9IjEiPk1VU0lDUExBWUVSIEVOR0lORTwvdGV4dD4KICA8dGV4dCB4PSI1NjUiIHk9IjE1NSIgZmlsbD0iI2U4ZWNmNSIgZm9udC1mYW1pbHk9IlNlZ29lIFVJLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEzIj4xLiBTd2l0Y2hlcyBvbmx5IHdoZW4gbW9vZCBjaGFuZ2VzPC90ZXh0PgogIDx0ZXh0IHg9IjU2NSIgeT0iMTgwIiBmaWxsPSIjZThlY2Y1IiBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTMiPiAgIChqaXR0ZXJ5IHByZWRpY3Rpb25zIGRvbid0IHJlc3RhcnQgc29uZ3MpPC90ZXh0PgogIDx0ZXh0IHg9IjU2NSIgeT0iMjEwIiBmaWxsPSIjZThlY2Y1IiBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTMiPjIuIFJhbmRvbSBwaWNrLCBuZXZlciByZXBlYXRzIHRoZTwvdGV4dD4KICA8dGV4dCB4PSI1NjUiIHk9IjIzNSIgZmlsbD0iI2U4ZWNmNSIgZm9udC1mYW1pbHk9IlNlZ29lIFVJLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEzIj4gICBwcmV2aW91cyB0cmFjayBpbiB0aGUgc2FtZSBtb29kPC90ZXh0PgogIDx0ZXh0IHg9IjU2NSIgeT0iMjY1IiBmaWxsPSIjZThlY2Y1IiBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTMiPjMuIHB5Z2FtZS5taXhlci5tdXNpYyBwbGF5YmFjayArPC90ZXh0PgogIDx0ZXh0IHg9IjU2NSIgeT0iMjkwIiBmaWxsPSIjZThlY2Y1IiBmb250LWZhbWlseT0iU2Vnb2UgVUksIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTMiPiAgIHZvbHVtZSAvIHBhdXNlIC8gZWxhcHNlZC10aW1lIGNvbnRyb2w8L3RleHQ+CgogIDxwYXRoIGQ9Ik00NTAsMTYwIFE1MDAsMTYwIDU0MCwxNjAiIHN0cm9rZT0iIzAwZTVmZiIgc3Ryb2tlLXdpZHRoPSIyIiBmaWxsPSJub25lIiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93MikiLz4KPC9zdmc+Cg==" alt="Emotion Flow Diagram" width="100%">

| Emotion | Mood Folder | Behavior |
|---|---|---|
| Happy | `songs/happy/` | Upbeat / feel-good tracks |
| Sad | `songs/motivation/` | Uplifting tracks to lift the mood |
| Angry | `songs/calm/` | Calm / relaxing tracks |
| Neutral | — | No auto-play, by design |

This mapping lives in a single place, `config.EMOTION_MUSIC_MAP`, so changing it (or adding moods) never requires touching playback logic.

---

## Project Structure

```
emotica-ai/
├── app.py                      # Home dashboard + shared session state (entry point)
├── camera.py                   # Threaded webcam capture + MediaPipe face detection
├── emotion_model.py            # CNN architectures (3 variants) + cached model loader
├── database.py                 # Thread-safe SQLite persistence layer
├── analytics.py                # Plotly chart builders for the Analytics page
├── music_player.py             # pygame-based mood music playback engine
├── utils.py                    # Glassmorphism theming + shared UI helpers
├── config.py                   # All constants, paths, and the emotion→music map
│
├── collect_faces.py            # Standalone webcam tool to build your own dataset
├── train_model.py               # Train from scratch on FER2013
├── train_custom_model.py        # Train a small CNN on your own collected images
├── train_transfer_model.py      # Train via MobileNetV2 transfer learning (recommended)
├── test_camera.py               # Standalone camera/backend diagnostic tool
│
├── requirements.txt
├── README.md
├── emotica.db                   # SQLite database (created automatically)
│
├── assets/                      # Logo & static images
├── models/                      # emotion_model.h5 lives here (you generate it)
├── data/
│   ├── fer2013.csv              # only needed for train_model.py
│   └── custom/
│       ├── Angry/                # PNG bursts from collect_faces.py
│       ├── Happy/
│       ├── Neutral/
│       └── Sad/
├── songs/
│   ├── happy/                   # Happy   → upbeat tracks
│   ├── motivation/               # Sad     → uplifting tracks
│   └── calm/                     # Angry   → relaxing tracks
│                                  # Neutral → no auto-play, by design
└── pages/                        # Streamlit auto-builds sidebar nav from these
    ├── 1_📷_Live_Detection.py
    ├── 2_📊_Analytics.py
    ├── 3_🎵_Song_Manager.py
    ├── 4_⚙️_Settings.py
    └── 5_ℹ️_About.py
```

> Streamlit auto-discovers everything under `pages/` and builds the sidebar navigation from those files — `app.py` only renders the Home dashboard and initializes the session state every page shares.

---

## Installation

**Requirements:** Python 3.10+, a working webcam, and (for audio) a working audio output device.

```bash
# 1. Clone / unzip the project, then move into it
cd emotica-ai

# 2. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

<details>
<summary>Key dependencies (see <code>requirements.txt</code> for exact pins)</summary>

```
streamlit>=1.35
opencv-contrib-python==4.11.0.86
tensorflow==2.15.1
mediapipe==0.10.21
numpy==1.26.4
protobuf==4.25.3
pandas>=2.2
Pillow>=10.3
pygame>=2.5
plotly>=5.22
streamlit-extras>=0.4
mutagen>=1.47
```
</details>

Until a trained model exists at `models/emotion_model.h5`, the app runs fine — the Home page shows a clear warning banner and the Live Detection page stays disabled rather than crashing.

---

## Getting a Model — 3 Ways to Train

### Option A — Recommended: MobileNetV2 Transfer Learning on Your Own Face

Best real-world accuracy for a small, personal dataset.

```bash
# Step 1 — collect your own labeled dataset via webcam
python collect_faces.py
#   a / h / n / s  → select label (Angry / Happy / Neutral / Sad)
#   SPACE          → capture a 3-second burst (~20 images)
#   q              → quit
# Aim for 150–200+ images per emotion, across multiple sittings
# (different lighting/rooms) so the model learns expressions, not the room.

# Step 2 — train
python train_transfer_model.py
```

Training runs in two phases: the classification head trains first with the MobileNetV2 backbone frozen, then the last few backbone layers are unfrozen for low-learning-rate fine-tuning. `--head-epochs`, `--finetune-epochs`, `--finetune-layers`, `--batch-size`, and `--val-split` are all configurable via CLI flags.

### Option B — Small CNN From Scratch on Your Own Face

Simpler and faster to train than Option A, still tailored to your own data (uses the same `collect_faces.py` dataset).

```bash
python collect_faces.py            # if not already collected
python train_custom_model.py --epochs 60 --batch-size 32
```

### Option C — Classic CNN on the Public FER2013 Dataset

No webcam data collection required, but the original FER2013 label set is 7-class; you'll want to adapt `config.EMOTION_LABELS` accordingly if you go this route.

```bash
# 1. Download fer2013.csv (Kaggle) and place it at data/fer2013.csv
# 2. Train
python train_model.py --epochs 60 --batch-size 64
```

All three scripts save the best checkpoint to `models/emotion_model.h5` — whichever one you run last is the model the Streamlit app will load. Both custom-data scripts split train/validation **by capture burst, not by individual frame**, since frames from the same 3-second burst are near-duplicates; splitting at the frame level would let near-identical images leak across the split and produce misleadingly high validation accuracy that doesn't hold up on live video.

---

## Adding Music

Drop `.mp3`, `.wav`, or `.ogg` files into the mood folders under `songs/` (see the [mapping table](#emotion--music-mapping) above). Nothing needs to be registered — files are auto-discovered on every page load, and playback picks a random track per mood without repeating the immediately-previous one.

---

## Running the App

```bash
streamlit run app.py
```

Open the printed local URL, go to **📷 Live Detection**, and click **Start Camera**.

---

## Data & Analytics

Every detection (timestamp, emotion, confidence, song played) is written to a local SQLite database (`emotica.db`) via `database.py`. The **📊 Analytics** page (`analytics.py`) turns that history into:

- An emotion distribution **pie chart** and **bar chart**
- A **timeline scatter plot** of detections over time, sized by confidence
- A **live trend line** of confidence over the last N seconds
- A compact **"top emotion" donut** for at-a-glance summaries
- Summary stats: total detections, most frequent emotion, average confidence

---

## Configuration Reference

All tunables live in `config.py` — nothing else in the codebase hard-codes these values:

| Setting | Default | Purpose |
|---|---|---|
| `FACE_IMG_SIZE` | `48` | Input size for grayscale (from-scratch) models |
| `TRANSFER_IMG_SIZE` | `96` | Input size for the MobileNetV2 transfer model |
| `EMOTION_LABELS` | `["Angry","Happy","Neutral","Sad"]` | Class order — must match dataset folder names exactly |
| `INFERENCE_EVERY_N_FRAMES` | `3` | How often the (heavier) CNN classification runs; face *detection* still runs every frame |
| `MIN_FACE_DETECTION_CONFIDENCE` | `0.6` | MediaPipe face detector threshold |
| `DEFAULT_CONFIDENCE_THRESHOLD` | `0.55` | Below this, the UI shows "Uncertain" instead of a label |
| `DEFAULT_CAMERA_WIDTH / HEIGHT` | `640 x 480` | Overridable from the Settings page |
| `DEFAULT_TARGET_FPS` | `30` | Camera capture target |
| `EMOTION_MUSIC_MAP` | see table above | Single source of truth for emotion → mood folder |
| `SUPPORTED_AUDIO_EXT` | `.mp3 .wav .ogg` | File types the Song Manager will discover |

---

## Performance Notes

- Camera capture runs on its own background thread (`camera.py`), so the UI never blocks on `cv2.VideoCapture.read()`; only the latest frame is kept, so consumers never fall behind.
- Face **detection** runs every frame (MediaPipe is fast); CNN **classification** runs every `INFERENCE_EVERY_N_FRAMES` frames since it's the heavier step — this keeps the feed smooth without sacrificing responsiveness.
- The Keras model is loaded **once per server process** via `st.cache_resource`, not on every Streamlit rerun.
- Camera resolution/target FPS are adjustable from the Settings page; actual achievable FPS depends on your webcam and CPU/GPU.
- On Windows, the app prefers the `DSHOW` backend (more reliable than `CAP_ANY`) and automatically falls back across a matrix of backends/indices if the preferred one fails — the same logic `test_camera.py` exposes standalone for diagnostics.

---

## Troubleshooting

**Camera won't open / "No working webcam found"**
Run `python test_camera.py` — it scans every backend/index combo the app would try and reports which one works. Common causes: another app (Zoom/Teams/browser tab) has the camera open, or OS-level camera privacy permissions are off.

**"Emotion model not found" warning on Home page**
You haven't trained a model yet — see [Getting a Model](#getting-a-model--3-ways-to-train). The app is fully usable otherwise; only Live Detection stays disabled.

**No sound / music doesn't play**
Check that `songs/<mood>/` actually contains `.mp3`/`.wav`/`.ogg` files, and that `pygame.mixer.init()` succeeded (check the terminal log — it fails quietly if no audio device is available).

**Model trained but accuracy is poor on live video**
Almost always a dataset issue, not a modeling one: collect more images (150–200+ per emotion), across *multiple sittings* with different lighting, and make expressions clearly exaggerated — see the tips in `collect_faces.py`'s docstring, especially the Angry-vs-Sad distinction.

---

## Technology Stack

**Python 3.10+** · **Streamlit** (UI/pages) · **OpenCV** (video I/O) · **MediaPipe** (face detection) · **TensorFlow / Keras** (CNN + MobileNetV2 transfer learning) · **NumPy / Pandas** (data handling) · **Pillow** · **pygame** (audio playback) · **SQLite** (persistence) · **Plotly** (analytics charts) · **mutagen** (audio metadata)

---

## Roadmap Ideas

- Re-add the additional FER2013 emotion classes (Fear, Surprise, Disgust) as optional mood folders
- Export/import detection history as CSV from the Analytics page
- Multi-face support (currently the largest detected face drives playback)
- Dockerfile for one-command setup

---

## License

No license file is currently included with this project. Add one (e.g. MIT, Apache-2.0) before distributing or open-sourcing.

---

*Emotica AI — built with Streamlit, TensorFlow, and a genuine dislike of choosing your own playlist.*
