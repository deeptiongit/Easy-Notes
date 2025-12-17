from database import database, schemas
from sqlalchemy.orm import Session
from ..utils import currentuser
from fastapi import APIRouter,Depends
from database.repository import client

router = APIRouter(
    tags=["client"],
)

get_db = database.get_db


@router.post('/register', response_model=schemas.ShowClient)
def create_user(request: schemas.Client,db: Session = Depends(get_db)):
    return client.create(request,db)

@router.get('/{id}', response_model=schemas.ShowClient )
def get_user(id:int,db: Session = Depends(get_db) ,
              current_user: schemas.client.Client = Depends(currentuser.get_current_client) ):
    return client.show(id,db)
