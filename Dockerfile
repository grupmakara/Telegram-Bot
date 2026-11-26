FROM node:22-bookworm-slim

# FFmpeg ve Python (yt-dlp ile Whisper için)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg python3 python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Whisper'ı yalnızca CPU sürümü torch ile kur (GPU sürümünden birkaç GB küçük).
ENV VIRTUAL_ENV=/opt/venv PATH=/opt/venv/bin:$PATH
ARG WHISPER_MODEL=base
RUN python3 -m venv /opt/venv \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir openai-whisper yt-dlp \
    && python3 -c "import whisper; whisper.load_model('${WHISPER_MODEL}')"
ENV WHISPER_MODEL=${WHISPER_MODEL}

WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev --no-audit --no-fund
COPY . .

CMD ["node", "index.js"]
