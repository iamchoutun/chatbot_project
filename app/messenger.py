import requests
from app.utils import PAGE_ACCESS_TOKEN, FB_API_URL  # Securely import tokens and URLs

# ================== FACEBOOK MESSENGER FUNCTIONS ==================

def send_text(recipient_id: str, text: str) -> dict:
    """
    Send a text message to a Facebook user via Messenger Graph API.

    Args:
        recipient_id (str): Facebook user ID to send the message to.
        text (str): Text content of the message.

    Returns:
        dict: JSON response from Facebook Graph API or fallback dict on error.
    """
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}

    try:
        res = requests.post(FB_API_URL, params=params, json=payload, timeout=5)
        res.raise_for_status()  # Raise HTTPError if request failed
        return res.json()
    except requests.RequestException as e:
        # Return fallback info in case of network or HTTP error
        return {"error": str(e), "status": getattr(res, "status_code", None), "text": getattr(res, "text", "")}


def send_image(recipient_id: str, image_url: str) -> dict:
    """
    Send an image message to a Facebook user via Messenger Graph API.

    Args:
        recipient_id (str): Facebook user ID to send the image to.
        image_url (str): URL of the image to send.

    Returns:
        dict: JSON response from Facebook Graph API or fallback dict on error.
    """
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {"url": image_url, "is_reusable": True}
            }
        }
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}

    try:
        res = requests.post(FB_API_URL, params=params, json=payload, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        return {"error": str(e), "status": getattr(res, "status_code", None), "text": getattr(res, "text", "")}
