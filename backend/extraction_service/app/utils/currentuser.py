from database import schemas , models
from fastapi import Depends, HTTPException
from . import oauth2
from sqlalchemy.orm import Session
from database import database

get_db = database.get_db


def get_current_client(
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.Client).filter(models.Client.email == token_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
