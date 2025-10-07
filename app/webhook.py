from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from app.utils import VERIFY_TOKEN  # Import from utils securely

# ================= ROUTER =================
router = APIRouter()

# ================== WEBHOOK VERIFICATION ==================
@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    """
    Verify Facebook webhook subscription using the token defined in utils.py.

    Expected query parameters:
        - hub.mode
        - hub.challenge
        - hub.verify_token
    """
    hub_mode = request.query_params.get("hub.mode")
    hub_challenge = request.query_params.get("hub.challenge")
    hub_verify_token = request.query_params.get("hub.verify_token")

    # Log the incoming verification request
    # (Use logger in production; print for quick debugging)
    print("Received verification request:", hub_verify_token)

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        # Return the challenge token to confirm subscription
        return hub_challenge or ""

    # Verification failed
    raise HTTPException(status_code=403, detail="Verification token mismatch")
