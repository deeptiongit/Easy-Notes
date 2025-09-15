from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status
from ..hashing import Hash

def create(request: schemas.Client,db:Session):
    new_client = models.Client(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

def show(id:int,db:Session):
    client = db.query(models.Client).filter(id==models.Client.id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return client