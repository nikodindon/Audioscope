import os, json
from app.db.database import SessionLocal
from app.db.models import Video, Job, Transcript
from app.services.media.downloader import download
from app.services.media.audio import extract_audio
from app.services.inference.llama_cpp import transcribe
from app.services.subtitles import segments_to_srt, segments_to_vtt
from app.core.config import settings

def run_import(url):
    db=SessionLocal()
    try:
        data_dir=settings.data_dir
        os.makedirs(os.path.join(data_dir,"library"),exist_ok=True)
        os.makedirs(os.path.join(data_dir,"audio"),exist_ok=True)
        os.makedirs(os.path.join(data_dir,"transcripts"),exist_ok=True)
        os.makedirs(os.path.join(data_dir,"subtitles"),exist_ok=True)
        vid, vpath = download(url, os.path.join(data_dir,"library"))
        v=Video(source_url=url,status="downloaded")
        db.add(v); db.commit(); db.refresh(v)
        j=Job(video_id=v.id,type="transcribe",status="running"); db.add(j); db.commit()
        apath=os.path.join(data_dir,"audio",f"{vid}.wav")
        extract_audio(vpath,apath)
        result=transcribe(apath)
        segs=result.get("segments", [])
        if not segs and result.get("text"):
            segs=[{"start":0,"end":0,"text":result["text"]}]
        tdir=os.path.join(data_dir,"transcripts")
        base=f"video_{v.id}"
        json_path=os.path.join(tdir,base+".json")
        txt_path=os.path.join(tdir,base+".txt")
        srt_path=os.path.join(data_dir,"subtitles",base+".srt")
        vtt_path=os.path.join(data_dir,"subtitles",base+".vtt")
        with open(json_path,"w") as f: json.dump({"segments":segs},f,indent=2)
        with open(txt_path,"w") as f: f.write("\n".join(s["text"] for s in segs))
        with open(srt_path,"w") as f: f.write(segments_to_srt(segs))
        with open(vtt_path,"w") as f: f.write(segments_to_vtt(segs))
        tr=Transcript(video_id=v.id,language=result.get("language"),json_path=json_path,txt_path=txt_path,srt_path=srt_path,vtt_path=vtt_path)
        db.add(tr); j.status="done"; v.status="ready"; db.commit()
        return {"video_id":v.id,"status":"done"}
    except Exception as e:
        if 'j' in locals(): j.status="failed"; j.error=str(e); db.commit()
        raise
    finally:
        db.close()
