"""
Run script for starting the FAQ Chatbot FastAPI server on Render.

Uses environment variable PORT to determine the listening port.
"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (Render provides PORT automatically)
    port = int(os.getenv("PORT", 8000))

    # Start FastAPI app using Uvicorn
    uvicorn.run(
        "app.main:app",  # path to FastAPI app
        host="0.0.0.0",  # listen on all interfaces
        port=port,
        reload=True      # keep True for development, False for production
    )
