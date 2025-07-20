# postToPinterest.py

import os
from dotenv import load_dotenv
import requests
import base64
import mimetypes

load_dotenv()

PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
PINTEREST_BOARD_ID = os.getenv("PINTEREST_BOARD_ID")

def image_url_to_base64(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch image")

    mime_type = response.headers.get("Content-Type", "image/jpeg")
    b64_data = base64.b64encode(response.content).decode("utf-8")

    return b64_data, mime_type

def post_pin_to_pinterest(product):
    image_data, content_type = image_url_to_base64(product["image"])

    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "board_id": PINTEREST_BOARD_ID,
        "title": product["title"],
        "alt_text": product["alt_text"],
        "description": product["description"],
        "link": product.get("link", os.getenv("AMAZON_HOME_AFFILIATE_LINK") or ""),
        "media_source": {
            "source_type": "image_base64",
            "content_type": content_type,
            "data": image_data
        }
    }

    response = requests.post(
        os.getenv("PINTEREST_ENDPOINT") or "",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        print("✅ Pin posted successfully!")
        print("📌 Response:", response.json())
    else:
        print("❌ Failed to post Pin:", response.status_code, response.text)

