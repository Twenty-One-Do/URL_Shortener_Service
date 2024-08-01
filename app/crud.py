from sqlalchemy.orm import Session
from urllib.parse import urlparse
from . import models
from datetime import datetime, timedelta
from typing import Optional

def create_short_url(db: Session, url: str, short_url: str, expiration_datetime: Optional[datetime] = None):
    parsed_url = urlparse(url)
    base_url_str = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path = parsed_url.path

    # base_url 중복 체크
    base_url = db.query(models.BaseUrl).filter(models.BaseUrl.base_url == base_url_str).first()
    if not base_url:
        base_url = models.BaseUrl(base_url=base_url_str)
        db.add(base_url)
        db.commit()
        db.refresh(base_url)

    # path 중복 체크
    path_entry = db.query(models.Path).filter(models.Path.path == path, models.Path.base_url_id == base_url.id).first()
    if not path_entry:
        path_entry = models.Path(path=path, base_url_id=base_url.id)
        db.add(path_entry)
        db.commit()
        db.refresh(path_entry)

    # short_url 생성
    short_url_entry = models.ShortUrl(short_url=short_url,
                                      path_id=path_entry.id,
                                      expiration_date=expiration_datetime)
    db.add(short_url_entry)
    db.commit()
    db.refresh(short_url_entry)

    return short_url_entry

def get_short_url(db: Session, short_url: str):
    return db.query(models.ShortUrl).filter(models.ShortUrl.short_url == short_url).first()
