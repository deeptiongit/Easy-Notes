from database import database, schemas
from sqlalchemy.orm import Session
from ..utils import oauth2
from fastapi import APIRouter,Depends
from database.repository import client

router = APIRouter(
    prefix="/client",
    tags=["client"],
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowClient)
def create_user(request: schemas.Client,db: Session = Depends(get_db)):
    return client.create(request,db)

@router.get('/{id}', response_model=schemas.ShowClient )
def get_user(id:int,db: Session = Depends(get_db) , current_user: schemas.Client = Depends(oauth2.get_current_user) ):
    return client.show(id,db)
