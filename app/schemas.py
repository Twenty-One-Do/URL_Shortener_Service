from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import pytz
from dateutil import parser

class URLRequest(BaseModel):
    url: str
    expiration_datetime: Optional[datetime] = Field(None, description="Expiration datetime for the short URL")

    @validator('expiration_datetime', pre=True, always=True)
    def convert_to_utc(cls, value):
        if value:
            try:
                parsed_dt = parser.isoparse(value)

                if parsed_dt.tzinfo is None:
                    seoul_tz = pytz.timezone('Asia/Seoul')
                    parsed_dt = seoul_tz.localize(parsed_dt)

                return parsed_dt.astimezone(pytz.utc)
            except (ValueError, TypeError) as e:
                raise ValueError("Invalid datetime format. Please use a recognizable format.") from e
        return value

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
