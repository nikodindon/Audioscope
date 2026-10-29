from fastapi import APIRouter
from app.services.inference.llama_cpp import check_connection
router=APIRouter()

@router.get("/inference/check")
def inference_check():
    return check_connection()
