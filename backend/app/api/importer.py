from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.services.jobs import run_import

router=APIRouter()
class ImportReq(BaseModel):
    url:str

@router.post("/import")
def import_url(req: ImportReq, bg: BackgroundTasks):
    bg.add_task(run_import, req.url)
    return {"status":"started"}
