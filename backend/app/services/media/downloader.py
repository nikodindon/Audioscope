import subprocess, os, uuid, sys

def download(url, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    vid = uuid.uuid4().hex[:12]
    path = os.path.join(out_dir, f"{vid}.mp4")
    subprocess.run([sys.executable, "-m", "yt_dlp", "--no-playlist", "--merge-output-format", "mp4", "-o", path, url], check=True)
    return vid, path
