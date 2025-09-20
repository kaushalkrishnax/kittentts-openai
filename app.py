from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import StreamingResponse
from kittentts import KittenTTS
import io
import soundfile as sf
from typing import Optional

# -------- Config --------
API_KEY = "changeme"  # set a strong key in prod
SAMPLE_RATE = 25000   # match your working prototype
AVAILABLE_VOICES = [
    "expr-voice-2-m","expr-voice-2-f",
    "expr-voice-3-m","expr-voice-3-f",
    "expr-voice-4-m","expr-voice-4-f",
    "expr-voice-5-m","expr-voice-5-f"
]

# -------- FastAPI --------
app = FastAPI(title="KittenTTS OpenAI Spec API")

# Initialize KittenTTS model (newer model you tested)
tts_model = KittenTTS("KittenML/kitten-tts-nano-0.2")

# -------- Helpers --------
def check_auth(authorization: Optional[str]):
    if API_KEY == "":
        return True
    if not authorization:
        return False
    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1].strip()
        return token == API_KEY
    return False

# -------- Endpoints --------
@app.get("/health")
def health():
    return {"ok": True, "model": "KittenTTS", "sample_rate": SAMPLE_RATE}

@app.get("/v1/voices")
def voices(authorization: Optional[str] = Header(None)):
    if not check_auth(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"voices": AVAILABLE_VOICES}

@app.post("/v1/audio/speech")
async def synthesize(request: Request, authorization: Optional[str] = Header(None)):
    if not check_auth(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")

    payload = await request.json()
    text = payload.get("input") or payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="`input` or `text` required")

    voice = payload.get("voice", "expr-voice-3-m")
    if voice not in AVAILABLE_VOICES:
        voice = "expr-voice-3-m"

    # Optional speed param (not used directly by KittenTTS yet)
    speed = float(payload.get("speed", 1.0))

    try:
        # Generate audio with KittenTTS
        audio = tts_model.generate(text, voice=voice)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Stream WAV back
    buf = io.BytesIO()
    sf.write(buf, audio, SAMPLE_RATE, format="WAV")
    buf.seek(0)
    return StreamingResponse(buf, media_type="audio/wav")

