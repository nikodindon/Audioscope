from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base

class Video(Base):
    __tablename__="videos"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=True)
    source_url=Column(String)
    duration=Column(Float,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    status=Column(String,default="imported")

class Job(Base):
    __tablename__="jobs"
    id=Column(Integer,primary_key=True)
    video_id=Column(Integer,ForeignKey("videos.id"))
    type=Column(String)
    status=Column(String,default="pending")
    progress=Column(Float,default=0)
    error=Column(Text,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)

class Transcript(Base):
    __tablename__="transcripts"
    id=Column(Integer,primary_key=True)
    video_id=Column(Integer,ForeignKey("videos.id"))
    language=Column(String,nullable=True)
    json_path=Column(String)
    txt_path=Column(String)
    srt_path=Column(String)
    vtt_path=Column(String)
