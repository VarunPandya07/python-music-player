FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV SDL_AUDIODRIVER=alsa

# Install dependencies for GUI (Tkinter) and audio (ALSA)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    libasound2 \
    libasound2-dev \
    alsa-utils \
    libglib2.0-0 \
    x11-apps \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip install --no-cache-dir pygame Pillow

# Set work directory
WORKDIR /app

# Copy everything into container
COPY . .

# Run the GUI application
CMD ["python", "main.py"]
