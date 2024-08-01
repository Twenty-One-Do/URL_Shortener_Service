import string, random
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from .. import crud, schemas, models
from ..database import get_db, redis_client
from user_agents import parse

router = APIRouter()

def get_device_type(user_agent_str):
    user_agent = parse(user_agent_str)
    if user_agent.is_mobile:
        return "Mobile"
    elif user_agent.is_tablet:
        return "Tablet"
    elif user_agent.is_pc:
        return "PC"
    else:
        return "Unknown"

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
async def redirect_to_url(short_key: str, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    cached_data = redis_client.hgetall(short_key)
    if cached_data:
        redirect_url = cached_data.get(b'url').decode('utf-8')
        short_url_id = int(cached_data.get(b'id').decode('utf-8'))
    else:
        short_url = crud.get_short_url(db, short_key)
        if not short_url or (short_url.expiration_date and short_url.expiration_date < datetime.utcnow()):
            raise HTTPException(status_code=404, detail="Short URL not found or expired")

        redirect_url = short_url.path.base_url.base_url + short_url.path.path
        short_url_id = short_url.id

        redis_client.hmset(short_key, {'url': redirect_url, 'id': short_url_id})
        redis_client.expire(short_key, 3600)

    client_ip = request.client.host
    user_agent_str = request.headers.get('user-agent', 'unknown')
    device_type = get_device_type(user_agent_str)

    background_tasks.add_task(save_click_stat, db, short_url_id, client_ip, device_type)

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
