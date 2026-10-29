import httpx
from app.core.config import settings

def check_connection():
    base = settings.llama_cpp_base_url.rstrip("/")
    try:
        r = httpx.get(f"{base}/models", timeout=10)
        data = r.json() if r.status_code==200 else {}
        audio_supported = False
        model_info = {}
        for m in data.get("data", []):
            modalities = m.get("architecture", {}).get("input_modalities", [])
            if "audio" in modalities:
                audio_supported = True
            model_info[m.get("id")] = {"input_modalities": modalities, "output_modalities": m.get("architecture", {}).get("output_modalities", [])}
        return {
            "status":"ok" if r.status_code==200 else "error",
            "code":r.status_code,
            "audio_supported": audio_supported,
            "models": model_info,
        }
    except Exception as e:
        return {"status":"unreachable","error":str(e),"audio_supported":False}

def transcribe(audio_path):
    raise RuntimeError(
        "Ce runtime llama.cpp expose uniquement les modalités text (pas audio). "
        "Utilisez NeMo-Speech.cpp ou vLLM pour NVIDIA Nemotron 3.5 Transcribe."
    )
