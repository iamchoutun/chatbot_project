"""
Utility module for environment variables and constants used across the chatbot project.

This module loads sensitive credentials from a .env file and defines common constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ================== FACEBOOK TOKENS & CONFIG ==================

# Facebook Page Access Token for sending messages via Graph API
PAGE_ACCESS_TOKEN: str = os.getenv("PAGE_ACCESS_TOKEN", "")

# Verification token for Facebook Webhook
VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN", "default-verify-token")

# Backend host URL (used for webhooks or API calls)
BACKEND_HOST: str = os.getenv("BACKEND_HOST", "http://127.0.0.1:8000")

# Facebook Graph API URL to send messages
FB_API_URL: str = "https://graph.facebook.com/v21.0/me/messages"

# ================== VALIDATION / WARNINGS ==================

if not PAGE_ACCESS_TOKEN:
    import warnings
    warnings.warn(
        "PAGE_ACCESS_TOKEN is empty. Please set it in the .env file for production."
    )
