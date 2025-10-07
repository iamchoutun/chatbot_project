from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Import routers
from app.routes import router as api_router
from app.webhook import router as webhook_router

# Import global FAQBot instance
from app.ai_engine import faq_bot

# ================= FASTAPI APP =================
app = FastAPI(title="FAQ Chatbot")

# Include API and webhook routers
app.include_router(api_router)
app.include_router(webhook_router)


# ================== ENDPOINTS ==================
@app.post("/reload-faq")
async def reload_faq() -> JSONResponse:
    """
    Reload the FAQ data from the CSV file.

    Returns:
        JSONResponse: Success message or error details.
    """
    try:
        faq_bot.reload_faq()
        return JSONResponse(content={"message": "FAQ reloaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
