# postPinMock.py
# This file is used to mock the Pinterest API for testing purposes.
# It is used to test the Pinterest API before it is implemented in the main file.
# It is not used in the production environment.
# To run the file, use the following command:
# python3 -m uvicorn postPinMock:app --reload

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class ProductTag(BaseModel):
    pin_id: str

class MediaItem(BaseModel):
    title: str
    description: str
    link: str
    content_type: str
    data: str

class MediaSource(BaseModel):
    source_type: str
    items: Optional[List[MediaItem]] = None
    index: Optional[int] = 0
    content_type: Optional[str] = None
    data: Optional[str] = None
    is_standard: Optional[bool] = True

class PinData(BaseModel):
    link: Optional[str] = None
    title: str
    description: str
    dominant_color: Optional[str] = "#FFFFFF"
    alt_text: Optional[str] = None
    board_id: Optional[str]
    board_section_id: Optional[str] = None
    media_source: MediaSource
    parent_pin_id: Optional[str] = None
    note: Optional[str] = None
    product_tags: Optional[List[ProductTag]] = None
    sponsor_id: Optional[str] = None
    is_removable: Optional[bool] = True

@app.post("/mock-pinterest/pins")
async def mock_post_pin(pin: PinData, response: Response):
    # Simulate saving or posting data
    print("\n🎯 Pin Received:")
    print(f"📌 Title: {pin.title}")
    print(f"📝 Description: {pin.description}")
    print(f"📷 Alt Text: {pin.alt_text}")
    print(f"🧃 Base64 Image (preview): {pin.media_source.data[:100]}...\n") # type: ignore

    response.status_code = 201
    return {
        "status": "success",
        "message": "Mock pin received successfully",
        "data": pin
    }
