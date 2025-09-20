---

# KittenTTS OpenAI-Spec Server

This repo provides a FastAPI wrapper around **KittenTTS**, exposing OpenAI-style endpoints for speech synthesis.
You can query it from your own clients or integrate with an OpenAI-spec web UI.

---

## 🚀 Installation

1. **Install KittenTTS wheel** (local package file):

```bash
pip install kittentts-0.1.0-py3-none-any.whl
```

2. **Install other dependencies**:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Server

Start the FastAPI server with `uvicorn`:

```bash
uvicorn server:app --host 0.0.0.0 --port 8081 --reload
```

The API will now be available at:

```
http://localhost:8081
```

---

## ✅ Available Endpoints

### Health check

```bash
curl http://localhost:8081/health
```

### Get available voices

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8081/v1/voices
```

### Generate speech

```bash
curl -X POST http://localhost:8081/v1/audio/speech \
  -H "Authorization: Bearer changeme" \
  -H "Content-Type: application/json" \
  -o output.wav \
  -d '{
    "input": "Hello, this is KittenTTS speaking!",
    "voice": "expr-voice-3-m"
  }'
```

---

## 🛠 Notes

* Default API key is `changeme`. Update `API_KEY` in `server.py` for production.
* Supported voices:
  `expr-voice-2-m`, `expr-voice-2-f`,
  `expr-voice-3-m`, `expr-voice-3-f`,
  `expr-voice-4-m`, `expr-voice-4-f`,
  `expr-voice-5-m`, `expr-voice-5-f`

---
# kittentts-openai
