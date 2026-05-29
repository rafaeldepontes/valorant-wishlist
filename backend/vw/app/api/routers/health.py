from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/health-check", tags=["Health Check"])

@router.get("")
async def health_check(request: Request):
    return {"status": "ok"}