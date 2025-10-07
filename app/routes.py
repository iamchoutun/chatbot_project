import os
import logging
import pandas as pd
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from app.utils import VERIFY_TOKEN
from app.ai_engine import faq_bot
from app.messenger import send_text, send_image

# ================= ROUTER & LOGGER =================
router = APIRouter()
log = logging.getLogger("uvicorn.error")

# Path to the CSV file storing FAQs
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "faq.csv")

# ================== WEBHOOK VERIFICATION ==================
@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    """
    Verify Facebook webhook subscription.
    """
    hub_mode = request.query_params.get("hub.mode")
    hub_challenge = request.query_params.get("hub.challenge")
    hub_verify_token = request.query_params.get("hub.verify_token")

    log.debug("Received verification request: %s", hub_verify_token)

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge or ""
    raise HTTPException(status_code=403, detail="Verification token mismatch")


# ================== WEBHOOK EVENTS ==================
@router.post("/webhook")
async def receive_webhook(req: Request):
    """
    Receive messages from Facebook Messenger webhook and respond using FAQBot.
    """
    data = await req.json()
    log.debug("Webhook received: %s", data)

    if "entry" in data:
        for entry in data["entry"]:
            for ev in entry.get("messaging", []):
                sender_id = ev.get("sender", {}).get("id")
                message = ev.get("message", {})
                text = message.get("text")

                if sender_id and text:
                    answer = faq_bot.get_answer(text)

                    # Check if answer is an image URL (format: [[IMAGE: URL]])
                    if isinstance(answer, str) and answer.startswith("[[IMAGE:") and answer.endswith("]]"):
                        url = answer.replace("[[IMAGE:", "").replace("]]", "").strip()
                        send_image(sender_id, url)
                    else:
                        send_text(sender_id, answer)

    return {"status": "ok"}


# ================== ADMIN ENDPOINTS ==================
@router.post("/reload-faq")
async def reload_faq():
    """
    Reload FAQ data from CSV file without restarting the server.
    """
    try:
        faq_bot.reload_faq()
        return {"status": "success", "message": "FAQ reloaded successfully"}
    except Exception as e:
        log.error("Failed to reload FAQ: %s", e)
        return {"status": "error", "message": str(e)}


@router.post("/update-faq")
async def update_faq(req: Request):
    """
    Update FAQ from JSON payload and reload into faq_bot.
    
    Expected JSON format: [{"question": "...", "answer": "..."}]
    """
    try:
        data = await req.json()
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Data must be a list of {question, answer}")

        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")

        # Reload FAQBot
        faq_bot.reload_faq()

        return {"status": "success", "message": "FAQ updated and loaded successfully"}
    except Exception as e:
        log.error("Failed to update FAQ: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/faq-data")
async def get_faq_data():
    """
    Fetch current FAQ data as a JSON list for editor tools.
    """
    try:
        df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        log.error("Failed to fetch FAQ data: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
