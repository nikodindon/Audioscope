from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    llama_cpp_base_url: str = "http://100.91.114.49:8080/v1"
    llama_cpp_model: str = "nemotron-transcribe"
    data_dir: str = "./data"
    database_url: str = "sqlite:///./data/audioscope.db"
    video_download_enabled: bool = True
    max_video_size_gb: int = 10
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()
