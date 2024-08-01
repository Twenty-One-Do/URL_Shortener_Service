import string, random, pytz
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()

def save_click_stat(db: Session, short_url_id: int, ip: str, device_type: str):
    click_stat = models.ShortUrlStat(
        short_url_id=short_url_id,
        device_type=device_type,
        click_time=datetime.now(),
        ip=ip
    )
    db.add(click_stat)
    db.commit()

def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@router.get("/{short_key}", response_class=RedirectResponse)
async def redirect_to_url(short_key: str, request: Request, background_tasks: BackgroundTasks,
                          db: Session = Depends(get_db)):
    short_url = crud.get_short_url(db, short_key)

    if short_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if short_url.expiration_date and short_url.expiration_date < datetime.now():
        raise HTTPException(status_code=404, detail="Short URL expired")

    redirect_url = short_url.path.base_url.base_url + short_url.path.path

    client_ip = request.client.host
    user_agent = request.headers.get('user-agent', 'unknown')

    background_tasks.add_task(save_click_stat, db, short_url.id, client_ip, user_agent)

    return RedirectResponse(url=redirect_url, status_code=301)

@router.post("/shorten", response_model=schemas.ShortURLResponse)
def shorten_url(url_request: schemas.URLRequest, db: Session = Depends(get_db)):

    short_url_key = generate_short_key()
    while crud.get_short_url(db, short_url_key):
        short_url_key = generate_short_key()

    short_url_entry = crud.create_short_url(db=db,
                                            url=url_request.url,
                                            short_url=short_url_key,
                                            expiration_datetime=url_request.expiration_datetime)

    return schemas.ShortURLResponse(short_url=short_url_entry.short_url)
