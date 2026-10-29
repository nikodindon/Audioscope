from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine
import app.db.models  # noqa
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AudioScope", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

from app.api.inference import router as inference_router
from app.api.importer import router as importer_router
app.include_router(inference_router)
app.include_router(importer_router)

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/config")
def config():
    return {"llama_cpp_base_url": settings.llama_cpp_base_url, "model": settings.llama_cpp_model, "data_dir": settings.data_dir}
