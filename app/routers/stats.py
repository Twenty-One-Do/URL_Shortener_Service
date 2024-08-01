from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import crud, models
from ..database import get_db
from typing import Dict

router = APIRouter()

@router.get("/stats/{short_key}")
async def get_stats(short_key: str, db: Session = Depends(get_db)) -> Dict:
    short_url = crud.get_short_url(db, short_key)

    if short_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    total_clicks = db.query(func.count(models.ShortUrlStat.id)).filter(
        models.ShortUrlStat.short_url_id == short_url.id
    ).scalar()

    device_categories = ["PC", "Tablet", "Mobile", "Unknown"]
    device_stats_dict = {category: 0 for category in device_categories}

    device_stats = db.query(models.ShortUrlStat.device_type, func.count(models.ShortUrlStat.id)).filter(
        models.ShortUrlStat.short_url_id == short_url.id
    ).group_by(models.ShortUrlStat.device_type).all()

    for device_type, count in device_stats:
        if device_type in device_stats_dict:
            device_stats_dict[device_type] = count

    return {
        "total_clicks": total_clicks,
        "device_stats": device_stats_dict
    }
