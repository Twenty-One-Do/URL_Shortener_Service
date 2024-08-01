import string, random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@router.post("/shorten", response_model=schemas.ShortURLResponse)
def shorten_url(url_request: schemas.URLRequest, db: Session = Depends(get_db)):

    short_url_key = generate_short_key()
    while crud.get_short_url(db, short_url_key):
        short_url_key = generate_short_key()

    short_url_entry = crud.create_short_url(db=db, url=url_request.url, short_url=short_url_key)
    return schemas.ShortURLResponse(short_url=short_url_entry.short_url)
