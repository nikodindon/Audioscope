import subprocess, os

def extract_audio(video_path, out_path):
    subprocess.run(["ffmpeg","-y","-i",video_path,"-vn","-acodec","pcm_s16le","-ar","16000","-ac","1",out_path],check=True)
    return out_path
