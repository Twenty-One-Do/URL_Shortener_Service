from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import pytz

class URLRequest(BaseModel):
    url: str
    expiration_datetime: Optional[datetime] = Field(None, description="Expiration datetime for the short URL")

    @validator('expiration_datetime', pre=True, always=True)
    def convert_to_utc(cls, value):
        if value:
            try:
                seoul_tz = pytz.timezone('Asia/Seoul')
                local_dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                local_dt = seoul_tz.localize(local_dt)
                return local_dt.astimezone(pytz.utc)
            except ValueError as e:
                raise ValueError("Invalid datetime format. Use 'YYYY-MM-DDTHH:MM:SS' format.") from e
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
