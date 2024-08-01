from pydantic import BaseModel
from typing import List

class URLRequest(BaseModel):
    url: str

class ShortURLResponse(BaseModel):
    short_url: str

class URLStats(BaseModel):
    device_type: str
    click_count: int

class ShortURLStats(BaseModel):
    short_url: str
    stats: List[URLStats]

class OriginalURLStats(BaseModel):
    original_url: str
    short_urls: List[ShortURLStats]
