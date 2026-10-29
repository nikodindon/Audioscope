import httpx
from app.core.config import settings

def check_connection():
    base = settings.llama_cpp_base_url.rstrip("/")
    try:
        r = httpx.get(f"{base}/models", timeout=10)
        return {"status":"ok" if r.status_code==200 else "error","code":r.status_code,"body":r.text[:500]}
    except Exception as e:
        return {"status":"unreachable","error":str(e)}
