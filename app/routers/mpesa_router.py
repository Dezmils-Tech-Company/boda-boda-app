from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from app.utils.mpesa_client import MpesaClient

router = APIRouter()

@router.post("/callback")
async def mpesa_callback(request: Request):
    try:
        data = await request.json()
        logger.info(f"M-Pesa Callback: {data}")
        # Process payment confirmation here
        # Update relevant contribution/loan/subscription
        return {"ResultCode": 0, "ResultDesc": "Accepted"}
    except Exception as e:
        logger.error(f"M-Pesa callback error: {e}")
        raise HTTPException(400, "Invalid callback")