from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="AudioScope", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/config")
def config():
    return {"llama_cpp_base_url": settings.llama_cpp_base_url, "model": settings.llama_cpp_model, "data_dir": settings.data_dir}
