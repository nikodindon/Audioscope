import subprocess, os, uuid, json

def download(url, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    vid = uuid.uuid4().hex[:12]
    path = os.path.join(out_dir, f"{vid}.mp4")
    subprocess.run(["yt-dlp","--js-runtimes","node","-f","best[ext=mp4]/best","-o",path,url],check=True)
    return vid, path
