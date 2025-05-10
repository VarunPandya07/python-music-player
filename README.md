# 🎵 Tkinter Audio Player

A simple GUI-based audio player built using **Python**, **Tkinter**, and **Pygame**, packaged to run inside a **Docker container** with audio and GUI support.

---

## 📦 Features

- Play, pause, resume, stop MP3 files
- Next/previous track support
- GUI using Tkinter
- Uses `pygame.mixer` for audio playback
- Runs inside Docker with X11 and ALSA/PulseAudio support

---

## 📁 Folder Structure

```
project/
│
├── Dockerfile
├── main.py
├── icon/                # Button & logo icons
├── m/                   # Folder with your `.mp3` files
└── README.md
```

---

## 🐳 Run with Docker

### 1. Build the Docker image

```bash
docker build -t music-player .
```

### 2. Run the container (ALSA example)

```bash
xhost +local:root  # allow X11 access for audio & GUI

docker run -it --rm \
  --env DISPLAY=$DISPLAY \
  --env SDL_AUDIODRIVER=alsa \
  --device /dev/snd \
  --group-add audio \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "$PWD":/app \
  --name audio-player \
  music-player
```

> If you use **PulseAudio**, see "Advanced PulseAudio Support" below.

---

## 🛠️ Dependencies

Installed via Dockerfile:

- `python3`, `tkinter`, `pygame`, `Pillow`
- Audio & GUI libs: `libasound2`, `libglib2.0-0`, `alsa-utils`, `x11-apps`

---

## 📝 Usage

- Add `.mp3` files to the `m/` folder.
- Run the Docker container.
- Use the GUI to play/pause/skip/stop songs.

---

## 🧪 Troubleshooting

### ❌ `libgthread-2.0.so.0` missing?
Make sure your Dockerfile includes:

```Dockerfile
RUN apt-get install -y libglib2.0-0
```

### ❌ No audio?
Check:
- Your host audio driver is ALSA or PulseAudio.
- You passed `--device /dev/snd` and `--group-add audio` to Docker.
- You ran `xhost +local:root` before launching.

---

## 🔊 Advanced PulseAudio Support (Optional)

If you use **PulseAudio**, run Docker with:

```bash
docker run -it --rm \
  --env DISPLAY=$DISPLAY \
  --env PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native \
  --volume /tmp/.X11-unix:/tmp/.X11-unix \
  --volume ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native \
  --device /dev/snd \
  --group-add audio \
  -v "$PWD":/app \
  -v ~/.config/pulse/cookie:/root/.config/pulse/cookie \
  --name audio-player \
  music-player
```

---

